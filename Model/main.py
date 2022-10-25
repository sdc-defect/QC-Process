import argparse
import importlib
import os

import numpy as np
import yaml

from sklearn.model_selection import KFold
import tensorflow as tf
from keras.utils import Progbar

from utils.trainer import MyTrainer, MyTester, inference
from utils.preprocess import Preprocessor, get_index_batch_slices
from utils.saver import Saver
from dataset.read_record import get_dataset


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root",
                        type=str,
                        help="input root dir",
                        default=".")
    parser.add_argument("--config",
                        type=str,
                        help="input your yaml file path",
                        required=True)
    args = parser.parse_args()

    os.chdir(args.root)

    with open(args.config, "r") as f:
        config = yaml.load(f, yaml.FullLoader)

    user = config['user']
    save = config['save']
    module = config['module']
    cls = config['class']
    batch_size = config['batch_size']
    epochs = config['epochs']
    init_lr = config['init_lr']
    decay_steps = config['decay_steps']

    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        try:
            # tf.config.experimental.set_visible_devices(gpus[1:], 'GPU')
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            logical_gpus = tf.config.list_logical_devices('GPU')
            print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
        except RuntimeError as e:
            print(e)

    # Load Dataset
    train_dataset_img, train_dataset_label = get_dataset("dataset/train.tfrecord")
    val2_dataset_img, _ = get_dataset("dataset/val2.tfrecord")

    # Saver & Preprocessor
    saver = Saver(user=user, save=save)
    pre = Preprocessor()

    # Train
    module = importlib.import_module(f"train.{user}.{module}")
    for fold, (slices_train, slices_val) in enumerate(KFold(5, shuffle=True).split(range(len(train_dataset_img)))):
        saver.clear()

        train_aug_img, train_aug_label = pre.augment_dataset(train_dataset_img, train_dataset_label, slices_train)

        train_ds_img = train_dataset_img + train_aug_img
        train_ds_label = train_dataset_label + train_aug_label
        train_ds_slices = get_index_batch_slices(len(train_ds_img), batch_size)

        val1_ds_img = [train_dataset_img[i] for i in slices_val]
        val1_ds_label = [train_dataset_label[i] for i in slices_val]
        val1_ds_slices = get_index_batch_slices(len(val1_ds_img), batch_size)

        val2_ds_slices = get_index_batch_slices(len(val2_dataset_img), batch_size)

        # Load Model
        model = getattr(module, cls)()
        # model.build(input_shape=(None, 300, 300, 3))
        # model.summary()

        # Load Trainers
        trainer = MyTrainer(model=model, init_lr=init_lr, decay_steps=decay_steps)
        validator = MyTester(model=model)

        # Train
        for epoch in range(1, epochs + 1):
            print(f"fold {fold + 1}, epoch {epoch} / {epochs}")

            trainer.reset_matrix()
            validator.reset_matrix()

            # Train
            progbar = Progbar(len(train_ds_slices), width=50,
                              stateful_metrics=['loss', 'accuracy', 'def_recall', 'ok_recall', 'f1', 'ok_f1'])
            progbar.update(0, values=[('loss', 0), ('accuracy', 0), ('def_recall', 0),
                                      ('ok_recall', 0), ('f1', 0), ('ok_f1', 0)])
            for i, slice_list in enumerate(train_ds_slices):
                img = np.array([train_ds_img[i] for i in slice_list])
                label = np.array([train_ds_label[i] for i in slice_list])
                img = tf.image.grayscale_to_rgb(tf.convert_to_tensor(img))
                lab = tf.convert_to_tensor(label)
                trainer.train(img, lab)
                progbar.update(i + 1, values=[('loss', trainer.get_loss()), ('accuracy', trainer.get_accuracy()),
                                              ('def_recall', trainer.get_recall()), ('ok_recall', trainer.get_ok_recall()),
                                              ('f1', trainer.get_f1_score()), ('ok_f1', trainer.get_f1_score())])

            # Validation 1
            for slice_list in val1_ds_slices:
                img = np.array([val1_ds_img[i] for i in slice_list])
                label = np.array([val1_ds_label[i] for i in slice_list])
                img = tf.image.grayscale_to_rgb(tf.convert_to_tensor(img))
                lab = tf.convert_to_tensor(label)
                validator.test(img, lab)

            # Validation 2
            cnt = 0
            for slice_list in val2_ds_slices:
                img = np.array([val2_dataset_img[i] for i in slice_list])
                img = tf.image.grayscale_to_rgb(tf.convert_to_tensor(img))
                preds = inference(model, img)
                cnt += tf.reduce_sum(preds).numpy()

            print(
                f"1st validation loss: {validator.get_loss():.4f}, accuracy: {validator.get_accuracy():.4f}, "
                f"recall: {validator.get_recall():.4f}, ok_recall: {validator.get_ok_recall():.4f}, "
                f"f1 score: {validator.get_f1_score():.4f}, ok_f1 score: {validator.get_ok_f1_score():.4f}")
            print(f"2nd validation: {cnt} / 50\n")
            saver.save_train_log(fold + 1, epoch, trainer, validator, cnt)
            if cnt >= 48:
                saver.save_best_model(fold + 1, epoch, model,
                                      validator.get_recall(), validator.get_ok_recall(), validator.get_loss())

import argparse
import importlib
import os

import numpy as np
import yaml

from sklearn.model_selection import train_test_split
import tensorflow as tf
from keras.utils import Progbar

from utils.trainer import MyTrainer, MyTester, inference
from utils.matrix import Must, count_def_in_must_list
from utils.dataset import Preprocessor, get_index_batch_slices, get_dataset, get_dataset_with_fname
from utils.saver import Saver, save_test_log

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

    # Saver & Preprocessor
    saver = Saver(user=user, save=save)
    pre = Preprocessor()

    # Load Dataset
    train_dataset_img, train_dataset_label = get_dataset("dataset/train.tfrecord")
    val2_dataset_img, _, val2_dataset_fname = get_dataset_with_fname("dataset/val2.tfrecord")

    # Split Dataset into Train Validation
    train_img, val1_img, train_label, val1_label = train_test_split(train_dataset_img, train_dataset_label,
                                                                    test_size=0.2, shuffle=True, random_state=34)

    # Augment train image
    train_aug_img, train_aug_label = pre.augment_dataset(train_img, train_label)
    train_ds_img = train_dataset_img + train_aug_img
    train_ds_label = train_dataset_label + train_aug_label

    train_ds_slices = get_index_batch_slices(len(train_ds_img), batch_size)
    val1_ds_slices = get_index_batch_slices(len(val1_img), batch_size)
    val2_ds_slices = get_index_batch_slices(len(val2_dataset_img), batch_size)

    # Load Model
    module = importlib.import_module(f"train.{user}.{module}")
    model = getattr(module, cls)()

    # Load Trainers
    trainer = MyTrainer(model=model, init_lr=init_lr, decay_steps=decay_steps)
    validator = MyTester(model=model)

    # Train
    for epoch in range(1, epochs + 1):
        print(f"epoch {epoch} / {epochs}")

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
            img = np.array([val1_img[i] for i in slice_list])
            label = np.array([val1_label[i] for i in slice_list])
            img = tf.image.grayscale_to_rgb(tf.convert_to_tensor(img))
            lab = tf.convert_to_tensor(label)
            validator.test(img, lab)

        # Validation 2
        musts = []
        for slice_list in val2_ds_slices:
            img = np.array([val2_dataset_img[i] for i in slice_list])
            img = tf.image.grayscale_to_rgb(tf.convert_to_tensor(img))
            fnames = [val2_dataset_fname[i] for i in slice_list]
            predictions = inference(model, img)

            for fname, pred in zip(fnames, predictions.numpy()):
                correct = np.argmax(pred) == 1
                musts.append(Must(fname, correct, pred))

        cnt = count_def_in_must_list(musts)
        print(
            f"1st validation loss: {validator.get_loss():.4f}, accuracy: {validator.get_accuracy():.4f}, "
            f"recall: {validator.get_recall():.4f}, ok_recall: {validator.get_ok_recall():.4f}, "
            f"f1 score: {validator.get_f1_score():.4f}, ok_f1 score: {validator.get_ok_f1_score():.4f}")
        print(f"2nd validation: {cnt} / 50\n")
        saver.save_train_log(epoch, trainer, validator, cnt, musts)
        if cnt >= 48:
            saver.save_best_model(epoch, model,
                                  validator.get_recall(), validator.get_ok_recall(), validator.get_loss())

    # Test
    best_model = tf.saved_model.load(os.path.join("train", user, save))
    tester = MyTester(model=best_model)
    test_dataset_img, test_dataset_label, test_dataset_fname = get_dataset_with_fname("dataset/test.tfrecord")
    test_ds_slices = get_index_batch_slices(len(test_dataset_img), batch_size)
    test_logs = []
    for slice_list in test_ds_slices:
        img = np.array([test_dataset_img[i] for i in slice_list])
        label = np.array([test_dataset_label[i] for i in slice_list])
        fnames = [test_dataset_fname[i] for i in slice_list]
        img = tf.image.grayscale_to_rgb(tf.convert_to_tensor(img))
        lab = tf.convert_to_tensor(label)
        probs, results = tester.test(img, lab)
        for prob, result, fname in zip(probs, results, fnames):
            prob = prob.numpy()
            result = str(result.numpy())
            test_logs.append({fname: {"result": result, "probability": [float(prob[0]), float(prob[1])]}})

    print(f"test result - loss: {tester.get_loss():.4f}, accuracy: {tester.get_accuracy():.4f}, "
          f"recall: {tester.get_recall():.4f}, f1: {tester.get_f1_score():.4f}, "
          f"ok_recall: {tester.get_ok_recall():.4f}, ok_f1: {tester.get_ok_f1_score():.4f}")

    # Must
    must_dataset_img, _, must_dataset_fname = get_dataset_with_fname("dataset/must.tfrecord")
    img = tf.convert_to_tensor(np.array(must_dataset_img))
    predictions = inference(best_model, img)
    musts = []
    for i, (fname, pred) in enumerate(zip(must_dataset_fname, predictions.numpy())):
        correct = np.argmax(pred) == 1
        musts.append(Must(fname, correct, pred))

    # Save Log
    save_test_log(os.path.join("train", user, save), tester, musts, test_logs)

import argparse
import importlib
import os

import yaml
from sklearn.model_selection import KFold
import tensorflow as tf
from keras.utils.image_dataset import image_dataset_from_directory
from keras.utils import Progbar

from utils.trainer import MyTrainer, MyTester, inference
from utils.preprocess import Preprocessor
from utils.saver import Saver


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root",
                        type=str,
                        help="input root dir",
                        default=".")
    parser.add_argument("--config",
                        type=str,
                        help="input yaml file",
                        required=True)
    args = parser.parse_args()

    os.chdir(args.root)
    with open(args.config) as f:
        config = yaml.load(f, yaml.FullLoader)

    module = config['module']
    cls = config['class']
    root_dir = config['root_dir']
    save_dir = config['save_dir']
    batch_size = config['batch_size']
    epochs = config['epochs']
    init_lr = config['init_lr']
    decay_steps = config['decay_steps']

    # Load Dataset
    normalization_layer = tf.keras.layers.experimental.preprocessing.Rescaling(1. / 255)
    ds = image_dataset_from_directory(
        "dataset/train",
        image_size=(300, 300),
        batch_size=1)
    ds = ds.map(lambda x, y: (normalization_layer(x), tf.one_hot(y, 2)))
    val2_ds = image_dataset_from_directory(
        "dataset/val",
        image_size=(300, 300),
        shuffle=False,
        batch_size=batch_size)
    val2_ds = val2_ds.map(lambda x, y: (normalization_layer(x), tf.one_hot(y, 2)))

    pre = Preprocessor()

    # Train
    saver = Saver(folder=root_dir, save=save_dir)
    module = importlib.import_module(module)
    for fold, (train, val) in enumerate(KFold(5, shuffle=True).split(range(len(ds)))):
        train = [idx + 1 for idx in train]
        val = [idx + 1 for idx in val]

        train_ds = tf.data.Dataset.from_tensor_slices([ds.skip(t - 1).take(t) for t in train]).flat_map(
            lambda x: x).map(lambda x, y: (x[0, ...], y[0, ...]))
        val1_ds = tf.data.Dataset.from_tensor_slices([ds.skip(t - 1).take(t) for t in val]).flat_map(lambda x: x).map(
            lambda x, y: (x[0, ...], y[0, ...]))

        train_ds = train_ds.take(len(train)).batch(batch_size=batch_size, drop_remainder=True)
        val1_ds = val1_ds.take(len(val)).batch(batch_size=batch_size, drop_remainder=True)

        # Load Model
        model = getattr(module, cls)()

        # Load Trainers
        trainer = MyTrainer(model=model, init_lr=init_lr, decay_steps=decay_steps)
        validator = MyTester(model=model)

        # Train
        for epoch in range(1, epochs + 1):
            print(f"fold {fold + 1}, epoch {epoch} / {epochs}")

            trainer.reset_matrix()
            validator.reset_matrix()

            # Train
            progbar = Progbar(int(len(train) / batch_size), width=50,
                              stateful_metrics=['loss', 'accuracy', 'def_recall', 'ok_recall', 'f1', 'ok_f1'])
            progbar.update(0, values=[('loss', 0), ('accuracy', 0), ('def_recall', 0),
                                      ('ok_recall', 0), ('f1', 0), ('ok_f1', 0)])
            for i, (image, label) in enumerate(train_ds):
                img, lab = pre.preprocess(image, label)
                trainer.train(img, lab)
                progbar.update(i + 1, values=[('loss', trainer.get_loss()), ('accuracy', trainer.get_accuracy()),
                                              ('def_recall', trainer.get_recall()), ('ok_recall', trainer.get_ok_recall()),
                                              ('f1', trainer.get_f1_score()), ('ok_f1', trainer.get_f1_score())])

            # Validation 1
            for (image, label) in val1_ds:
                validator.test(image, label)

            # Validation 2
            cnt = 0
            for (image, label) in val2_ds:
                preds = inference(module, image)
                cnt += tf.reduce_sum(preds).numpy()

            print(
                f"1st validation loss: {validator.get_loss():.4f}, accuracy: {validator.get_accuracy():.4f}, "
                f"recall: {validator.get_recall():.4f}, ok_recall: {validator.get_ok_recall():.4f},"
                f"f1 score: {validator.get_f1_score():.4f}, ok_f1 score: {validator.get_ok_f1_score():.4f}")
            print(f"2nd validation: {cnt} / 50\n")
            saver.save_train_log(fold, epoch, trainer, validator, cnt)
            if cnt >= 48:
                saver.save_best_model(module, validator.get_recall(), validator.get_ok_recall())

    # Test
    best_model = tf.saved_model.load(os.path.join(root_dir, save_dir))
    tester = MyTester(model=best_model)
    test_ds = image_dataset_from_directory(
        "dataset/test",
        image_size=(300, 300),
        shuffle=False,
        batch_size=batch_size)
    test_ds = test_ds.map(lambda x, y: (normalization_layer(x), tf.one_hot(y, 2)))
    for image, label in test_ds:
        tester.test(image, label)
    saver.save_test_log(tester)

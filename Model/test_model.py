import argparse
import os

import pandas as pd
import numpy as np
import tensorflow as tf

from utils.trainer import MyTester
from utils.preprocess import get_index_batch_slices
from dataset.read_record import get_dataset


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root",
                        type=str,
                        help="input root dir",
                        default=".")
    parser.add_argument("--model",
                        type=str,
                        help="input folder name where your saved model file exists",
                        required=True)
    parser.add_argument("--batch",
                        type=int,
                        help="input batch size",
                        default=8)
    args = parser.parse_args()

    os.chdir(args.root)

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

    # Test
    best_model = tf.saved_model.load(os.path.join(args.model))
    tester = MyTester(model=best_model)
    test_dataset_img, test_dataset_label = get_dataset("dataset/test.tfrecord")
    test_ds_slices = get_index_batch_slices(len(test_dataset_img), args.batch)
    for slice_list in test_ds_slices:
        img = np.array([test_dataset_img[i] for i in slice_list])
        label = np.array([test_dataset_label[i] for i in slice_list])
        img = tf.image.grayscale_to_rgb(tf.convert_to_tensor(img))
        lab = tf.convert_to_tensor(label)
        tester.test(img, lab)
    print(f"test result - loss: {tester.get_loss():.4f}, accuracy: {tester.get_accuracy():.4f}, "
          f"recall: {tester.get_recall():.4f}, f1: {tester.get_f1_score():.4f}, "
          f"ok_recall: {tester.get_ok_recall():.4f}, ok_f1: {tester.get_ok_f1_score():.4f}")

    # Save Log
    tm = tester.get_confusion_matrix()
    tm_str = f"{tm.tp}-{tm.fn}-{tm.fp}-{tm.tn}"
    data = [tester.get_loss(), tester.get_accuracy(),
            tester.get_recall(), tester.get_f1_score(),
            tester.get_ok_recall(), tester.get_ok_f1_score(), tm_str]
    test_log = pd.DataFrame([data],
                            columns=["loss", "accuracy", "recall", "f1", "ok_recall", "ok_f1",
                                     "matrix(tp, fn, fp, tn)"])
    test_log.to_csv(os.path.join(args.model, f"test_log.csv"), index=False)

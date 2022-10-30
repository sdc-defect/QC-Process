import argparse
import json
import os

import pandas as pd
import numpy as np
import tensorflow as tf

from utils.matrix import Must
from utils.saver import save_test_log
from utils.trainer import MyTester, inference
from utils.preprocess import get_index_batch_slices
from dataset.read_record import get_dataset, get_dataset_with_fname


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root train/jjh/case1/case1",
                        type=str,
                        help="input root dir",
                        default=".")
    parser.add_argument("--model train/jjh/case1/case1",
                        type=str,
                        help="input folder name where your saved model file exists",
                        required=True)
    parser.add_argument("--batch train/jjh/case1/case1",
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

    best_model = tf.saved_model.load(os.path.join(args.model))

    # Test
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

    # Must
    must_dataset_img, _, must_dataset_fname = get_dataset_with_fname("dataset/must.tfrecord")
    img = tf.convert_to_tensor(np.array(must_dataset_img))
    predictions = inference(best_model, img)
    musts = []
    for i, (fname, pred) in enumerate(zip(must_dataset_fname, predictions.numpy())):
        correct = np.argmax(pred) == 1
        musts.append(Must(fname, correct, pred))

    # Save Log
    save_test_log(args.model, tester, musts)

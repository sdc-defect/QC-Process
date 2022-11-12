from typing import List, Tuple, Union

import random
import cv2
from glob import glob

import numpy as np
import albumentations as album
import tensorflow as tf
from sklearn.model_selection import train_test_split

from utils.dto import TrainConfig


def merge_dataset_path(path: List, img_size: Union[Tuple[int, int], int] = (300, 300)) \
        -> List[Tuple[np.ndarray, Tuple[float, float]]]:
    if not isinstance(path, list) and len(path) != 2:
        raise Exception("Wrong path input, input path must be List and length to be 2")
    if not (isinstance(img_size, tuple) or isinstance(img_size, int)):
        raise Exception("img_size type must be tuple[int, int] or int")
    if isinstance(img_size, tuple) and len(img_size) is not 2:
        raise Exception("Wrong img_size input, img_size length must be 2 if img_size is tuple")

    if isinstance(img_size, int):
        img_size = (img_size, img_size)

    paths = []
    labels = []

    paths0 = glob(path[0] + "/*")
    paths.extend(paths0)
    labels.extend([(1., 0.) for _ in range(len(paths0))])

    paths1 = glob(path[1] + "/*")
    paths.extend(paths1)
    labels.extend([(0., 1.) for _ in range(len(paths1))])

    merged = [(cv2.normalize(cv2.resize(cv2.imread(p), img_size), None, 0, 1, cv2.NORM_MINMAX, cv2.CV_32F), l)
              for p, l in zip(paths, labels)]

    random.shuffle(merged)

    return merged


def sample_beta_distribution(size, concentration_0=0.2, concentration_1=0.2):
    gamma_1_sample = tf.random.gamma(shape=[size], alpha=concentration_0)
    gamma_2_sample = tf.random.gamma(shape=[size], alpha=concentration_1)
    return gamma_1_sample / (gamma_1_sample + gamma_2_sample)


def mix_up(dataset: List[Tuple[np.ndarray, float]], per: float = 0.5):
    idx = [i for i in range(len(dataset))]
    random.shuffle(idx)

    center = int(len(dataset) * per)
    image1 = np.array([dataset[i][0] for i in idx[:center]])
    image1 = tf.convert_to_tensor(image1)
    image2 = np.array([dataset[i][0] for i in idx[center:2 * center]])
    image2 = tf.convert_to_tensor(image2)
    label1 = [dataset[i][1] for i in idx[:center]]
    label1 = tf.convert_to_tensor(label1)
    label2 = [dataset[i][1] for i in idx[center:2 * center]]
    label2 = tf.convert_to_tensor(label2)

    mat = sample_beta_distribution(int(len(dataset) / 2)) / 5

    x_l = tf.reshape(mat, (len(image1), 1, 1, 1))
    y_l = tf.reshape(mat, (len(image1), 1))

    mix_images: tf.Tensor = image1 * x_l + image2 * (1 - x_l)
    mix_labels: tf.Tensor = label1 * y_l + label2 * (1 - y_l)
    mix_images = mix_images.numpy()
    mix_labels = mix_labels.numpy()

    return [(i, l) for i, l in zip(mix_images, mix_labels)]


def get_dataset_from_config(config: TrainConfig) \
        -> Tuple[List[Tuple[np.ndarray, Tuple[float, float]]],
                 List[Tuple[np.ndarray, Tuple[float, float]]],
                 List[Tuple[np.ndarray, Tuple[float, float]]]]:
    train_dataset = merge_dataset_path(config.train_path)

    if config.test_path is None:
        train_dataset, test_dataset = \
            train_test_split(train_dataset, test_size=config.test_path)
    elif config.test_per is None:
        test_dataset = merge_dataset_path(config.test_path)
    else:
        raise Exception("One of test_path or test_per must be specified")

    if config.val_path is None:
        train_dataset, val_dataset = \
            train_test_split(train_dataset, test_size=config.val_path)
    elif config.test_per is None:
        val_dataset = merge_dataset_path(config.val_path)
    else:
        raise Exception("One of val_path or val_per must be specified")

    flipper = album.OneOf([
        album.HorizontalFlip(p=1),
        album.VerticalFlip(p=1),
    ], p=1)
    rotator = album.ShiftScaleRotate(shift_limit=0, rotate_limit=150, scale_limit=0, p=1,
                                     border_mode=1)
    shifter = album.ShiftScaleRotate(shift_limit=0.08, rotate_limit=0, scale_limit=0, p=1,
                                     border_mode=1)

    augments = []
    for img, label in train_dataset:
        if config.flip:
            augments.append((flipper(image=img)['image'], label))
        if config.spin:
            augments.append((rotator(image=img)['image'], label))
        if config.shift:
            augments.append((shifter(image=img)['image'], label))
    if config.mixup:
        augments.extend(mix_up(train_dataset, 0.5))

    train_dataset.extend(augments)
    random.shuffle(train_dataset)

    return train_dataset, val_dataset, test_dataset

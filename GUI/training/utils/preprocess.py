import random
from typing import List, Tuple, Union, Any

import albumentations as album
import cv2
import numpy as np

import tensorflow as tf


def get_index_batch_slices(size: int, batch_size: int):
    slice_list = [i for i in range(size)]
    random.shuffle(slice_list)
    return np.array_split(slice_list, int(size / batch_size))


def sample_beta_distribution(size, concentration_0=0.2, concentration_1=0.2):
    gamma_1_sample = tf.random.gamma(shape=[size], alpha=concentration_0)
    gamma_2_sample = tf.random.gamma(shape=[size], alpha=concentration_1)
    return gamma_1_sample / (gamma_1_sample + gamma_2_sample)


def mix_up(dataset: List[Tuple[np.ndarray, float]], per: float = 0.5):
    idx = [i for i in range(len(dataset))]
    random.shuffle(idx)

    center = int(len(dataset) * per)
    image1 = np.array([dataset[i] for i in idx[:center]])
    image1 = tf.convert_to_tensor(image1)
    image2 = np.array([dataset[i] for i in idx[center:]])
    image2 = tf.convert_to_tensor(image2)
    label1 = [dataset[i] for i in idx[:center]]
    label1 = tf.convert_to_tensor(label1)
    label2 = [dataset[i] for i in idx[center:]]
    label2 = tf.convert_to_tensor(label2)

    mat = sample_beta_distribution(int(len(dataset) / 2)) / 5

    x_l = tf.reshape(mat, (len(image1), 1, 1, 1))
    y_l = tf.reshape(mat, (len(image1), 1))

    mix_images = image1 * x_l + image2 * (1 - x_l)
    mix_labels = label1 * y_l + label2 * (1 - y_l)
    print(mix_images)
    print(mix_labels)
    exit()
    return [(i, l) for i, l in zip(mix_images, mix_labels)]


class Preprocessor:
    def __init__(self) -> None:
        self._flipper = album.OneOf([
            album.HorizontalFlip(p=1),
            album.VerticalFlip(p=1),
        ], p=1)
        self._rotator = album.ShiftScaleRotate(shift_limit=0, rotate_limit=150, scale_limit=0, p=1,
                                               border_mode=1)
        self._shifter = album.ShiftScaleRotate(shift_limit=0.08, rotate_limit=0, scale_limit=0, p=1,
                                               border_mode=1)
        self._gaussian = album.GaussNoise(var_limit=(0.0005, 0.0005), p=1)

    def augment_dataset(self, dataset: List[Tuple[np.ndarray, float]]) -> List[Tuple[np.ndarray, float]]:
        augments = []
        for img, label in dataset:
            augments.append((self._flipper(image=img)['image'], label))
            augments.append((self._rotator(image=img)['image'], label))
            augments.append((self._shifter(image=img)['image'], label))
            augments.append((self._gaussian(image=img)['image'], label))

        augments.extend(mix_up(dataset, 0.5))

        return augments

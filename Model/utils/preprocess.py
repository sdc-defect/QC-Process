import random
from typing import List, Tuple

import albumentations as album
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


def mix_up(images: List, labels: List):
    idx = [i for i in range(len(images))]
    random.shuffle(idx)

    image1 = np.array([images[i] for i in idx[:int(len(images) / 2)]])
    image1 = tf.convert_to_tensor(image1)
    image2 = np.array([images[i] for i in idx[int(len(images) / 2):]])
    image2 = tf.convert_to_tensor(image2)
    label1 = [labels[i] for i in idx[:int(len(labels) / 2)]]
    label1 = tf.convert_to_tensor(label1)
    label2 = [labels[i] for i in idx[int(len(labels) / 2):]]
    label2 = tf.convert_to_tensor(label2)

    mat = sample_beta_distribution(int(len(labels) / 2)) / 5

    x_l = tf.reshape(mat, (len(image1), 1, 1, 1))
    y_l = tf.reshape(mat, (len(image1), 1))

    mix_images = image1 * x_l + image2 * (1 - x_l)
    mix_labels = label1 * y_l + label2 * (1 - y_l)

    return mix_images, mix_labels


class Preprocessor:
    def __init__(self) -> None:
        self._flipper1 = album.OneOf([
            album.HorizontalFlip(p=1),
            album.VerticalFlip(p=1),
        ], p=1)
        self._flipper2 = album.Compose([
            album.HorizontalFlip(p=1),
            album.VerticalFlip(p=1)
        ])
        self._rotator = album.ShiftScaleRotate(shift_limit=0, rotate_limit=150, scale_limit=0, p=1,
                                               border_mode=1)
        self._shifter = album.ShiftScaleRotate(shift_limit=0.08, rotate_limit=0, scale_limit=0, p=1,
                                               border_mode=1)
        self._gaussian = album.GaussNoise(var_limit=(0.0005, 0.0005), p=1)

    def augment_dataset(self, train_img_list: list, train_label_list: list, slices: list = None) -> Tuple[List, List]:
        if slices is not None:
            target_img = [train_img_list[i] for i in slices]
            target_label = [train_label_list[i] for i in slices]
        else:
            target_img = train_img_list
            target_label = train_label_list

        img_list = []
        label_list = []
        for img, lab in zip(target_img, target_label):
            img_list.append(self._flipper1(image=img)['image'])
            label_list.append(lab)

            img_list.append(self._flipper2(image=img)['image'])
            label_list.append(lab)

            img_list.append(self._rotator(image=img)['image'])
            label_list.append(lab)

            img_list.append(self._shifter(image=img)['image'])
            label_list.append(lab)

            img_list.append(self._gaussian(image=img)['image'])
            label_list.append(lab)

        mix_img, mix_labels = mix_up(target_img, target_label)
        for mi, ml in zip(mix_img, mix_labels):
            img_list.append(mi)
            label_list.append(ml)

        return img_list, label_list

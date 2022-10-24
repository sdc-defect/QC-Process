import random
from typing import List

import albumentations as album
import numpy as np


def get_index_batch_slices(size: int, batch_size: int):
    slice_list = [i for i in range(size)]
    random.shuffle(slice_list)
    return np.array_split(slice_list, int(size / batch_size))


def sample_beta_distribution(size, concentration_0=0.2, concentration_1=0.2):
    gamma_1_sample = np.random.gamma(shape=[size], scale=concentration_0)
    gamma_2_sample = np.random.gamma(shape=[size], scale=concentration_1)
    return gamma_1_sample / (gamma_1_sample + gamma_2_sample)


def mix_up(images: List, labels: List):
    image1 = images[:int(len(images) / 2)]
    image2 = images[int(len(images) / 2):]
    label1 = labels[:int(len(labels) / 2)]
    label2 = labels[int(len(labels) / 2):]

    mat = sample_beta_distribution(int(len(labels) / 2))

    mix_images = image1 * mat + image2 * (1 - mat)
    mix_labels = label1 * mat + label2 * (1 - mat)
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

    def augment_dataset(self, train_img_list: list, train_label_list: list, slices: list):
        target_img = [train_img_list[i] for i in slices]
        target_label = [train_label_list[i] for i in slices]

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

        idx = [i for i in range(len(slices))]
        random.shuffle(idx)
        image1 = [target_img[i] for i in idx[:int(len(target_img) / 2)]]
        image2 = [target_img[i] for i in idx[int(len(target_img) / 2):]]
        label1 = [target_label[i] for i in idx[:int(len(target_label) / 2)]]
        label2 = [target_label[i] for i in idx[int(len(target_label) / 2):]]

        mat = sample_beta_distribution(int(len(target_label) / 2))

        mix_img = [img1 * mat + img2 * (1 - mat) for img1, img2 in zip(image1, image2)]
        mix_labels = [lab1 * mat + lab2 * (1 - mat) for lab1, lab2 in zip(label1, label2)]
        for mi, ml in zip(mix_img, mix_labels):
            img_list.append(mi)
            label_list.append(ml)

        return img_list, label_list

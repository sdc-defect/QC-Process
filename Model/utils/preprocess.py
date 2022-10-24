import albumentations as A
import numpy as np

import tensorflow as tf


def sample_beta_distribution(size, concentration_0=0.2, concentration_1=0.2):
    gamma_1_sample = tf.random.gamma(shape=[size], alpha=concentration_1)
    gamma_2_sample = tf.random.gamma(shape=[size], alpha=concentration_0)
    return gamma_1_sample / (gamma_1_sample + gamma_2_sample)


def mixup(image: tf.Tensor, label: tf.Tensor):
    image1, image2 = tf.split(image, num_or_size_splits=2)
    label1, label2 = tf.split(label, num_or_size_splits=2)
    batch_size = tf.shape(image)[0] / 2

    mat = sample_beta_distribution(batch_size)
    x_l = tf.reshape(mat, (batch_size, 1, 1, 1))
    y_l = tf.reshape(mat, (batch_size, 1))

    mix_images = image1 * x_l + image2 * (1 - x_l)
    mix_labels = label1 * y_l + label2 * (1 - y_l)
    return mix_images, mix_labels


class Preprocessor:
    def __init__(self) -> None:
        self._flipper1 = A.OneOf([
            A.HorizontalFlip(p=1),
            A.VerticalFlip(p=1),
        ], p=1)
        self._flipper2 = A.Compose([
            A.HorizontalFlip(p=1),
            A.VerticalFlip(p=1)
        ])
        self._rotator = A.ShiftScaleRotate(shift_limit=0, rotate_limit=150, scale_limit=0, p=1,
                                           border_mode=1)
        self._shifter = A.ShiftScaleRotate(shift_limit=0.08, rotate_limit=0, scale_limit=0, p=1,
                                           border_mode=1)
        self._gaussian = A.GaussNoise(var_limit=(0.0005, 0.0005), p=1)

    def preprocess(self, image: tf.Tensor, label: tf.Tensor):
        b, w, h, c = image.shape

        imgs = image.numpy()
        labels = label.numpy()

        img_pallete = np.empty([b * 6 + int(b / 2), w, h, c])
        label_pallete = np.empty([b * 6 + int(b / 2), 2])
        for i, (img, lab) in enumerate(zip(imgs, labels)):
            img_pallete[i] = img
            img_pallete[i + b * 1] = self._flipper1(image=img)['image']
            img_pallete[i + b * 2] = self._flipper2(image=img)['image']
            img_pallete[i + b * 3] = self._rotator(image=img)['image']
            img_pallete[i + b * 4] = self._shifter(image=img)['image']
            img_pallete[i + b * 5] = self._gaussian(image=img)['image']
            for j in range(6):
                label_pallete[i + b * j] = lab

        mixup_img, mixup_label = mixup(image, label)
        for i, (mi, ml) in enumerate(zip(mixup_img, mixup_label)):
            img_pallete[b * 6 + i] = mi
            label_pallete[b * 6 + i] = ml

        return tf.convert_to_tensor(img_pallete), tf.convert_to_tensor(label_pallete)

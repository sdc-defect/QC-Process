import os

import tensorflow as tf
from glob import glob


def make_example(image, label):
    return tf.train.Example(features=tf.train.Features(feature={
        'image': tf.train.Feature(bytes_list=tf.train.BytesList(value=[image])),
        'label': tf.train.Feature(int64_list=tf.train.Int64List(value=[label]))
    }))


def write_tfrecord(images, labs, filename):
    writer = tf.io.TFRecordWriter(filename)
    for image, label in zip(images, labs):
        ex = make_example(image, label)
        writer.write(ex.SerializeToString())
    writer.close()


def write(folder):
    files = glob(f"{folder}/*/*.jpeg")
    imgs = [open(f, 'rb').read() for f in files]
    labels = [1 if "def" in f else 0 for f in files]
    write_tfrecord(imgs, labels, f"{folder}.tfrecord")


if __name__ == "__main__":
    for name in ["must", "test", "train", "val2"]:
        write(name)

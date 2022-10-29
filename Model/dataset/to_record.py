import os

import tensorflow as tf
from glob import glob


def make_example(image, label, fname):
    return tf.train.Example(features=tf.train.Features(feature={
        'image': tf.train.Feature(bytes_list=tf.train.BytesList(value=[image])),
        'label': tf.train.Feature(int64_list=tf.train.Int64List(value=[label])),
        'fname': tf.train.Feature(bytes_list=tf.train.BytesList(value=[fname]))
    }))


def write_tfrecord(images, labs, fnames, tfname):
    writer = tf.io.TFRecordWriter(tfname)
    for image, label, fname in zip(images, labs, fnames):
        ex = make_example(image, label, str.encode(fname, encoding='utf-8'))
        writer.write(ex.SerializeToString())
    writer.close()


def write(folder):
    files = glob(f"{folder}/*/*.jpeg")
    imgs = [open(f, 'rb').read() for f in files]
    labels = [1 if "def" in f else 0 for f in files]
    fnames = [fname.split("\\")[-1] for fname in files]
    write_tfrecord(imgs, labels, fnames, f"{folder}.tfrecord")


if __name__ == "__main__":
    for name in ["must", "test", "train", "val2"]:
        write(name)

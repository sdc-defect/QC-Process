from typing import List, Tuple

import tensorflow as tf


image_feature_description = {
    'image': tf.io.FixedLenFeature([], tf.string),
    'label': tf.io.FixedLenFeature([], tf.int64),
}


def _parse_image_function(example_proto):
    return tf.io.parse_single_example(example_proto, image_feature_description)


def map_func(target_record):
    img = target_record['image']
    label = target_record['label']
    img = tf.image.decode_image(img)
    img = tf.dtypes.cast(img, tf.float32)
    return img, label


def prep_func(image, label):
    result_image = image / 255
    onehot_label = tf.one_hot(label, depth=2)
    return result_image, onehot_label


def get_dataset(tfile) -> Tuple[List, List]:
    dataset = tf.data.TFRecordDataset(tfile) \
        .map(_parse_image_function, num_parallel_calls=tf.data.experimental.AUTOTUNE) \
        .map(map_func, num_parallel_calls=tf.data.experimental.AUTOTUNE) \
        .map(prep_func, num_parallel_calls=tf.data.experimental.AUTOTUNE) \
        .shuffle(10000)\
        .prefetch(buffer_size=tf.data.experimental.AUTOTUNE)

    imgs = []
    labels = []
    for data in dataset:
        imgs.append(data[0].numpy())
        labels.append(data[1].numpy())

    return imgs, labels

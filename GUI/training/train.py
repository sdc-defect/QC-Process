import logging
from typing import Tuple

import os
import argparse
import dataclasses
import datetime
import json
import math


import tensorflow as tf
from keras.optimizers.schedules.learning_rate_schedule import CosineDecayRestarts
from keras.optimizers.optimizer_v2.adam import Adam
from keras.losses import CategoricalCrossentropy
from keras.utils import Progbar

import utils
from utils.dataset import get_dataset_from_config
from utils.model import MyModel
from utils.record import MyRecorder


@tf.function(reduce_retracing=True)
def train(images: tf.Tensor, labels: tf.Tensor,
          module, loss_fn, opt) -> Tuple[tf.Tensor, tf.Tensor]:
    with tf.GradientTape() as tape:
        probs: tf.Tensor = module(images, training=True)
        losses: tf.Tensor = loss_fn(labels, probs)
    gradients: list = tape.gradient(losses, module.trainable_variables)
    opt.apply_gradients(zip(gradients, module.trainable_variables))

    return losses, probs


@tf.function(reduce_retracing=True)
def test(images: tf.Tensor, labels: tf.Tensor,
         module, loss_fn) -> Tuple[tf.Tensor, tf.Tensor]:
    probs: tf.Tensor = module(images, training=False)
    losses: tf.Tensor = loss_fn(labels, probs)

    return losses, probs


# config.json = TrainConfig(save_path=".", train_path=["temp/def", "temp/ok"],
#                      test_path=None, test_per=0.5, val_path=None, val_per=0.1,
#                      flip=True, spin=True, shift=True, mixup=True,
#                      epoch=50, batch_size=16, lr=0.001, decay=1000)
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--json',
                        required=True)
    args = parser.parse_args()
    config = utils.load_config_json(args.json)

    now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    save_path = os.path.join(config.save_path, now)
    utils.make_folder(save_path)
    logging.basicConfig(filename=os.path.join(save_path, "base.log"))
    logger = utils.get_logger(save_path, "main")
    train_logger = utils.get_logger(save_path, "train")
    val_logger = utils.get_logger(save_path, "val")

    logger.info(f'config - {json.dumps(dataclasses.asdict(config))}')

    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            logical_gpus = tf.config.list_logical_devices('GPU')
            # print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
            logger.info(f'config - {len(gpus)}, Physical GPUs, {len(logical_gpus)}, Logical GPUs')
        except RuntimeError as e:
            # print(e)
            logger.error(f'config - {e}')

    model = MyModel()
    loss_func = CategoricalCrossentropy()
    schedular = CosineDecayRestarts(config.lr, config.decay)
    optimizer = Adam(schedular)

    train_dataset, val_dataset, test_dataset = get_dataset_from_config(config)
    recorder = MyRecorder()

    # Train
    train_batch_size = math.ceil(len(train_dataset) / config.batch_size)
    val_batch_size = math.ceil(len(val_dataset) / config.batch_size)
    for e in range(1, config.epoch + 1):
        recorder.reset()

        # Train
        progbar_train = Progbar(train_batch_size, width=50,
                                stateful_metrics=['loss', 'accuracy', 'recall', 'precision', 'f1'])
        progbar_train.update(0, values=[('loss', 0), ('accuracy', 0), ('recall', 0), ('precision', 0), ('f1', 0)])
        for b, (img, label) in enumerate(utils.batch(train_dataset, config.batch_size)):
            loss, prob = train(tf.convert_to_tensor(img), tf.convert_to_tensor(label), model, loss_func, optimizer)
            recorder.train.record(loss, prob, label)
            result = {'epoch': f'{e}/{config.epoch}', 'batch': f'{b + 1}/{train_batch_size}',
                      'loss': recorder.train.get_mean_loss(), 'accuracy': recorder.train.get_accuracy(),
                      'recall': recorder.train.get_recall(), 'precision': recorder.train.get_precision(),
                      'f1': recorder.train.get_f1_score()}
            progbar_train.update(b + 1, values=[('loss', result['loss']),
                                                ('accuracy', result['accuracy']),
                                                ('recall', result['recall']),
                                                ('precision', result['precision']),
                                                ('f1', result['f1'])])
            train_logger.info(json.dumps(result, cls=utils.MyEncoder))
            # print(json.dumps(result, cls=utils.MyEncoder))

        # Validate
        progbar_val = Progbar(val_batch_size, width=50,
                              stateful_metrics=['loss', 'accuracy', 'recall', 'precision', 'f1'])
        progbar_val.update(0, values=[('loss', 0), ('accuracy', 0), ('recall', 0), ('precision', 0), ('f1', 0)])
        for b, (img, label) in enumerate(utils.batch(val_dataset, config.batch_size)):
            loss, prob = test(tf.convert_to_tensor(img), tf.convert_to_tensor(label), model, loss_func)
            recorder.val.record(loss, prob, label)
            result = {'epoch': f'{e}/{config.epoch}', 'batch': f'{b + 1}/{val_batch_size}',
                      'loss': recorder.val.get_mean_loss(), 'accuracy': recorder.val.get_accuracy(),
                      'recall': recorder.val.get_recall(), 'precision': recorder.val.get_precision(),
                      'f1': recorder.val.get_f1_score()}
            progbar_val.update(b + 1, values=[('loss', result['loss']),
                                                ('accuracy', result['accuracy']),
                                                ('recall', result['recall']),
                                                ('precision', result['precision']),
                                                ('f1', result['f1'])])
            val_logger.info(json.dumps(result, cls=utils.MyEncoder))
            # print(json.dumps(result, cls=utils.MyEncoder))

        # Save
        if recorder.check_best_score():
            # print("New Best Model!!! model will be saved in", os.path.abspath(os.path.join(save_path, "model.onnx")))
            utils.model_to_onnx(model, os.path.join(save_path, "model.onnx"))

    # Test
    runtime = utils.load_onnx(os.path.join(save_path, "model.onnx"))
    test_batch_size = math.ceil(len(test_dataset) / config.batch_size)
    for b, (img, label) in enumerate(utils.batch(test_dataset, config.batch_size)):
        prob = runtime.runtime.run(None, {'input_1': img})[0]
        loss = loss_func(label, prob)
        recorder.test.record(loss, prob, label)
    result = {'loss': recorder.test.get_mean_loss(), 'accuracy': recorder.test.get_accuracy(),
              'recall': recorder.test.get_recall(), 'precision': recorder.test.get_precision(),
              'f1': recorder.test.get_f1_score()}
    result_str = json.dumps(result, cls=utils.MyEncoder)
    # print(f"Test Result - {result_str}")
    logger.info(f'test - {json.dumps(result, cls=utils.MyEncoder)}')

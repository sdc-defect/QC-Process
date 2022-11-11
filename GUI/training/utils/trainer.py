import math
import multiprocessing as mp
import os.path
import time
from threading import Thread
from typing import Union, Tuple

import numpy as np
import tensorflow as tf
from keras.optimizers.schedules.learning_rate_schedule import CosineDecayRestarts
from keras.optimizers.optimizer_v2.adam import Adam
from keras.losses import CategoricalCrossentropy

from utils import Singleton
from utils.util import batch, model_to_onnx, load_onnx
from utils.dataset import get_dataset_from_config
from utils.dto import TrainConfig, TrainResult
from utils.model import MyModel
from utils.record import MyRecorder


@tf.function
def train(images: tf.Tensor, labels: tf.Tensor,
          model, loss_func, optimizer) -> Tuple[tf.Tensor, tf.Tensor]:
    with tf.GradientTape() as tape:
        prob: tf.Tensor = model(images, training=True)
        loss: tf.Tensor = loss_func(labels, prob)
    gradients: list = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))

    return loss, prob


@tf.function
def test(images: tf.Tensor, labels: tf.Tensor,
         model, loss_func) -> Tuple[tf.Tensor, tf.Tensor]:
    prob: tf.Tensor = model(images, training=False)
    loss: tf.Tensor = loss_func(labels, prob)

    return loss, prob


class Trainer:
    def __init__(self, queue: mp.Queue, config: TrainConfig):
        self.queue = queue
        self.config = config

        self.model = MyModel()
        self.loss_func = CategoricalCrossentropy()
        self.schedular = CosineDecayRestarts(config.lr, config.decay)
        self.optimizer = Adam(self.schedular)

        self.train_dataset, self.val_dataset, self.test_dataset = get_dataset_from_config(config)
        self.recorder = MyRecorder()


class Manager(metaclass=Singleton):
    def __init__(self):
        self.queue = mp.Queue()
        self._thread: Union[Thread, None] = None
        self._trainer: Union[Trainer, None] = None

    def build_trainer(self, config: TrainConfig) -> None:
        del self._trainer
        self._trainer = Trainer(self.queue, config)

    def check(self) -> bool:
        if self._thread is None:
            return False
        else:
            if self._thread.is_alive():
                return True
            else:
                self._thread = None
                return False

    def start(self, is_train: bool) -> None:
        if self.check():
            raise RuntimeError("Process already started")

        if is_train:
            self._thread = Thread(target=train_process, args=(self._trainer,), daemon=True)
        else:
            self._thread = Thread(target=test_process, args=(self._trainer,), daemon=True)
        self._thread.start()


def train_process(trainer: Trainer) -> None:
    queue = trainer.queue
    train_dataset, val_dataset = trainer.train_dataset, trainer.val_dataset
    model, loss_func, optimizer = trainer.model, trainer.loss_func, trainer.optimizer
    epoch, batch_size = trainer.config.epoch, trainer.config.batch_size
    recorder = trainer.recorder

    # Train
    train_batch_size = math.ceil(len(train_dataset) / batch_size)
    val_batch_size = math.ceil(len(val_dataset) / batch_size)
    for e in range(1, epoch + 1):
        recorder.reset()

        # Train
        for b, (img, label) in enumerate(batch(train_dataset, batch_size)):
            loss, prob = train(img, label, model, loss_func, optimizer)
            recorder.train.record(loss, prob, label)
            queue.put(TrainResult(confusionmatrix=recorder.train.get_confusion_matrix(), loss=float(loss.numpy()),
                                  header="train", epoch=f"{e}/{epoch}", batch=f"{b + 1}/{train_batch_size}"))

        # Validate
        for b, (img, label) in enumerate(batch(val_dataset, batch_size)):
            loss, prob = test(img, label, model, loss_func)
            recorder.val.record(loss, prob, label)
            queue.put(TrainResult(confusionmatrix=recorder.val.get_confusion_matrix(), loss=float(loss.numpy()),
                                  header="val", epoch=f"{e}/{epoch}", batch=f"{b + 1}/{val_batch_size}"))

        # Save
        if recorder.check_best_score():
            model_to_onnx(model, os.path.join(trainer.config.save_path, "model.onnx"))


def test_process(trainer: Trainer) -> None:
    queue = trainer.queue
    test_dataset = trainer.test_dataset
    runtime = load_onnx(os.path.join(trainer.config.save_path, "model.onnx"))
    loss_func = trainer.loss_func
    batch_size = trainer.config.batch_size
    recorder = trainer.recorder

    # Test
    for b, (img, label) in enumerate(batch(test_dataset, batch_size)):
        prob = runtime.runtime.run(None, {'input_1': img.numpy()})[0]
        loss = loss_func(label, prob)
        recorder.test.record(loss, prob, label)

    queue.put("hi")


if __name__ == "__main__":
    cconfig = TrainConfig(save_path="../", train_path=["../temp/def", "../temp/ok"],
                          test_path=0.5, val_path=0.1,
                          flip=True, spin=True, shift=True, mixup=True)

    Manager().build_trainer(cconfig)
    Manager().start(is_train=True)
    # Manager().start(is_train=False)
    while True:
        time.sleep(0.5)
        if Manager().queue.empty():
            continue
        data: TrainResult = Manager().queue.get()
        print(data)

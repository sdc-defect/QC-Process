import numpy as np

import tensorflow as tf
from keras.optimizers.schedules.learning_rate_schedule import CosineDecayRestarts
from keras.optimizers.optimizer_v2.adam import Adam
from keras.losses import CategoricalCrossentropy
from keras.metrics import Mean

from utils.matrix import Matrix


@tf.function
def inference(model, images) -> tf.Tensor:
    return model(images, training=False)


class MyTester(Matrix):
    def __init__(self, model) -> None:
        super().__init__()
        self._model = model
        self._loss_func = CategoricalCrossentropy()
        self._loss = Mean(name='Loss')

    @tf.function
    def test(self, images, labels) -> None:
        preds: tf.Tensor = self._model(images, training=False)
        loss: tf.Tensor = self._loss_func(labels, preds)

        self._loss.update_state(loss)
        self.update_matrix(tf.cast(tf.argmax(labels, axis=1), dtype=tf.int64),
                           tf.cast(tf.argmax(preds, axis=1), dtype=tf.int64))

    def get_loss(self) -> np.float32:
        return self._loss.result().numpy()


class MyTrainer(MyTester):
    def __init__(self, model, init_lr: float = 0.001, decay_steps: int = 1000) -> None:
        super().__init__(model=model)
        self._schedular = CosineDecayRestarts(init_lr, decay_steps)
        self._optimizer = Adam(self._schedular)

    @tf.function
    def train(self, images, labels) -> None:
        with tf.GradientTape() as tape:
            preds: tf.Tensor = self._model(images, training=True)
            loss: tf.Tensor = self._loss_func(labels, preds)
        gradients: list = tape.gradient(loss, self._model.trainable_variables)
        self._optimizer.apply_gradients(zip(gradients, self._model.trainable_variables))

        self._loss.update_state(loss)
        self.update_matrix(tf.cast(tf.argmax(labels, axis=1), dtype=tf.int64),
                           tf.cast(tf.argmax(preds, axis=1), dtype=tf.int64))


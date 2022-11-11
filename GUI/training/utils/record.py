from typing import List, Dict, Union

import numpy as np
from dataclasses import dataclass

import tensorflow as tf
from keras.metrics import TruePositives, TrueNegatives, FalsePositives, FalseNegatives
from keras.metrics import Mean


@dataclass
class ConfusionMatrix:
    tp: int
    tn: int
    fp: int
    fn: int


class Record:
    def __init__(self) -> None:
        self._tp = TruePositives()
        self._tn = TrueNegatives()
        self._fp = FalsePositives()
        self._fn = FalseNegatives()
        self._list = {"tp": self._tp, "tn": self._tn, "fp": self._fp, "fn": self._fn}

        self._loss = Mean(name='Loss')

    def record(self, loss: tf.Tensor, prob: tf.Tensor, label: tf.Tensor):
        self._loss.update_state(loss)
        self._update_matrix(tf.cast(tf.argmax(label, axis=1), dtype=tf.int64),
                            tf.cast(tf.argmax(prob, axis=1), dtype=tf.int64))

    def get_mean_loss(self):
        return self._loss.result().numpy()

    def get_confusion_matrix(self) -> ConfusionMatrix:
        tp = int(self._tp.result().numpy())
        tn = int(self._tn.result().numpy())
        fp = int(self._fp.result().numpy())
        fn = int(self._fn.result().numpy())

        return ConfusionMatrix(tp=tp, tn=tn, fp=fp, fn=fn)

    def _update_matrix(self, labels, preds) -> None:
        for metric in self._list.values():
            metric.update_state(labels, preds)

    def reset(self) -> None:
        for metric in self._list.values():
            metric.reset_states()

    def get_accuracy(self) -> float:
        mat = self.get_confusion_matrix()
        acc = (mat.tp + mat.tn) / (mat.tp + mat.tn + mat.fp + mat.fn) if (mat.tp + mat.tn + mat.fp + mat.fn) != 0 else 0.
        return acc

    def get_recall(self) -> float:
        mat = self.get_confusion_matrix()
        recall = mat.tp / (mat.tp + mat.fn) if (mat.tp + mat.fn) != 0 else 0.
        return recall

    def get_ok_recall(self) -> float:
        mat = self.get_confusion_matrix()
        ok_recall = mat.tn / (mat.tn + mat.fp) if (mat.tn + mat.fp) != 0 else 0.
        return ok_recall

    def get_precision(self) -> float:
        mat = self.get_confusion_matrix()
        precision = mat.tp / (mat.tp + mat.fp) if (mat.tp + mat.fp) != 0 else 0.
        return precision

    def get_ok_precision(self) -> float:
        mat = self.get_confusion_matrix()
        ok_precision = mat.tn / (mat.tn + mat.fn) if (mat.tn + mat.fn) != 0 else 0.
        return ok_precision

    def get_f1_score(self) -> float:
        recall = self.get_recall()
        precision = self.get_precision()
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) != 0 else 0.
        return f1

    def get_ok_f1_score(self) -> float:
        ok_recall = self.get_ok_recall()
        ok_precision = self.get_ok_precision()
        ok_f1 = (2 * ok_precision * ok_recall) / (ok_precision + ok_recall) if (ok_precision + ok_recall) != 0 else 0.
        return ok_f1


class MyRecorder:
    def __init__(self) -> None:
        self.train = Record()
        self.val = Record()
        self.test = Record()

        self._best_loss = float('inf')
        self._best_score = float('-inf')

    def reset(self) -> None:
        self.train.reset()
        self.val.reset()

    def check_best_score(self) -> bool:
        score = self.val.get_accuracy()
        loss = self.val.get_mean_loss()
        if score >= self._best_score and loss >= self._best_loss:
            self._best_score = score
            self._best_loss = loss
            return True

        return False


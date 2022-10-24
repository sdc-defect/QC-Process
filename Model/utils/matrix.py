import numpy as np
from dataclasses import dataclass

from keras.metrics import TruePositives, TrueNegatives, FalsePositives, FalseNegatives


@dataclass
class ConfusionMatrix:
    tp: int
    tn: int
    fp: int
    fn: int


class Matrix:
    def __init__(self) -> None:
        self._tp = TruePositives()
        self._tn = TrueNegatives()
        self._fp = FalsePositives()
        self._fn = FalseNegatives()

        self._list = {"tp": self._tp, "tn": self._tn, "fp": self._fp, "fn": self._fn}

    def get_confusion_matrix(self) -> ConfusionMatrix:
        tp = int(self._tp.result().numpy())
        tn = int(self._tn.result().numpy())
        fp = int(self._fp.result().numpy())
        fn = int(self._fn.result().numpy())

        return ConfusionMatrix(tp=tp, tn=tn, fp=fp, fn=fn)

    def update_matrix(self, labels, preds) -> None:
        for metric in self._list.values():
            metric.update_state(labels, preds)

    def reset_matrix(self) -> None:
        for metric in self._list.values():
            metric.reset_states()

    def get_accuracy(self) -> np.float32:
        mat = self.get_confusion_matrix()
        acc = (mat.tp + mat.tn) / (mat.tp + mat.tn + mat.fp + mat.fn) if (mat.tp + mat.tn + mat.fp + mat.fn) != 0 else 0
        return acc

    def get_recall(self) -> np.float32:
        mat = self.get_confusion_matrix()
        recall = mat.tp / (mat.tp + mat.fn) if (mat.tp + mat.fn) != 0 else 0
        return recall

    def get_ok_recall(self) -> np.float32:
        mat = self.get_confusion_matrix()
        ok_recall = mat.fn / (mat.fn + mat.tn) if (mat.fn + mat.tn) != 0 else 0
        return ok_recall

    def get_precision(self) -> np.float32:
        mat = self.get_confusion_matrix()
        precision = mat.tp / (mat.tp + mat.fp) if (mat.tp + mat.fp) != 0 else 0
        return precision

    def get_ok_precision(self) -> np.float32:
        mat = self.get_confusion_matrix()
        ok_precision = mat.tn / (mat.tn + mat.fn) if (mat.tn + mat.fn) != 0 else 0
        return ok_precision

    def get_f1_score(self) -> np.float64:
        recall = self.get_recall()
        precision = self.get_precision()
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) != 0 else 0
        return f1

    def get_ok_f1_score(self) -> np.float64:
        ok_recall = self.get_ok_recall()
        ok_precision = self.get_ok_precision()
        ok_f1 = (2 * ok_precision * ok_recall) / (ok_precision + ok_recall) if (ok_precision + ok_recall) != 0 else 0
        return ok_f1

import os
from datetime import datetime

import pandas as pd

import tensorflow as tf

from utils.trainer import MyTrainer, MyTester


class Saver:
    def __init__(self, folder, save) -> None:
        self.dir = folder
        self.save = save
        self.save_dir = os.path.join(folder, save)
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir, exist_ok=True)

        self._columns = ["epoch", "timestamp",
                         "train_loss", "train_accuracy", "train_recall", "train_f1", "train_matrix(tp, fn, fp, tn)",
                         "val_loss", "train_accuracy", "val_recall", "val_f1", "val_matrix(tp, fn, fp, tn)", "val2"]
        self._log = pd.DataFrame([], columns=self._columns)

        self._best_val_recall = float("-inf")
        self._best_val_ok_recall = float("-inf")

    def save_train_log(self, fold, epoch, trainer: MyTrainer, validator: MyTester, val2_cnt: int):
        tm = trainer.get_confusion_matrix()
        tl = trainer.get_loss()
        ta = trainer.get_accuracy()
        tr = trainer.get_recall()
        tf1 = trainer.get_f1_score()
        tm_str = f"{tm.tp}-{tm.fn}-{tm.fp}-{tm.tn}"

        vm = validator.get_confusion_matrix()
        vl = validator.get_loss()
        va = validator.get_accuracy()
        vr = validator.get_recall()
        vf1 = validator.get_f1_score()
        vm_str = f"{vm.tp}-{vm.fn}-{vm.fp}-{vm.tn}"

        data = [epoch, datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                tl, ta, tr, tf1, tm_str,
                vl, va, vr, vf1, vm_str, val2_cnt]

        new_data = pd.DataFrame([data], columns=self._columns)
        self._log = pd.concat([self._log, new_data])
        self._log.to_csv(os.path.join(self.save_dir, f"{fold}_log.csv"), index=False)

    def save_test_log(self, tester: MyTester):
        tm = tester.get_confusion_matrix()
        tm_str = f"{tm.tp}-{tm.fn}-{tm.fp}-{tm.tn}"
        data = [tester.get_loss(), tester.get_accuracy(), tester.get_recall(), tester.get_f1_score(), tm_str]
        test_log = pd.DataFrame([data],
                                columns=["loss", "accuracy", "recall", "f1", "matrix(tp, fn, fp, tn)"])
        test_log.to_csv(os.path.join(self.save_dir, f"test_log.csv"), index=False)

    def save_best_model(self, model, new_recall, new_ok_recall) -> None:
        if self._best_val_recall <= new_recall and self._best_val_ok_recall <= new_ok_recall:
            self._best_val_recall = new_recall
            self._best_val_ok_recall = new_ok_recall
            print("saving...")
            tf.saved_model.save(model, self.save_dir)

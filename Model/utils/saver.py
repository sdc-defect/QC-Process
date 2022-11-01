from typing import List, Dict, Union

import os
import time
import subprocess
import json
from datetime import datetime

import numpy as np
import pandas as pd
import tensorflow as tf
import onnx
import onnx.numpy_helper as numpy_helper

import utils
from utils.trainer import MyTrainer, MyTester
from utils.matrix import Must, convert_must_list_to_dict, count_def_in_must_list


def save_test_log(path: str, tester: MyTester, musts: List[Must], test_logs: List[Dict]):
    tm = tester.get_confusion_matrix()
    data = {"loss": float(tester.get_loss()), "accuracy": tester.get_accuracy(), "recall": tester.get_recall(),
            "f1": tester.get_f1_score(), "ok_recall": tester.get_ok_recall(), "ok_f1": tester.get_ok_f1_score(),
            "tp": tm.tp, "fn": tm.fn, "fp": tm.fp, "tn": tm.tn,
            'must_cnt': count_def_in_must_list(musts), 'must': convert_must_list_to_dict(musts), 'result': test_logs}

    with open(os.path.join(path, "test_log.json"), "w") as f:
        json.dump(data, f)


class Saver:
    def __init__(self, user, save) -> None:
        self.save_dir = os.path.join("train", user, save)
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir, exist_ok=True)

        self._columns = ["epoch", "timestamp",
                         "train_loss", "train_accuracy", "train_recall", "train_f1", "train_matrix(tp, fn, fp, tn)",
                         "val_loss", "val_accuracy", "val_recall", "val_f1", "val_matrix(tp, fn, fp, tn)", "val2"]
        self._log = pd.DataFrame([], columns=self._columns)
        self._must_log = dict()

        self._best_val_recall = float("-inf")
        self._best_val_ok_recall = float("-inf")
        self._best_loss = float("inf")

    def clear(self):
        self._log = pd.DataFrame([], columns=self._columns)

    def save_train_log(self, epoch, trainer: MyTrainer, validator: MyTester, val2_cnt: int,
                       musts: List[Must]):
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
        self._log.to_csv(os.path.join(self.save_dir, f"train_log.csv"), index=False)
        self._must_log[epoch] = convert_must_list_to_dict(musts)
        with open(os.path.join(self.save_dir, "train_must_log.json"), 'w') as f:
            json.dump(self._must_log, f)

    def save_best_model(self, epoch, model, new_recall, new_ok_recall, new_loss) -> None:
        if self._best_val_recall <= new_recall and self._best_val_ok_recall <= new_ok_recall \
                and self._best_loss > new_loss:
            self._best_val_recall = new_recall
            self._best_val_ok_recall = new_ok_recall
            self._best_loss = new_loss
            print("saving...")
            with open(os.path.join(self.save_dir, f"best_model.txt"), "w") as note:
                note.write(f"{epoch} epoch")
            tf.saved_model.save(model, self.save_dir)


class Convertor:
    def __int__(self, model_path: str, onnx_name: str = 'model.onnx', modified_name: str = 'modified.onnx'):
        self._logger = utils.get_logger(__name__)
        self._saved_model = model_path
        self._folder = os.path.join(self._saved_model, "onnx")
        self._check_folder()
        self._onnx_name = onnx_name
        self._modified_name = modified_name

    def _check_folder(self):
        if not os.path.exists(self._folder):
            os.mkdir(self._folder)

    def save(self):
        try:
            self._saved_model_to_onnx()
            self._modify_onnx()
        except Exception as e:
            self._logger.error(f"Failed to convert saved model to onnx!!! - {e}")

    def _saved_model_to_onnx(self):
        st = time.time()
        subprocess.run(args=["python", "-m", "tf2onnx.convert", "--tag", "serve",
                             "--saved-model", self._saved_model, "--output",
                             os.path.join(self._folder, self._onnx_name)],
                       shell=True, encoding='utf-8')
        self._logger.info(f"Convert Tensorflow Model to ONNX {time.time() - st}")

    def _modify_onnx(self):
        st = time.time()
        model = onnx.load(os.path.join(self._folder, "model.onnx"))
        last_layer = onnx.shape_inference.infer_shapes(model).graph.value_info[-5]
        dense = numpy_helper.to_array(model.graph.initializer[-3])
        model.graph.output.append(last_layer)

        onnx.checker.check_model(model)
        onnx.save_model(model, os.path.join(self._folder, "modified.onnx"))
        np.save(os.path.join(self._folder, "dense.npy"), dense)
        self._logger.info(f"Modify ONNX {time.time() - st}")


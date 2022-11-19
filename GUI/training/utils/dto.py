import datetime
import os
from dataclasses import dataclass
from typing import Union, List, Optional

import onnxruntime
import numpy as np


@dataclass
class ConfusionMatrix:
    tp: int
    tn: int
    fp: int
    fn: int


@dataclass
class ONNXRuntime:
    runtime: onnxruntime.InferenceSession
    dense: np.ndarray


@dataclass
class TrainConfig:
    save_path: str
    train_path: List[str]

    test_path: Optional[List[str]]
    test_per: Optional[float]

    val_path: Optional[List[str]]
    val_per: Optional[float]

    flip: bool = False
    spin: bool = False
    shift: bool = False
    mixup: bool = False

    epoch: int = 50
    batch_size: int = 16
    lr: float = 0.001
    decay: int = 1000

    def process(self):
        if self.save_path is None:
            raise Exception("save_path must be specified")
        if self.train_path is None:
            raise Exception("train_path must be specified")
        if self.test_path is None and self.test_per is None:
            raise Exception("One of test_path and test_per must be specified")

        if self.val_path is None and self.val_per is None:
            raise Exception("One of val_path and val_per must be specified")

        now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        save_path = os.path.abspath(os.path.join(self.save_path, now))

        self.train_path = [os.path.abspath(p) for p in self.train_path]
        if isinstance(self.test_path, list):
            self.test_path = [os.path.abspath(p) for p in self.test_path]
        if isinstance(self.val_path, list):
            self.val_path = [os.path.abspath(p) for p in self.val_path]

        return save_path

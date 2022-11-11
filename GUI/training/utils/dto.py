from dataclasses import dataclass
from typing import Union, List

import onnxruntime
import numpy as np

from utils.record import Record, ConfusionMatrix


@dataclass
class ONNXRuntime:
    runtime: onnxruntime.InferenceSession
    dense: np.ndarray


@dataclass
class TrainConfig:
    save_path: str
    train_path: List
    test_path: Union[List, float]
    val_path: Union[List, float]

    flip: bool = False
    spin: bool = False
    shift: bool = False
    mixup: bool = False

    epoch: int = 50
    batch_size: int = 16
    lr: float = 0.001
    decay: int = 1000


@dataclass
class TestConfig:
    save_path: str
    test_path: Union[List, float]


@dataclass
class TrainResult:
    confusionmatrix: ConfusionMatrix
    loss: float = 0.523234
    header: str = "train/val/test"
    epoch: str = "1/50"
    batch: str = "3/20"


@dataclass
class TestResult:
    record: Record



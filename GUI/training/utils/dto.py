from dataclasses import dataclass
from typing import Union, List

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

    test_path: Union[List[str], None]
    test_per: Union[float, None]

    val_path: Union[List[str], None]
    val_per: Union[float, None]

    flip: bool = False
    spin: bool = False
    shift: bool = False
    mixup: bool = False

    epoch: int = 50
    batch_size: int = 16
    lr: float = 0.001
    decay: int = 1000

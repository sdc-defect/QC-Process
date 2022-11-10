from dataclasses import dataclass
from typing import Union, List

from utils.matrix import Matrix


@dataclass
class TrainConfig:
    save_path: str
    train_path: List

    test_path: Union[List, float]

    val_path: Union[List, float]

    flip: bool = False
    spin: bool = False
    swift: bool = False
    mixup: bool = False

    epoch: int = 50
    batch_size: int = 16
    lr: float = 0.001
    decay: int = 1000


@dataclass
class TrainResult:
    epoch: int
    matrix: Matrix

    train_loss: float
    val_loss: float


@dataclass
class TestResult:
    matrix: Matrix
    test_loss: float

import dataclasses
import json
import os
from typing import Generator, Tuple, List

import numpy as np

from utils.dto import TrainConfig, ONNXRuntime


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def make_folder(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def config_to_json(data: TrainConfig, path: str):
    if not isinstance(data, TrainConfig):
        raise TypeError("input data type must be TrainConfig")
    with open(path, "w") as file:
        json.dump(dataclasses.asdict(data), file)


def load_config_json(path: str):
    name, ext = os.path.splitext(path)
    if len(ext) == 0:
        ext = '.json'
    elif ext is not 'json':
        raise TypeError("config file must be json")
    return TrainConfig(**json.load(open(name + ext, 'r')))


def batch(data, batch_size: int = 1) \
        -> Generator[Tuple[np.ndarray, np.ndarray], Tuple[List[Tuple[np.ndarray, Tuple[float, float]]], int], None]:
    size = len(data)
    for idx in range(0, size, batch_size):
        split = data[idx:min(idx + batch_size, size)]
        yield [s[0] for s in split], [s[1] for s in split]

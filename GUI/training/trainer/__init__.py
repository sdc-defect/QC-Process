import multiprocessing as mp
import random
from typing import Union, Dict, List, Tuple

from glob import glob
import cv2
import numpy as np

from sklearn.model_selection import train_test_split
import tensorflow as tf

from utils.dto import TrainConfig
from utils.preprocess import Preprocessor


class Manager:
    def __init__(self, queue: mp.Queue):
        self._queue = queue
        self._config: Union[TrainConfig, None] = None
        self._process: Union[mp.Process, None] = None

    def update_config(self, config: TrainConfig) -> None:
        self._config = config

    def check(self) -> bool:
        if self._process is None:
            return False
        else:
            if self._process.is_alive():
                return True
            else:
                return False

    def trainer(self) -> None:
        if self.check():
            raise RuntimeError("Process already started")

        self._process = mp.Process(target=train, args=(self._config,), daemon=True)
        self._process.run()

    def test(self):
        if self.check():
            raise RuntimeError("Process already started")

        self._process = mp.Process(target=train, args=(self._config,), daemon=True)
        self._process.run()


def train(config: TrainConfig) -> None:
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            logical_gpus = tf.config.list_logical_devices('GPU')
            print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
        except RuntimeError as e:
            print(e)

    # Load Dataset
    train_img, train_label, val_img, val_label, test_img, test_label = get_dataset_path(config)

    # Split Dataset
    # Load Model
    # Train
    # Save


def get_dataset_path(config: TrainConfig) -> Tuple:
    print("start")
    train_dataset = merge_dataset_path(config.train_path)
    print("train")
    if isinstance(config.test_path, List):
        test_dataset = merge_dataset_path(config.test_path)
    else:
        train_dataset, test_dataset = \
            train_test_split(train_dataset, test_size=config.test_path)
    print("test")
    if isinstance(config.val_path, List):
        val_dataset = merge_dataset_path(config.val_path)
    else:
        train_dataset, val_dataset = \
            train_test_split(train_dataset, test_size=config.val_path)
    print("val")
    # pre = Preprocessor()
    # pre.augment_dataset(train_dataset)

    return train_dataset, val_dataset, test_dataset


def merge_dataset_path(path: List) -> List[Tuple[np.ndarray, float]]:
    if not isinstance(path, list) and len(path) != 2:
        raise Exception("Wrong path input, input path must be List and length to be 2")

    paths = []
    labels = []

    paths0 = glob(path[0] + "*")
    paths.extend(paths0)
    labels.extend([0. for _ in range(len(paths0))])

    paths1 = glob(path[1] + "*")
    paths.extend(paths1)
    labels.extend([1. for _ in range(len(paths1))])

    merged = [(get_path_to_processed_img(p), l) for p, l in zip(paths, labels)]
    random.shuffle(merged)

    return merged


def get_path_to_processed_img(path: str) -> np.ndarray:
    return cv2.normalize(cv2.imread(path), None, 0, 1, cv2.NORM_MINMAX, cv2.CV_32F)


if __name__ == "__main__":
    cconfig = TrainConfig(save_path=".", train_path=["E:/dataset/def_front/", "E:/dataset/ok_front"],
                          test_path=0.1, val_path=0.1)
    print(cconfig)
    ttrain_dataset, tval_dataset, ttest_dataset = get_dataset_path(cconfig)

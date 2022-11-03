from typing import Tuple

import os

import numpy as np
import onnx
import psutil
import logging

import onnxruntime
import onnx.numpy_helper as numpy_helper

from utils.dto import ONNXRuntime


def check_folder(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)


def print_mem_use():
    psutil.cpu_percent(percpu=False)
    pid = os.getpid()
    ps = psutil.Process(pid)
    mem = round(ps.memory_info()[0] / (1024 * 1024), 2)
    print(f"{mem}MB")


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # file_handler = logging.FileHandler('my.log')
    # file_handler.setFormatter(formatter)
    # logger.addHandler(file_handler)

    return logger


def load_onnx(path: str, gpu: bool = True) -> ONNXRuntime:
    try:
        model = onnx.load_model(path)
        runtime = onnxruntime.InferenceSession(path, providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])

        for w in reversed(model.graph.initializer):
            dense = numpy_helper.to_array(w)
            if dense.ndim == 2 and dense.shape[1] == 2:
                return ONNXRuntime(runtime=runtime, dense=dense)
    except FileNotFoundError as e:
        print(e)


def merge_two_imgs(img1: np.ndarray, img2: np.ndarray, per_1: float = 0.5, per_2: float = 0.3) -> np.float64:
    merged = img1 * per_1 + img2 * per_2
    merged -= np.min(merged)
    merged /= np.max(merged)

    return merged

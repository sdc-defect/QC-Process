from typing import List

import psutil
import os

import numpy as np
import tensorflow as tf

import logging


def print_mem_use():
    tmp = psutil.cpu_percent(percpu=False)
    pid = os.getpid()
    ps = psutil.Process(pid)
    mem = round(ps.memory_info()[0] / (1024 * 1024), 2)
    print(f"{mem}MB")


def list_index_to_tensor(data_list: List, slice_list: List):
    return tf.convert_to_tensor(np.array([data_list[i] for i in slice_list]))


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

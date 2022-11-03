import psutil
import os

import logging


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

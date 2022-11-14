from typing import Generator, Tuple, List, Any

import os
import logging
import json
import dataclasses

import numpy as np

import tf2onnx
import onnx
import onnxruntime
from onnx import shape_inference, checker, save_model, numpy_helper as numpy_helper

from utils.dto import TrainConfig, ONNXRuntime


class MyEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, np.integer):
            return int(o)
        elif isinstance(o, np.floating):
            return float(o)
        else:
            return super(MyEncoder, self).default(o)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def get_logger(save_path: str, name: str):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(stream_handler)
    file_handler = logging.FileHandler(os.path.join(save_path, f'{name}.log'))
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.handlers.pop(0)

    return logger


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


def model_to_onnx(model, path: str):
    model_proto, external_tensor_storage = tf2onnx.convert.from_keras(model)

    last_layer = shape_inference.infer_shapes(model_proto).graph.value_info[-5]
    model_proto.graph.output.append(last_layer)
    checker.check_model(model_proto)
    save_model(model_proto, path)


def load_onnx(path: str) -> ONNXRuntime:
    if not os.path.exists(path):
        raise FileNotFoundError
    model = onnx.load(path)

    providers = onnxruntime.get_available_providers()
    if 'TensorrtExecutionProvider' in providers:
        providers.remove('TensorrtExecutionProvider')
    runtime = onnxruntime.InferenceSession(path, providers=providers)

    for w in reversed(model.graph.initializer):
        dense = numpy_helper.to_array(w)
        if dense.ndim == 2 and dense.shape[1] == 2:
            return ONNXRuntime(runtime=runtime, dense=dense)

    raise Exception("Invalid ONNX Model")

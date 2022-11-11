import os
from typing import List, Tuple, Generator

import numpy as np
import onnxruntime

import tensorflow as tf
import tf2onnx
import onnx
from onnx import shape_inference, checker, save_model
import onnx.numpy_helper as numpy_helper

from utils.dto import ONNXRuntime


def set_gpu_to_growth():
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            logical_gpus = tf.config.list_logical_devices('GPU')
            print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
        except RuntimeError as e:
            print(e)


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
    runtime = onnxruntime.InferenceSession(path)

    for w in reversed(model.graph.initializer):
        dense = numpy_helper.to_array(w)
        if dense.ndim == 2 and dense.shape[1] == 2:
            return ONNXRuntime(runtime=runtime, dense=dense)

    raise Exception("Invalid ONNX Model")


def batch(data, batch_size: int = 1) \
        -> Generator[Tuple[tf.Tensor, tf.Tensor], Tuple[List[Tuple[np.ndarray, Tuple[float, float]]], int], None]:
    size = len(data)
    for idx in range(0, size, batch_size):
        split = data[idx:min(idx + batch_size, size)]
        yield tf.convert_to_tensor([s[0] for s in split]), tf.convert_to_tensor([s[1] for s in split])

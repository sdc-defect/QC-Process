import os
from typing import Tuple

import numpy as np
import onnx
import onnxruntime

import tensorflow as tf
import tf2onnx
from onnx import shape_inference, checker, save_model, numpy_helper as numpy_helper

from utils import ONNXRuntime


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


@tf.function
def train(images: np.ndarray, labels: np.ndarray,
          model, loss_func, optimizer) -> Tuple[tf.Tensor, tf.Tensor]:
    with tf.GradientTape() as tape:
        prob: tf.Tensor = model(tf.convert_to_tensor(images), training=True)
        loss: tf.Tensor = loss_func(tf.convert_to_tensor(labels), prob)
    gradients: list = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))

    return loss, prob


@tf.function
def test(images: np.ndarray, labels: np.ndarray,
         model, loss_func) -> Tuple[tf.Tensor, tf.Tensor]:
    prob: tf.Tensor = model(tf.convert_to_tensor(images), training=False)
    loss: tf.Tensor = loss_func(tf.convert_to_tensor(labels), prob)

    return loss, prob


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

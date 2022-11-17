import base64
import json
import os
from dataclasses import asdict

import cv2
import numpy as np
import onnx

import onnxruntime
import onnx.numpy_helper as numpy_helper

from utils.dto import ONNXRuntime, InferenceResult


def check_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)


def load_onnx(path: str) -> ONNXRuntime:
    if not os.path.exists(path):
        raise FileNotFoundError
    model = onnx.load_model(path)
    runtime = onnxruntime.InferenceSession(path)

    for w in reversed(model.graph.initializer):
        dense = numpy_helper.to_array(w)
        if dense.ndim == 2 and dense.shape[1] == 2:
            return ONNXRuntime(runtime=runtime, dense=dense)


def merge_two_imgs(img1: np.ndarray, img2: np.ndarray, per_1: float = 0.5, per_2: float = 0.3) -> np.ndarray:
    merged = img1 * per_1 + img2 * per_2
    merged -= np.min(merged)
    merged /= np.max(merged)

    return merged


async def save_images(data: InferenceResult) -> None:
    if not isinstance(data, InferenceResult):
        raise TypeError("Invalid Type")
    # save images
    try:
        folder = 'log/' + data.filename[:10]
        fname = data.filename[11:]
        check_folder(folder)
        cv2.imwrite(f"{folder}/{fname}.jpg", data.img)
        cv2.imwrite(f"{folder}/{fname}_cam.jpg", data.cam)
        cv2.imwrite(f"{folder}/{fname}_merged.jpg", data.merged)
    except Exception as e:
        print("save InferenceResult Failed - ", e)


def transfer_image(result: InferenceResult):
    result = asdict(result)
    result['img'] = image_to_base64(result['img'])
    result['cam'] = image_to_base64(result['cam'])
    result['merged'] = image_to_base64(result['merged'])

    return json.dumps(result)


def image_to_base64(img: np.ndarray) -> str:
    img_buffer = cv2.imencode('.jpg', img)[1]

    return base64.b64encode(img_buffer).decode('utf-8')

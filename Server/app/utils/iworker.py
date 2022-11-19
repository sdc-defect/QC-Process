import re
from typing import List, Optional

import datetime

import numpy as np
import cv2

import utils
from utils.dto import InferenceResult, ONNXRuntime


class IWorker:
    def __init__(self, path: str):
        self._path = path
        self._size = (300, 300)
        self._runtime: Optional[ONNXRuntime] = utils.load_onnx(self._path)

        self._img0: Optional[np.ndarray] = None
        self._timestamp: Optional[datetime.datetime] = None

    def get_model_path(self):
        return self._path

    def update_runtime(self, path):
        self._path = path
        del self._runtime.runtime
        del self._runtime.dense
        self._runtime = utils.load_onnx(self._path)

    def _preprocess(self, img: np.ndarray) -> np.ndarray:
        img = cv2.resize(img, self._size)
        self._img0 = img.copy()

        return np.expand_dims(img / 255, axis=0).astype('float32')

    def inference(self, img: np.ndarray, timestamp) -> InferenceResult:
        if self._runtime is None:
            raise Exception("No Runtime")
        self._timestamp = timestamp
        img = self._preprocess(img)

        output = self._runtime.runtime.run(None, {'input_1': img})

        return self._postprocess(output)

    def _postprocess(self, output: List[np.ndarray]) -> InferenceResult:
        timestamp = self._timestamp.strftime("%Y-%m-%d_%H:%M:%S:%f")[:-3]
        filename = re.sub('[-:]', '_', timestamp)
        prob = output[0].squeeze()
        label = int(np.argmax(prob))
        conv_layer = output[1].squeeze()
        cam = self._get_cam(conv_layer, 1, True)
        merged = utils.merge_two_imgs(self._img0, cam)
        merged = cv2.normalize(merged, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

        return InferenceResult(timestamp, filename, [float(p) for p in prob], label, self._img0, cam, merged)

    def _get_cam(self, conv_layer: np.ndarray, target_label: int, is_rgb: bool = False) -> np.ndarray:
        c, h, w = conv_layer.shape

        cam = np.matmul(np.expand_dims(self._runtime.dense[:, target_label], axis=0),
                        np.reshape(conv_layer, (c, h * w)))
        cam = np.reshape(cam, (h, w))
        cam = (cam - np.min(cam)) / (np.max(cam) - np.min(cam))
        cam = np.expand_dims(np.uint8(255 * cam), axis=2)
        cam = cv2.applyColorMap(cv2.resize(cam, self._size), cv2.COLORMAP_JET)
        if is_rgb:
            cam = cv2.cvtColor(cam, cv2.COLOR_BGR2RGB)

        return cam

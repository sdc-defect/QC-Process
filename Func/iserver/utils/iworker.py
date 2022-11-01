from typing import List

import numpy as np
import numpy.typing as npt
import onnxruntime
import cv2

import utils
from utils.dto import InferenceResult


def merge_two_imgs(img1: np.ndarray, img2: np.ndarray, per_1: float = 0.5, per_2: float = 0.3) -> npt.NDArray[np.float64]:
    merged = img1 * per_1 + img2 * per_2
    merged -= np.min(merged)
    merged /= np.max(merged)

    return merged


class IWorker:
    def __init__(self, onnx_path: str, npy_path: str):
        self._logger = utils.get_logger("ONNX Worker")
        self._model = onnxruntime.InferenceSession(onnx_path, providers=["CUDAExecutionProvider"])
        self._dense = np.load(npy_path)
        self._size = (300, 300)
        self._img0 = None

    def _preprocess(self, img: np.ndarray):
        self._img0 = img.copy()

        return np.expand_dims(img / 255, axis=0).astype('float32')

    def inference(self, img: np.ndarray) -> InferenceResult:
        img = self._preprocess(img)
        output = self._model.run(None, {'input_1': img})

        return self._postprocess(output)

    def _postprocess(self, output: List[np.ndarray]) -> InferenceResult:
        prob = output[0].squeeze()
        label = int(np.argmax(prob))
        conv_layer = output[1].squeeze()
        cam = self._get_cam(conv_layer, 1)
        merged = merge_two_imgs(self._img0, cam)

        return InferenceResult(label, list(prob), cam, merged)

    def _get_cam(self, conv_layer: np.ndarray, target_label: int, is_rgb: bool = False):
        c, h, w = conv_layer.shape

        cam = np.matmul(np.expand_dims(self._dense[:, target_label], axis=0),
                        np.reshape(conv_layer, (c, h * w)))
        cam = np.reshape(cam, (h, w))
        cam = (cam - np.min(cam)) / (np.max(cam) - np.min(cam))
        cam = np.expand_dims(np.uint8(255 * cam), axis=2)
        cam = cv2.applyColorMap(cv2.resize(cam, self._size), cv2.COLORMAP_JET)
        if is_rgb:
            cam = cv2.cvtColor(cam, cv2.COLOR_BGR2RGB)

        return cam


if __name__ == "__main__":
    wo = IWorker(onnx_path="../temp/case2/onnx/modified.onnx", npy_path="../temp/case2/onnx/dense.npy")
    im = cv2.imread("../temp/dataset/test/1_def/def_7724.jpeg")
    result = wo.inference(im)

    cv2.imshow("concat", cv2.hconcat((result.cam / 255, result.merged)))
    cv2.waitKey()

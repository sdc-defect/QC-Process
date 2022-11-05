import time
import datetime
from typing import List, Union, Tuple, Dict

import multiprocessing as mp
import numpy as np
import cv2

import utils
from utils.dto import InferenceResult, ONNXRuntime


class IWorker:
    def __init__(self, path: str, size: Union[Tuple[int, int], int] = (300, 300)):
        self._path = path
        self._size = size
        self._runtime: Union[ONNXRuntime, None] = None
        self._img0 = None
        self._timestamp = None

    def __getstate__(self) -> Dict:
        return {'path': self._path, 'size': self._size}

    def __setstate__(self, values):
        self._path = values['path']
        self._size = values['size']
        self._runtime = utils.load_onnx(self._path)

    def _preprocess(self, img: np.ndarray) -> np.ndarray:
        self._timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._img0 = img.copy()

        return np.expand_dims(img / 255, axis=0).astype('float32')

    def inference(self, img: np.ndarray) -> InferenceResult:
        img = self._preprocess(img)

        output = self._runtime.runtime.run(None, {'input_1': img})

        return self._postprocess(output)

    def _postprocess(self, output: List[np.ndarray]) -> InferenceResult:
        prob = output[0].squeeze()
        label = int(np.argmax(prob))
        conv_layer = output[1].squeeze()
        cam = self._get_cam(conv_layer, 1)
        merged = utils.merge_two_imgs(self._img0, cam)

        return InferenceResult(self._timestamp, [float(p) for p in prob], label, self._img0, cam, merged)

    def _get_cam(self, conv_layer: np.ndarray, target_label: int, is_rgb: bool = False):
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


class IProcess(mp.Process):
    def __init__(self, queue: mp.Queue, path: str, size: Union[Tuple[int, int], int] = (300, 300)):
        super(IProcess, self).__init__()
        self._queue = queue
        self._worker = IWorker(path, size)

    def run(self) -> None:
        while True:
            time.sleep(1)
            rimg = np.uint8(np.random.rand(300, 300, 3) * 255)

            result = self._worker.inference(rimg)
            print(result.timestamp)
            self._queue.put(result)


class IService:
    def __init__(self):
        self.queue = mp.Queue()
        self._path: Union[str, None] = None
        self._size: Union[Tuple[int, int]] = (300, 300)
        self._process: Union[IProcess, None] = None
        self.terminated = []

    def check_process_alive(self):
        if self._process is None:
            return False
        return self._process.is_alive()

    def update_onnx_info(self, path: str, size: Union[Tuple[int, int], int] = (300, 300)):
        self._path = path
        self._size = size

    def run_process(self):
        if self._path is None:
            raise RuntimeError("Specify ONNX path")
        if self._size is None:
            raise RuntimeError("Specify image size")
        if self.check_process_alive():
            raise RuntimeError("Process is already started")

        self._process = IProcess(self.queue, self._path, self._size)
        self._process.start()

    async def stop_inference(self):
        self._process.terminate()
        self._process.join()

        self.terminated.append(self._process)
        self._process = None


if __name__ == "__main__":
    # mp.freeze_support()
    # mp.set_start_method('spawn')
    service = IService()
    service.update_onnx_info("../temp/case2/onnx/modified.onnx")
    service.run_process()
    time.sleep(10)
    service.stop_inference()

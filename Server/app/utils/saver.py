import os
import time
import subprocess

import numpy as np

from onnx import load, shape_inference, checker, save_model
import onnx.numpy_helper as numpy_helper

import utils


class Convertor:
    def __init__(self, onnx_name: str = 'model.onnx', modified_name: str = 'default.onnx'):
        self._logger = utils.get_logger(__name__)
        self._onnx_name = onnx_name
        self._modified_name = modified_name

    def save(self, model_path):
        folder = os.path.join(model_path, "onnx")
        utils.check_folder(folder)

        try:
            self._saved_model_to_onnx(model_path, folder)
            self._modify_onnx(folder)
        except Exception as e:
            self._logger.error(f"Failed to convert saved model to onnx!!! - {e}")

    def _saved_model_to_onnx(self, model_path, folder):
        st = time.time()
        subprocess.run(args=["python", "-m", "tf2onnx.convert", "--tag", "serve",
                             "--saved-model", model_path, "--output",
                             os.path.join(folder, self._onnx_name)],
                       shell=True, encoding='utf-8')
        self._logger.info(f"Convert Tensorflow Model to ONNX {time.time() - st:.2f}s")

    def _modify_onnx(self, folder):
        st = time.time()
        model = load(os.path.join(folder, "model.onnx"))
        last_layer = shape_inference.infer_shapes(model).graph.value_info[-5]
        for w in reversed(model.graph.initializer):
            temp = numpy_helper.to_array(w)
            if temp.ndim == 2 and temp.shape[1] == 2:
                np.save(os.path.join(folder, "dense.npy"), temp)
                break

        model.graph.output.append(last_layer)
        checker.check_model(model)
        save_model(model, os.path.join(folder, "default.onnx"))

        self._logger.info(f"Modify ONNX {time.time() - st:.2f}s")

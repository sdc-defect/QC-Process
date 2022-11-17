from typing import List

from dataclasses import dataclass
import numpy as np
import onnxruntime


@dataclass
class InferenceResult:
    timestamp: str
    filename: str
    prob: List[float]
    label: int
    img: np.ndarray
    cam: np.ndarray
    merged: np.ndarray


@dataclass
class ONNXRuntime:
    runtime: onnxruntime.InferenceSession
    dense: np.ndarray


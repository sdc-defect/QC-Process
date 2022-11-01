from typing import List

from dataclasses import dataclass
import numpy as np


@dataclass
class InferenceResult:
    idx: int
    prob: List[float]
    cam: np.ndarray
    merged: np.ndarray

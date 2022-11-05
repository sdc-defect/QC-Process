import json
import numpy as np
import cv2
import base64
from dataclasses import asdict

from utils.dto import InferenceResult


def transfer_image(result: InferenceResult):
    result = asdict(result)
    result['img'] = image_to_base64(result['img'])
    result['cam'] = image_to_base64(result['cam'])
    result['merged'] = image_to_base64(result['merged'])

    return json.dumps(result)


def image_to_base64(img: np.ndarray) -> str:
    img_buffer = cv2.imencode('.jpg', img)[1]

    return base64.b64encode(img_buffer).decode('utf-8')


def get_image(volume, index: int):
    image = volume[:, :, index]
    return image_to_base64(image)

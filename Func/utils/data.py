import json
import numpy as np
import cv2
import base64
from dataclasses import asdict

from utils.dto import InferenceResult


def reverse_transfer_image(result: InferenceResult):
    result['img'] = base64_to_image(result['img'])
    result['cam'] = base64_to_image(result['cam'])
    result['merged'] = base64_to_image(result['merged'])

    return result


def base64_to_image(img: str) -> np.ndarray:
    binary = base64.b64decode(img)
    image = np.asarray(bytearray(binary), dtype=np.uint8)

    return cv2.imdecode(image, cv2.IMREAD_COLOR)


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

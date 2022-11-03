from typing import List
import os
import numpy as np
import onnxruntime
import cv2
import time
import sys

class Worker:
    def __init__(self, onnx_path: str):
    
        self._model = onnxruntime.InferenceSession(onnx_path)
        self._size = (300, 300)
        self._img0 = None

    def _preprocess(self, img: np.ndarray):
        self._img0 = img.copy()

        return np.expand_dims(img / 255, axis=0).astype('float32')

    def inference(self, img: np.ndarray):
        img = self._preprocess(img)
        result = self._model.run(None, {'input_1': img})
        return result

wo = Worker(onnx_path="model.onnx")

def inferencing_image(im):
    global wo
    print('<---start--->')
    start=time.time()
    tmp_result=wo.inference(im)
    end=time.time()
    print(tmp_result)
    print('time=',end-start)
    print('<-----end----->')

cap = cv2.VideoCapture(0)
timeCheck=time.time()
while 1:
    if time.time()-timeCheck>=1:
        timeCheck=time.time()
        ret,frame=cap.read()
        frame=frame[15:465,85:535]
        frame=cv2.resize(frame,(300,300))
        cv2.imshow('test',frame)
        inferencing_image(frame)
        cv2.waitKey(1)
cap.release()
cv2.destroyAllWindows()
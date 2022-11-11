from typing import List
import os
import numpy as np
import onnxruntime
import cv2
import time
import sys
import RPi.GPIO as GPIO

def setup(Rpin, Gpin, Bpin):
    global pins
    global p_R, p_G, p_B
    pins = {'pin_R': Rpin, 'pin_G': Gpin, 'pin_B': Bpin}
    GPIO.setmode(GPIO.BCM)
    for i in pins:
        GPIO.setup(pins[i], GPIO.OUT)
        GPIO.output(pins[i], GPIO.HIGH)
    
    p_R = GPIO.PWM(pins['pin_R'], 2000)
    p_G = GPIO.PWM(pins['pin_G'], 2000)
    p_B = GPIO.PWM(pins['pin_B'], 2000)
    
    p_R.start(0)
    p_G.start(0)
    p_B.start(0)
    
def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def setColor(col):   
    R_val = (col & 0xff0000) >> 16
    G_val = (col & 0x00ff00) >> 8
    B_val = (col & 0x0000ff) >> 0

    R_val = map(R_val, 0, 255, 0, 100)
    G_val = map(G_val, 0, 255, 0, 100)
    B_val = map(B_val, 0, 255, 0, 100)
    
    p_R.ChangeDutyCycle(100-R_val)
    p_G.ChangeDutyCycle(100-G_val)
    p_B.ChangeDutyCycle(100-B_val)
    
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
    if tmp_result[0][0][0]>0.75:
        setColor(0x00FF00)
    else:
        setColor(0xFF0000)
    print(tmp_result)
    print('time=',end-start)
    print('<-----end----->')

cap = cv2.VideoCapture(0)
timeCheck=time.time()
setup(23,24,25)
setColor(0x000000)
while 1:
    if time.time()-timeCheck>=1:
        timeCheck=time.time()
        ret,frame=cap.read()
        frame=frame[15:465,85:535]
        frame=cv2.resize(frame,(300,300))
        cv2.imshow('test',frame)
        setColor(0xFFFF00)
        inferencing_image(frame)
        cv2.waitKey(1)
cap.release()
cv2.destroyAllWindows()
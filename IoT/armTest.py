import RPi.GPIO as GPIO

from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(25,GPIO.OUT)

servo1=GPIO.PWM(23,50)
servo1.start(0)
servo2=GPIO.PWM(24,50)
servo2.start(0)
servo3=GPIO.PWM(25,50)
servo3.start(0)

def setServoLoc(num,degree):
    if degree>180:
        degree=180
    if degree<0:
        degree=0
    if num==1:
        duty = 3+(degree*9/180.0)
        servo1.ChangeDutyCycle(duty)
    if num==2:
        duty = 3+(degree*9/180.0)
        servo2.ChangeDutyCycle(duty)
    if num==3:
        duty = 3+(degree*9/180.0)
        servo3.ChangeDutyCycle(duty)
    sleep(1)
while 1:
    num,degree=input().split()
    setServoLoc(int(num),int(degree))
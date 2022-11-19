import RPi.GPIO as GPIO

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(13,GPIO.OUT)
    GPIO.setup(5,GPIO.OUT)
    GPIO.setup(6,GPIO.OUT)
    GPIO.output(5,1)
    GPIO.output(6,0)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    GPIO.output(17, GPIO.HIGH)
    
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)
    GPIO.setup(25, GPIO.OUT)
    GPIO.output(23, GPIO.HIGH)
    GPIO.output(24, GPIO.HIGH)
    GPIO.output(25, GPIO.HIGH)

                                  
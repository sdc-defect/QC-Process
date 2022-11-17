import RPi.GPIO as GPIO
import time

def setup():
    GPIO.setmode(GPIO.BCM)      
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def loop():
    while True:
        if GPIO.input(17) == GPIO.LOW:
            print ('White detected')

        else:
            print ('Black detected')
        time.sleep(0.5)
 

if __name__ == '__main__':     
    setup()
    loop()

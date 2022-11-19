import RPi.GPIO as GPIO

class Conveyor:
    def __init__(self) -> None:
        self.pwmMotor=GPIO.PWM(13,100)
        self.pwmMotor.start(0)
        self.setMotorDirection(False)

    def setMotorSpeed(self,speed):
        self.pwmMotor.ChangeDutyCycle(speed)

    def setMotorDirection(self,a):
        if a:
            GPIO.output(5,0)
            GPIO.output(6,1)
        else:
            GPIO.output(5,1)
            GPIO.output(6,0)
import pigpio
import time

pi=pigpio.pi()

def servoControl(num,degree):
    if degree>180:
        degree=180
    elif degree<0:
        degree=0
    degree= degree*(2000/180.0)+500
    if num==1:
        pi.set_servo_pulsewidth(23,degree)
    elif num==2:
        pi.set_servo_pulsewidth(24,degree)
    elif num==3:
        pi.set_servo_pulsewidth(25,degree)

    time.sleep(1)

while 1:
    num,degree=input().split()
    servoControl(int(num),int(degree))
import pigpio
import time
from multiprocessing import Process


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
numList=[1,2,3]
degreeList=[45,45,45]
while 1:
    degree=int(input())
    #servoControl(int(num),int(degree))
    p1=Process(target=servoControl,args=(numList[0],degree))
    p2=Process(target=servoControl,args=(numList[1],degree))
    p3=Process(target=servoControl,args=(numList[2],degree))

    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()

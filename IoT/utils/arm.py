import pigpio
import RPi.GPIO as GPIO
from threading import Thread
from time import sleep

class RobotArm:
    def __init__(self) -> None:
        self.degreeList=[[500,1000,500],[1500,2500,500],[500,1000,500],[500,1000,1500],[500,1500,1500],[1500,2100,1500],[500,1000,500]] 
        self.pi=pigpio.pi()
        self.nowDegree=[500,1000,500]
        self.p1=Thread(target=self.servoControl,args=(1,self.degreeList[0][0],self.nowDegree[0]))
        self.p2=Thread(target=self.servoControl,args=(2,self.degreeList[0][1],self.nowDegree[1]))
        self.p3=Thread(target=self.servoControl,args=(3,self.degreeList[0][2],self.nowDegree[2]))
        self.p1.start()
        self.p2.start()
        self.p3.start()
        self.p1.join()
        self.p2.join()
        self.p3.join()

    def servoControl(self,num,degree,nD):
        if degree>2500:
            degree=2500
        elif degree<500:
            degree=500
        pm=-10 if nD>degree else 10
        if num==1:
            self.pi.set_servo_pulsewidth(16,nD+pm)
        elif num==2:
            self.pi.set_servo_pulsewidth(20,nD+pm)
        elif num==3:
            self.pi.set_servo_pulsewidth(21,nD+pm)
        self.nowDegree[num-1]=nD+pm
        sleep(0.001)
    
    def armControl(self):
        for i in range(len(self.degreeList)):
            while True:
                self.p1=Thread(target=self.servoControl,args=(1,self.degreeList[i][0],self.nowDegree[0]))
                self.p2=Thread(target=self.servoControl,args=(2,self.degreeList[i][1],self.nowDegree[1]))
                self.p3=Thread(target=self.servoControl,args=(3,self.degreeList[i][2],self.nowDegree[2]))
                self.p1.start()
                self.p2.start()
                self.p3.start()
                self.p1.join()
                self.p2.join()
                self.p3.join()
                if abs(self.degreeList[i][0]-self.nowDegree[0])<1 and abs(self.degreeList[i][1]-self.nowDegree[1])<1 and abs(self.degreeList[i][2]-self.nowDegree[2])<1:
                        break
            if i==5:
                    GPIO.output(17, GPIO.HIGH)
import RPi.GPIO as GPIO

class Led:
    def __init__(self) -> None:
        self.p_R = GPIO.PWM(23, 2000)
        self.p_G = GPIO.PWM(24, 2000)
        self.p_B = GPIO.PWM(25, 2000)
        self.p_R.start(0)
        self.p_G.start(0)
        self.p_B.start(0)
        self.setColor(0x00FFFF)
    
    def setColor(self,col):   
        R_val = (col & 0xff0000) >> 16
        G_val = (col & 0x00ff00) >> 8
        B_val = (col & 0x0000ff) >> 0

        R_val = self.map(R_val, 0, 255, 0, 100)
        G_val = self.map(G_val, 0, 255, 0, 100)
        B_val = self.map(B_val, 0, 255, 0, 100)
        
        self.p_R.ChangeDutyCycle(100-R_val)
        self.p_G.ChangeDutyCycle(100-G_val)
        self.p_B.ChangeDutyCycle(100-B_val)

    def map(self,x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

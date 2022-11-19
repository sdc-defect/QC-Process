import smbus as smbus
import RPi.GPIO as GPIO
import time

bus = smbus.SMBus(1)
def setup(Addr):
    global address
    address = Addr
maxLux=0
if __name__ == "__main__":
    setup(0x48)
    while True:
        bus.write_byte(address,0x40)
        bus.read_byte(address)
        tmp=bus.read_byte(address)
        if maxLux<tmp:
            maxLux=tmp
        time.sleep(0.2)
        print('Now: ',tmp,', Max: ',maxLux)
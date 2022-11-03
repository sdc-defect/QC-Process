import smbus as smbus
import RPi.GPIO as GPIO
import time

bus = smbus.SMBus(1)
def setup(Addr):
    global address
    address = Addr

def read(chn): #channel
    try:
        if chn == 0:
            bus.write_byte(address,0x40)
        if chn == 1:
            bus.write_byte(address,0x41)
        if chn == 2:
            bus.write_byte(address,0x42)
        if chn == 3:
            bus.write_byte(address,0x43)
        bus.read_byte(address)
    except Exception as e:
        print (e)
    return bus.read_byte(address)

if __name__ == "__main__":
    setup(0x48)
    while True:
        tmp = read(0)
        time.sleep(0.2)
        print(tmp)
        
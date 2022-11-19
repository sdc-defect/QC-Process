import smbus as smbus
import RPi.GPIO as GPIO
import pigpio
import utils
from utils.arm import RobotArm
from utils.led import Led
from utils.conveyor import Conveyor
from time import sleep
import websockets
import asyncio 
import json
import multiprocessing as mp


async def ws_client(q):
    uri = "ws://k7b306.p.ssafy.io:8080/ws"

    async with websockets.connect(uri, ping_interval=None) as websocket:
        data = await websocket.recv()
        subscribe_data = json.dumps({})
        await websocket.send(subscribe_data)

        while True:
            data = await websocket.recv()
            imgDescription = json.loads(data.replace("'", "\""))
            q.put(imgDescription['label'])



async def m(q):
    await ws_client(q)

def producer(q):
    asyncio.run(m(q))

if __name__ == "__main__":
    pi=pigpio.pi()
    bus = smbus.SMBus(1)
    utils.setup()
    arm=RobotArm()
    light=Led()
    conveyor=Conveyor()
    q = mp.Queue()
    p = mp.Process(name="Pr", target=producer, args=(q,), daemon=True)
    p.start()
    conveyor.setMotorSpeed(13)
    while 1:
        bus.write_byte(0x48,0x40)
        stuff=bus.read_byte(0x48)
        stuff=bus.read_byte(0x48)
        sleep(0.001)
        if stuff>180:
            count+=1
        else:
            count=0 
        if count>10:
            tmp =q.get()
            if tmp==1:
                light.setColor(0x00FF00)
                conveyor.setMotorSpeed(0)
                conveyor.setMotorDirection(True)
                conveyor.setMotorSpeed(14)
                sleep(0.1)
                conveyor.setMotorSpeed(0)
                conveyor.setMotorDirection(False)
                count=0
                GPIO.output(17, GPIO.LOW)
                arm.armControl()
                light.setColor(0x00FFFF)
                conveyor.setMotorSpeed(13)
            else:
                light.setColor(0xFF0000)
                sleep(0.4)
                light.setColor(0x00FFFF)
                conveyor.setMotorSpeed(13)
    conveyor.setMotorSpeed(0)
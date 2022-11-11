from typing import Tuple
from asyncio import Queue, Task
from multiprocessing import Queue
from multiprocessing.synchronize import Event
from typing import Union

import asyncio
import time
import threading
import websockets
import multiprocessing as mp

from utils.iworker import IProcess


class IService:
    def __init__(self, queue: mp.Queue):
        self._process: Union[IProcess, None] = None
        self._queue = queue
        self._flag = mp.Event()

    async def run_process(self, path: str, size: Union[Tuple[int, int], int] = (300, 300)):
        if path is None:
            raise RuntimeError("Specify ONNX path")
        if size is None:
            raise RuntimeError("Specify image size")
        if self._process is not None:
            raise RuntimeError("Process is already started")

        self._process = IProcess(self._flag, self._queue, path, size)
        self._process.start()
        self._flag.set()

    async def stop_inference(self):
        self._flag.clear()
        self._process.terminate()
        self._process.join()

        self._process = None

    def get_flag(self):
        return self._flag.is_set()

    async def pause_inference(self):
        self._flag.clear()

    async def restart_inference(self):
        self._flag.set()


class Listener(threading.Thread):
    def __init__(self, queue: Queue):
        super().__init__()
        self._flag = False
        self.subscriber: Union[Queue, None] = None
        self._listener_task: Union[Task, None] = None
        self._queue = queue

    def get_flag(self):
        return self._flag

    def set_flag(self, flag: bool):
        self._flag = flag

    async def subscribe(self, q: Queue) -> None:
        self.subscriber = q

    async def check_subscribe(self) -> bool:
        return True if self.subscriber is not None else False

    async def start_listening(self) -> None:
        self._listener_task = asyncio.create_task(self._listener())

    async def _listener(self) -> None:
        async with websockets.connect("ws://localhost:8001") as websocket:
            async for message in websocket:
                await self.subscriber.put(message)

    async def stop_listening(self):
        if self._listener_task.done():
            self._listener_task.result()
        else:
            self._listener_task.cancel()

    def run(self) -> None:
        while True:
            if self.subscriber is None:
                continue
            try:
                data = self._queue.get()

                try:
                    self.subscriber.put_nowait(data)
                except Exception as e:
                    raise e
            except Exception as e:
                print(e)

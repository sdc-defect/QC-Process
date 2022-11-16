from typing import Optional, List
from asyncio import Queue, Task

import asyncio
import time
import datetime
import threading
import random

import cv2
import websockets
import multiprocessing as mp
import numpy as np
from glob import glob

from utils import InferenceResult
from utils.iworker import IWorker


class Service:
    def __init__(self):
        super().__init__()
        self._flag = mp.Event()
        self._subscribers: List[Queue] = []
        self._worker = IWorker("./model/case21.onnx")
        self._listener_task: Optional[Task] = None
        self._worker_task: Optional[threading.Thread] = None

        self._files = glob('dataset/*.[png$|jpg$|jpeg$|tif$]', recursive=True)

    def get_flag(self) -> bool:
        return self._flag.is_set()

    def clear_flag(self) -> None:
        if len(self._subscribers) == 0:
            return
        self._flag.clear()

    def set_flag(self) -> None:
        if len(self._subscribers) == 0:
            return
        self._flag.set()

    async def subscribe(self, q: Queue) -> None:
        self._subscribers.append(q)
        self.set_flag()

    async def unsubscribe(self, q: Queue) -> None:
        self._subscribers.remove(q)
        if len(self._subscribers) == 0:
            self._flag.clear()

    def get_subscriber_size(self) -> int:
        return len(self._subscribers)

    def get_model_path(self) -> str:
        return self._worker.get_model_path()

    async def start_listening(self) -> None:
        self._listener_task = asyncio.create_task(self._listener())

    async def _listener(self) -> None:
        async with websockets.connect("ws://localhost:8001") as websocket:
            async for message in websocket:
                for q in self._subscribers:
                    await q.put(message)

    async def stop_listening(self) -> None:
        if self._listener_task.done():
            self._listener_task.result()
        else:
            self._listener_task.cancel()

    def update_worker(self, path) -> None:
        self._flag.clear()
        self._worker.update_runtime(path)
        self._flag.set()

    def start_worker(self) -> None:
        if self._worker_task is not None:
            return

        self._worker_task = threading.Thread(target=self._run, daemon=True)
        self._worker_task.start()

    def _run(self) -> None:
        while True:
            if not self._flag.is_set() or self._subscribers is None or len(self._subscribers) == 0:
                continue
            try:
                time.sleep(1)
                img = cv2.imread(random.choice(self._files))

                data = self._worker.inference(img, datetime.datetime.now())

                for q in self._subscribers:
                    q.put_nowait(data)
            except Exception as e:
                print(e)

    def single_inference_bytes(self, data: bytes) -> InferenceResult:
        self._flag.clear()
        img: np.ndarray = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
        result = self._worker.inference(img, datetime.datetime.now())
        self._flag.set()

        return result

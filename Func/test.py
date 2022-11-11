import websockets
import asyncio


async def ws_client():
    url = "ws://127.0.0.1:8000/ws"

    async with websockets.connect(url) as websocket:
        greeting = await websocket.recv()
        print(greeting)

async def main():
    await ws_client()

asyncio.run(main())
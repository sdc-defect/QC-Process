import asyncio
import multiprocessing as mp

from fastapi import FastAPI, Response, WebSocket
from starlette.websockets import WebSocketDisconnect

from service import IService, Listener


app = FastAPI()
queue = mp.Queue()
service = IService(queue)
listener = Listener(queue)


@app.on_event("startup")
async def startup_event():
    await listener.start_listening()
    service.update_onnx_info("./data/modified.onnx")
    service.run_process()
    listener.start()
    return


@app.on_event("shutdown")
async def shutdown_event():
    await listener.stop_listening()
    return


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    if listener.get_flag():
        return

    await websocket.accept()
    listener.set_flag(True)
    q: asyncio.Queue = asyncio.Queue()

    await listener.subscribe(q=q)
    await service.restart_inference()

    print(f"client connected : {websocket.client}")

    try:
        while True:
            data = await q.get()

            await websocket.send_text(data)
    except WebSocketDisconnect:
        print("websocket connection missing")
        return
    except Exception as e:
        print("websocket connection missing", e)
        await service.stop_inference()
        is_sending = False
        return


@app.post("/pause", status_code=200)
async def pause_isystem():
    await service.pause_inference()
    return {"message": "Successfully Paused"}


@app.post("/restart", status_code=200)
async def restart_isystem():
    await service.restart_inference()
    return {"message": "Successfully Restarted"}


@app.post("/stop", status_code=200)
async def stop_isystem(response: Response):
    check = service.check_process_alive()
    if not check:
        response.status_code = 409
        return {"message": "Already Stopped"}
    else:
        await service.stop_inference()
        return {"message": "Successfully Stopped"}




# 개발/디버깅용으로 사용할 앱 구동 함수
def run():
    import uvicorn
    uvicorn.run(app)


if __name__ == "__main__":
    run()

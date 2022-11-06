import time
import websockets

from fastapi import FastAPI, Response, WebSocket
from starlette.websockets import WebSocketDisconnect

from utils.data import transfer_image
from utils.iworker import IService


app = FastAPI()
service = IService()
is_connected = True

# @app.post("/conn", status_code=200)
# async def connection():
#     return {"message": "Successfully Connected"}


# 웹소켓 설정
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print(f"client connected : {websocket.client}")
    await websocket.accept()
    try:
        await websocket.send_text(f"Welcome client : {websocket.client}")
        while True:
            time.sleep(0.1)
            if not service.queue.empty():
                result = service.queue.get()
                data = transfer_image(result)
                await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        await websocket.send_text(f"Bye client : {websocket.client}")
        await websocket.close()


@app.post("/conn", status_code=200)
async def connection():
    if is_connected:
        return {"message": "Successfully Connected"}
    else:
        return {"message": "Connection Failed"}


@app.post("/start", status_code=200)
async def start_isystem(response: Response):
    check = service.check_process_alive()
    if check:
        response.status_code = 409
        return {"message": "Already Started"}
    else:
        service.update_onnx_info("./data/modified.onnx")
        service.run_process()
        return {"message": "Successfully Started"}


@app.post("/stop", status_code=200)
async def stop_isystem(response: Response):
    check = service.check_process_alive()
    if not check:
        response.status_code = 409
        return {"message": "Already Stopped"}
    else:
        await service.stop_inference()
        return {"message": "Successfully Stopped"}


@app.post("/pause", status_code=200)
async def pause_isystem():
    return {"message": "Successfully Paused"}


# 개발/디버깅용으로 사용할 앱 구동 함수
def run():
    import uvicorn
    uvicorn.run(app)


if __name__ == "__main__":
    run()

from enum import Enum
from fastapi import FastAPI, Response, status, WebSocket, Request

from fastapi.responses import HTMLResponse
from fastapi.logger import logger

from starlette.websockets import WebSocketDisconnect

app = FastAPI()
service = IService()
is_connected = True

@app.post("/conn", status_code=200)
async def connection():
    return { "messege" : "Successfully Connected"}

# 웹소켓 설정 ws://127.0.0.1:8000/ws 로 접속할 수 있음
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print(f"client connected : {websocket.client}")
    await websocket.accept() # client의 websocket접속 허용
    try:
        await websocket.send_text(f"Welcome client : {websocket.client}")
        while True:
            # 수정해야됨 메시지 -> 이미지
            data = await websocket.receive_text()  # client 메시지 수신대기
            print(f"message received : {data} from : {websocket.client}")
            await websocket.send_text(f"Message text was: {data}") # client에 메시지 전달
    except WebSocketDisconnect:
        await websocket.close()

@app.post("/conn", status_code=200)
async def connection():
    if is_connected:
        return { "messege" : "Successfully Connected"}
    else:
        return { "messege" : "Connection Failed"}
    
@app.post("/start", status_code=200)
async def start_isystem(response: Response):
    check = service.check_process_alive()
    if check:
        response.status_code = 409
        return { "messege" : "Already Started"}
    else:
        service.update_onnx_info("./data/modified.onnx")
        service.run_process()
        return { "messege" : "Successfully Started"}

@app.post("/stop", status_code=200)
async def stop_isystem(response: Response):
    check = service.check_process_alive()
    if not check:
        response.status_code = 409
        return { "messege" : "Already Stopped"}
    else:
        await service.stop_inference()
        return { "messege" : "Successfully Stopped"}

@app.post("/pause", status_code=200)
async def pause_isystem():
    return { "messege" : "Successfully Paused"}
    

# 개발/디버깅용으로 사용할 앱 구동 함수
def run():
    import uvicorn
    uvicorn.run(app)


if __name__ == "__main__":
    run()
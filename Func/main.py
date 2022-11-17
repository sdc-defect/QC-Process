import asyncio
import os

from fastapi import FastAPI, HTTPException, WebSocket, UploadFile

import utils
from utils.service import Service
from utils.data import transfer_image

app = FastAPI()
service = Service()


@app.on_event("startup")
async def startup_event():
    await service.start_listening()
    service.start_worker()


@app.on_event("shutdown")
async def shutdown_event():
    await service.stop_listening()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    q: asyncio.Queue = asyncio.Queue()
    await service.subscribe(q=q)

    print(f"client connected : {websocket.client}")
    try:
        while True:
            data = await q.get()

            await websocket.send_text(transfer_image(data))
            await utils.save_images(data)
    except Exception as e:
        print("websocket connection missing", e)
        await service.unsubscribe(q)


@app.post("/pause", status_code=200)
async def pause_runtime():
    if not service.get_flag():
        raise HTTPException(status_code=500, detail="ISystem is not started")
    service.clear_flag()


@app.post("/restart", status_code=200)
async def restart_runtime():
    if service.get_flag():
        raise HTTPException(status_code=500, detail="ISystem is already started")
    service.set_flag()


@app.post("/single", status_code=200)
def inference_image(file: UploadFile):
    data = file.file.read()

    return transfer_image(service.single_inference_bytes(data))


@app.get("/model", status_code=200)
def get_model_path():
    return {'model': service.get_model_path().split('/')[-1].split('.')[0]}


@app.get("/model/list", status_code=200)
def get_models():
    files = os.listdir('model')

    models = [service.get_model_path().split('/')[-1].split('.')[0]]
    for file in files:
        fname = file.split('.')[0]
        if file.endswith('.onnx') and fname not in models:
            models.append(fname)
    return {'models': models}


@app.put("/model/upload", status_code=200)
async def upload_model(file: UploadFile):
    path = f"model/{file.filename}"
    f = file.file.read()
    with open(path, "wb+") as ff:
        ff.write(f)


@app.put("/model/update/{model}", status_code=200)
def update_runtime(model):
    path = os.path.join('model', f'{model}.onnx')
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"{model} model doesn't exists")
    service.update_worker(path)


@app.get("/status", status_code=200)
def get_status():
    if service.get_flag():
        return {"message": "Inference started"}
    else:
        return {"message": "Inference stopped"}


@app.get("/connections", status_code=200)
def get_connections():
    return {'connections': service.get_subscriber_size()}


# 개발/디버깅용으로 사용할 앱 구동 함수
def run():
    import uvicorn
    uvicorn.run(app)


if __name__ == "__main__":
    run()

import asyncio
import multiprocessing as mp

from fastapi import FastAPI, HTTPException, WebSocket, UploadFile, File
import shutil
import utils
from service import IService, Listener
from utils.data import transfer_image
from utils.iworker import IWorker
import os
import numpy as np
from io import BytesIO
from PIL import Image

app = FastAPI()
queue = mp.Queue()
service = IService(queue)
listener = Listener(queue)



@app.on_event("startup")
async def startup_event():
    await listener.start_listening()
    await service.run_process("./model/default.onnx")
    listener.start()


@app.on_event("shutdown")
async def shutdown_event():
    await listener.stop_listening()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    if listener.get_flag():
        #raise HTTPException(status_code=400, detail="Websocket is already connected")
        listener.set_flag(False)
        #test
    await websocket.accept()
    listener.set_flag(True)
    q: asyncio.Queue = asyncio.Queue()

    await listener.subscribe(q=q)
    await service.restart_inference()

    print(f"client connected : {websocket.client}")

    try:
        while True:
            data = await q.get()

            await websocket.send_text(transfer_image(data))
            # Add handshake
            await utils.save_logs(data)
    except Exception as e:
        print("websocket connection missing", e)
        await service.pause_inference()
        listener.set_flag(False)


@app.post("/pause", status_code=200)
async def pause_isystem():
    if not service.get_flag():
        raise HTTPException(status_code=500, detail="ISystem is not started")
    await service.pause_inference()
    return {"message": "Successfully Paused"}


@app.post("/restart", status_code=200)
async def restart_isystem():
    if service.get_flag():
        raise HTTPException(status_code=500, detail="ISystem is already started")
    await service.restart_inference()
    return {"message": "Successfully Restarted"}


#@app.post("/update", status_code=200)
#async def stop_isystem(file: UploadFile=File(...)):
#    print(file.filename)
    
#    try:
#        f = file.file.read()
#        with open(os.path.join('./',file.filename), "wb+") as ff:
#            shutil.copyfileobj(file.file,ff)
#    except Exception:
#        return{"message":"error occured"}
    
@app.put("/update",status_code=200)
async def stop_isystem(file:UploadFile):
    fname=f"model/{file.filename}"
    f=file.file.read()
    with open(fname,'wb+') as ff:
        ff.write(f)
    if listener.get_flag():
        raise HTTPException(status_code=400, detail="Websocket is already connected")
    #await service.stop_inference()
    await service.run_process(fname)
    transfer_image(data)
    return {"message": "Successfully Updated"}


@app.post("/oneshot",status_code=200)
async def once_isystem(file:UploadFile):
    f=await file.read()
    npImage=np.array(Image.open(BytesIO(f)))
    infOnce=IWorker("./model/default.onnx")
    result= infOnce.inference(npImage)
       
    return {'return':transfer_image(result)}


@app.get("/status", status_code=200)
def get_status():
    if listener.get_flag():
        return {"message": "Inference started"}
    else:
        return {"message": "Available to connect"}


# 개발/디버깅용으로 사용할 앱 구동 함수
def run():
    import uvicorn
    uvicorn.run(app)


if __name__ == "__main__":
    run()

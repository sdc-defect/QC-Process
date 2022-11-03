from fastapi import WebSocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("started")
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            print(f"received: {int(data)}")
            index = int(data)
            image = get_image(volume, index)
            await websocket.send_bytes(image)
    except Exception as e:
        print(e)
    finally:
        websocket.close()
        
def image_to_base64(img: np.ndarray) -> bytes:
    """ Given a numpy 2D array, returns a JPEG image in base64 format """

    # using opencv 2, there are others ways
    img_buffer = cv2.imencode('.jpg', img)[1]
    return base64.b64encode(img_buffer).decode('utf-8')
    
def get_image(volume, index: int):
    image = volume[:, :, index]
    return image_to_base64(image)
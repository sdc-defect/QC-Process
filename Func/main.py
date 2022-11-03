from enum import Enum
from fastapi import FastAPI, Response, status

app = FastAPI()


# class ModelName(str, Enum):
#     alexnet = "alexnet"
#     resnet = "resnet"
#     lenet = "lenet"


@app.post("/conn", status_code=200)
async def connection():
    return { "messege" : "Successfully Connected"}

@app.post("/start", status_code=200)
async def start_isystem():
    return { "messege" : "Successfully Started"}

'''
def get_or_create_task(task_id: str, response: Response):
    if task_id not in tasks:
        tasks[task_id] = "This didn't exist before"
        response.status_code = status.HTTP_201_CREATED
'''


@app.post("/stop", status_code=200)
async def stop_isystem():
    return { "messege" : "Successfully Stopped"}

@app.post("/pause", status_code=200)
async def pause_isystem():
    return { "messege" : "Successfully Paused"}
    


# ===========================================================================================================
# ===========================================================================================================

# @app.post("/items/", status_code=status.HTTP_201_CREATED)
# async def create_item(name: str):
#     return {"name": name}


# tasks = {"foo": "Listen to the Bar Fighters"}


# @app.put("/get-or-create-task/{task_id}", status_code=200)
# def get_or_create_task(task_id: str, response: Response):
#     if task_id not in tasks:
#         tasks[task_id] = "This didn't exist before"
#         response.status_code = status.HTTP_201_CREATED
#     return tasks[task_id]

# # 순서 문제 me 먼저 선언해야함
# @app.get("/users/me")
# async def read_user_me():
#     return {"user_id": "the current user"}


# @app.get("/users/{user_id}")
# async def read_user(user_id: str):
#     return {"user_id": user_id}


# @app.get("/models/{model_name}")
# async def get_model(model_name: ModelName):
#     if model_name is ModelName.alexnet:
#         return {"model_name": model_name, "message": "Deep Learning FTW!"}

#     if model_name.value == "lenet":
#         return {"model_name": model_name, "message": "LeCNN all the images"}

#     return {"model_name": model_name, "message": "Have some residuals"}
import base64
import json
import os
from io import BytesIO

import requests
from PIL import Image


def send_file_post(ip: str, path, file_path):
    url = 'http://' + ip + path
    upload = {'file': open(file_path, "rb")}
    return requests.post(url, files=upload)


def send_file_put(ip: str, path, file_path):
    url = 'http://' + ip + path
    upload = {'file': open(file_path, "rb")}
    return requests.put(url, files=upload)


def send_api(ip: str, path: str, method: str):
    url = 'http://' + ip + path
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}

    method = method.upper()
    try:
        if method == 'GET':
            return requests.get(url, headers=headers)
        elif method == 'POST':
            return requests.post(url, headers=headers)
        elif method == 'PUT':
            return requests.put(url, headers=headers)
        elif method == 'DELETE':
            return requests.delete(url, headers=headers)
    except Exception as ex:
        print(ex)


def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)


# 이미지 파일 저장하기
def saveImageFile(filestring, savePath):
    create_folder(os.path.dirname(savePath))

    imgFile = filestring.encode("utf-8")
    im = Image.open(BytesIO(base64.b64decode(imgFile)))
    im.save(savePath)


# 로그 파일 initialize
def logFileInit(directory):
    # 이미지 파일들 리스트
    imageFileList = os.listdir(directory)
    # 이미지 딕셔너리 만듦
    imageDict = {}
    for image in imageFileList:
        imageDict[image] = {}

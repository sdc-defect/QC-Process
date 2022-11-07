import sys

import requests
import json

from PyQt5 import QtCore, QtWebSockets, QtNetwork
from PyQt5.QtCore import QUrl, QCoreApplication, QTimer
from PyQt5.QtWidgets import QApplication

from utils.dto import InferenceResult
from utils.data import reverse_transfer_image, base64_to_image



def send_api(path, method):
    API_HOST = "http://127.0.0.1:8000"
    url = API_HOST + path
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
    body = {
        "key1": "value1",
        "key2": "value2"
    }
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers, data=json.dumps(body, ensure_ascii=False, indent="\t"))
        print("response status %r" % response.status_code)
        print("response text %r" % response.text)
    except Exception as ex:
        print(ex)

class Client(QtCore.QObject):
    def __init__(self, parent):
        super().__init__(parent)

        self.client = QtWebSockets.QWebSocket("",QtWebSockets.QWebSocketProtocol.Version13,None)
        self.client.error.connect(self.error)

        self.client.open(QUrl("ws://127.0.0.1:8000/ws"))
        self.client.pong.connect(self.onPong)
        self.client.textMessageReceived.connect(self.handle_message)

    def do_ping(self):
        print("client: do_ping")
        # payload = {
        #     InferenceResult.timestamp: str,
        #     InferenceResult.prob: [float],
        #     InferenceResult.label: int,
        #     InferenceResult.img: np.ndarray,
        #     InferenceResult.cam: np.ndarray,
        #     InferenceResult.merged: np.ndarray,
        # }
        # self.client.ping(payload)
        self.client.ping(b"foo")

    def send_message(self):
        print("client: send_message")
        self.client.sendTextMessage("asd")
        
    def handle_message(self, message):
        msg = json.loads(message)
        test = reverse_transfer_image(msg)

    def onPong(self, elapsedTime, payload):
        # payload = InferenceResult(timestamp, prob, label, img, cam, merged)
        # payload1 = payload
        # # {
        # #     InferenceResult.timestamp: str,
        # #     InferenceResult.prob: [float],
        # #     InferenceResult.label: int,
        # #     InferenceResult.img: np.ndarray,
        # #     InferenceResult.cam: np.ndarray,
        # #     InferenceResult.merged: np.ndarray,
        # # }
        print("onPong - time: {} ; payload: {}".format(elapsedTime, payload))

    def error(self, error_code):
        print("error code: {}".format(error_code))
        print(self.client.errorString())

    def close(self):
        self.client.close()


def quit_app():
    print("timer timeout - exiting")
    QCoreApplication.quit()

def ping():
    client.do_ping()

def send_message():
    client.send_message()

if __name__ == '__main__':
    global client
    app = QApplication(sys.argv)
    send_api("/start", "POST")

    QTimer.singleShot(2000, ping)
    QTimer.singleShot(3000, send_message)
    # QTimer.singleShot(5000, quit_app)
    
    client = Client(app)

    app.exec_()

    # self.client.pong.connect(self.onPong)

    # def onPong(self, elapsedTime, payload):
        # payload = {
        #     InferenceResult.timestamp: str,
        #     InferenceResult.prob: [float],
        #     InferenceResult.label: int,
        #     InferenceResult.img: np.ndarray,
        #     InferenceResult.cam: np.ndarray,
        #     InferenceResult.merged: np.ndarray,
        # }
    #     print("onPong - time: {} ; payload: {}".format(elapsedTime, payload))
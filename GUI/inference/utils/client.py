from PyQt5 import QtWebSockets
from PyQt5.QtCore import QUrl, pyqtSignal, QObject


class Client(QObject):
    signal = pyqtSignal(str)

    def __init__(self, address):
        super().__init__()
        self.client = QtWebSockets.QWebSocket("", QtWebSockets.QWebSocketProtocol.Version13, None)
        self.client.error.connect(self.error)

        # # self.client.open(QUrl("ws://127.0.0.1:8000/ws"))
        self.client.open(QUrl(address))
        # self.client.open(QUrl("ws://192.168.0.30:8080/ws"))
        self.client.textMessageReceived.connect(self.handle_message)

    def handle_message(self, message):
        # print("handle_message: ", type(message), len(message))
        self.signal.emit(message)

    def error(self, error_code):
        print("error code: {}".format(error_code))
        print(self.client.errorString())

    def close(self):
        self.client.close()

import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import os
from PyQt5 import QtCore, QtWidgets
# from PyQt5.QtCore import *
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
# graph lib
import pandas as pd
from pandas import Series
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import *
from PyQt5.QtChart import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtCore import *
from PyQt5.QtCore import pyqtSlot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.animation as animation
from matplotlib.figure import Figure
import random

# 출력 thread
import json
import time
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QWaitCondition
from PyQt5.QtCore import QMutex

# 웹소켓
import requests

from PyQt5 import QtCore, QtWebSockets, QtNetwork
from PyQt5.QtCore import QUrl, QCoreApplication, QTimer
from PyQt5.QtWidgets import QApplication

import logging
import base64
from PIL import Image
from io import BytesIO

from all_images import AllImageWindowClass
from inference_init import InferenceInitModal
# import inference_init

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.

form_class = uic.loadUiType("inference.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class InferenceWindowClass(QMainWindow, form_class) :
    inferenceDir = ""
    modelDir = ""
    singleInferenceDir = ""

    allFileLst = []
    okFileLst = []
    defFileLst = []

    allInferencedFile = {}
    okInferencedFile = {}
    defInferencedFile = {}

    yy = 0
    total = 0
    old_ts = 0
    a = 0

    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.initUI()
        # self.initLogger()
        
        # 그래프
        self.canvas = PlotCanvasLine(self, width=10, height=8)
        self.gridLayoutGraph.addWidget(self.canvas)
        self.x = np.arange(60)
        self.y = np.ones(60, dtype=np.float64)*np.nan
        self.line, = self.canvas.axes.plot(self.x, self.y, animated=True, color='red', lw=2)
        self.pushButtonControlStart.clicked.connect(self.on_start)
        self.pushButtonControlStop.clicked.connect(self.on_stop)
        # self.on_start()
            # window size
        # self.setMinimumSize(800, 800)
        self.series = QBarSeries()
        
        
            # chart object
        chart = QChart()
            # chart.legend().hide()
        chart.addSeries(self.series)
        chart.layout().setContentsMargins(0, 0, 0, 0)

            # self.resize(800, 600)

        chart.setTitle('수율')
        chart.setAnimationOptions(QChart.SeriesAnimations)

        dt = QDateTime.currentDateTime()
        self.ts = dt.toString('mm')

        months = (self.ts)

        axisX = QBarCategoryAxis()
        axisX.append('시간')

        axisY = QValueAxis()
        axisY.setRange(0, 500)

        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)
        self.series.attachAxis(axisX)
        self.series.attachAxis(axisY)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        self.chartView = QChartView(chart)
        
        self.gridLayoutGraph.addWidget(self.chartView)
        

        # 쓰레드 선언
        self.threadRecieve = receiveThread()
        self.threadRecieve.start()

        
    def init_widget(self):
        # 시그널 슬롯 연결
        self.threadWebsocket.recieved_message.connect(self.logSave)


    # 웹소켓에서 데이터 받았을 때 실행
    def logSave(self, logContext):

        imgDescription = json.loads(logContext.replace("'", "\""))

        


        # comma = ", "
        # logmessage = "Timestamp: " + imgDescription["timestamp"] + comma + "File name: " + imgDescription["filename"] + comma + "Probability_ok: " + imgDescription["prob"][0] + comma + "Probability_def : " + imgDescription["prob"][1] + comma + "Result : " + imgDescription["label"] if imgDescription["label"] is "ok" else "def" + comma + "Image_path: " + "imagePath111" + comma + "CAN_path: " + "canPath111" + comma + "Merged_path: " + "mergedPath111"
        

        # 이미지 파일 저장 위치 정하기
        imagePath = self.inferenceDir + '/image/' + imgDescription["filename"] + '.jpg'
        camPath = self.inferenceDir + '/cam/' + imgDescription["filename"] + '_cam.jpg'
        mergedPath = self.inferenceDir + '/merged/' + imgDescription["filename"] + '_merged.jpg'

        # 로그 파일 저장용
        logMessage = {
            "Timestamp" : imgDescription["timestamp"],
            "File_name" : imgDescription["filename"] ,
            "Probability_ok" : str(imgDescription["prob"][0]),
            "Probability_def" : str(imgDescription["prob"][1]),
            "Result" : imgDescription["label"] if imgDescription["label"] is "ok" else "def" ,
            "Image_path" : imagePath,
            "CAM_path" : camPath,
            "Merged_path" : mergedPath
           }

        self.logUpdate("Timestamp: "+logMessage["Timestamp"]+", File_name: "+logMessage["File_name"]+", Probability_ok: "+logMessage["Probability_ok"]+", Probability_def: "+logMessage["Probability_def"]+", Result: "+logMessage["Result"]+", Image_path: "+logMessage["Image_path"]+", CAM_path: "+logMessage["CAM_path"]+", Merged_path: "+logMessage["Merged_path"]+"\n")
        self.get_data(logMessage)
        
        # 메인 화면 이미지 리스트에 계속 추가해주기
        # row = self.tableWidgetImageList.rowCount()-1
        # print(logMessage["File_name"])
        # self.tableWidgetImageList.setItem(row, 0, QTableWidgetItem(logMessage["File_name"]))
        # self.tableWidgetImageList.setItem(row, 1, QTableWidgetItem(logMessage["Timestamp"]))
        # self.tableWidgetImageList.setItem(row, 2, QTableWidgetItem(logMessage["Result"]))
        # self.tableWidgetImageList.insertRow(row+1)

        row = self.tableWidgetLog.rowCount()-1
        self.tableWidgetLog.setItem(row, 0, QTableWidgetItem(logMessage["File_name"]))
        self.tableWidgetLog.setItem(row, 1, QTableWidgetItem(logMessage["Timestamp"]))
        self.tableWidgetLog.setItem(row, 2, QTableWidgetItem(logMessage["Probability_ok"]))
        self.tableWidgetLog.setItem(row, 3, QTableWidgetItem(logMessage["Probability_def"]))
        self.tableWidgetLog.setItem(row, 4, QTableWidgetItem(logMessage["Result"]))
        self.tableWidgetLog.insertRow(row+1)

        filename = logMessage["File_name"]
        # ui 프린트용 모든 파일 몰아넣기

        self.allInferencedFile[filename] = logMessage
        self.allFileLst.append(filename)
        if imgDescription["label"] == "1": # 양품
            self.okInferencedFile[filename] = logMessage
            self.okFileLst.append(filename)
        else: # 불량
            self.defInferencedFile[filename] = logMessage
            self.defFileLst.append(filename)
        
        logger = self.initLogger("Inferenced")
        logger.info(logMessage)

        # 이미지 파일 jpg로 변환해서 저장
        self.saveImageFile(imgDescription["img"], imagePath)
        self.saveImageFile(imgDescription["cam"], camPath)
        self.saveImageFile(imgDescription["merged"], mergedPath)
    
    # 이미지 파일 저장하기
    def saveImageFile(self, filestring, savePath):
        imgFile = filestring.encode("utf-8")
        im = Image.open(BytesIO(base64.b64decode(imgFile)))
        im.save(savePath)


    def logUpdate(self, logContext):
        print("logUdate")
        self.textBrowserLogContent.append(logContext)

    # 초기화
    def initUI(self):
        _openFile = QtWidgets.QAction("다른 파일 열기", self)
        _openModel = QtWidgets.QAction("모델 열기", self)
        
        # Menu Bar Settings
        menu = self.menuBar()
        _file = menu.addMenu("파일")
        _file.addAction(_openFile)
        _file.addAction(_openModel)

        # Connect Actions
        _openFile.triggered.connect(self.editFileDir)
        _openModel.triggered.connect(self.editModelDir)

        # table setting
        # self.tableWidgetImageList.setColumnCount(3)
        # self.tableWidgetImageList.setHorizontalHeaderLabels(['File Name', 'Created Time', 'Result'])
        # self.tableWidgetImageList.insertRow(0)
        # self.tableWidgetImageList.horizontalHeaderItem(0).setToolTip("코드...")
        # self.tableWidgetImageList.setColumnWidth(0, self.tableWidgetImageList.width()*2/5)
        # self.tableWidgetImageList.setColumnWidth(1, self.tableWidgetImageList.width()*2/5)
        # self.tableWidgetImageList.setColumnWidth(2, self.tableWidgetImageList.width()*1/5)

        self.pushButtonLogClear.clicked.connect(self.clickLogClear)

        # log table setting
        self.tableWidgetLog.clicked.connect(self.clickTableImages)
        self.tableWidgetLog.setColumnCount(5)
        self.tableWidgetLog.setHorizontalHeaderLabels(['File Name', 'Created Time', 'Probability_ok', 'Probability_def', 'Result'])
        self.tableWidgetLog.insertRow(0)
        self.tableWidgetLog.horizontalHeaderItem(0).setToolTip("코드...")

        self.tableWidgetLog.setColumnWidth(0, self.tableWidgetLog.width()*1/5)
        self.tableWidgetLog.setColumnWidth(1, self.tableWidgetLog.width()*1/5)
        self.tableWidgetLog.setColumnWidth(2, self.tableWidgetLog.width()*1/5)
        self.tableWidgetLog.setColumnWidth(3, self.tableWidgetLog.width()*1/5)
        self.tableWidgetLog.setColumnWidth(4, self.tableWidgetLog.width()*1/6)

        # 이미지 미리보기
        self.pushButtonOpenSingleImageDir.clicked.connect(self.showSingleImage)

        # 추론 모든 이미지 보기
        self.pushButtonAllListShow.clicked.connect(self.allImagesWindowOpen)

        # 개별 이미지 추론 시작 버튼
        self.pushButtonSingleStartInference.clicked.connect(self.singleStartInference)

        # 전체 이미지 추론 시작 버튼
        self.pushButtonControlStart.clicked.connect(self.allStartInference)
        # 전체 이미지 추론 정지 버튼
    
        self.pushButtonControlStop.clicked.connect(self.allStopInference)
    
    # 로그창 초기화
    def clickLogClear(self):
        self.textBrowserLogContent.clear()

    # 로깅 초기화
    def initLogger(self, logger_name):
        self.logger = logging.getLogger(logger_name)
        if len(self.logger.handlers) > 0:
            return self.logger

        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(message)s")

        streamHandler = logging.StreamHandler()
        streamHandler.setLevel(logging.INFO)
        streamHandler.setFormatter(formatter)

        file_handler = logging.FileHandler('test.log')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        self.logger.addHandler(streamHandler)
        return self.logger

    # 테이블 클릭시 이미지 띄우기
    def clickTableImages(self):
        row = self.tableWidgetLog.currentIndex().row()
        filename = self.tableWidgetLog.item(row, 0).text()
        detail = self.allInferencedFile[filename]

        imageDir = detail["Image_path"]
        camDir = detail["CAM_path"]
        self.singleInferenceDir = detail["Image_path"]
        self.labelSingleImageDir.setText(detail["Image_path"])
        # mergedDir = detail["Merged_path"]

        imageDirPixmap = QPixmap(imageDir)
        camDirPixmap = QPixmap(camDir)
        self.labelSingleImageShow.setPixmap(imageDirPixmap)
        self.labelSingleCAMShow.setPixmap(camDirPixmap)
    

    # 모달 창 - 모든 이미지 파일 리스트
    def allImagesWindowOpen(self):
        self.allImages = AllImageWindowClass(self.allInferencedFile, self.allFileLst, self.okInferencedFile, self.okFileLst, self.defInferencedFile, self.defFileLst)
        self.allImages.show()


    # 메뉴에 파일 다시 열기 누르면
    def editFileDir(self):
        fname = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if fname:
            self.inferenceDir = fname
            self.textBrowserImageFile.setText(fname)

            self.textBrowserFileDir.clear()
            # self.textBrowserFileDir.append("<")

        # initModal = InferenceInitModal()
        # initModal.exec_()
        # self.inferenceDir = initModal.inferenceDir
        # self.textBrowserImageFile.setText(self.inferenceDir)

    # 메뉴에 모델 열기 누르면
    def editModelDir(self):
        # fname = QFileDialog.getOpenFileName(self, '', 'Open file', 'ONNX(.onnx)') # 확장자 정해지면 설정하기
        fname = QFileDialog.getOpenFileName(self, '', 'Open file')
        
        if fname:
            self.modelDir = fname[0]
            self.textBrowserModelFile.setText(fname[0])


    # 로그 파일 initialize
    def logFileInit(self, directory):
        # 이미지 파일들 리스트
        imageFileList = os.listdir(directory)
        # 이미지 딕셔너리 만듦
        imageDict = {}
        for image in imageFileList:
            imageDict[image] = {}

    # 이미지 미리보기
    def showSingleImage(self):
        
        fname = QFileDialog.getOpenFileName(self, '', 'Open file')
        # fname = QFileDialog.getOpenFileName(self, '', 'Open file', 'ONNX(.onnx)') # 확장자 정해지면 설정하기
        if fname:
            self.labelSingleImageDir.setText(fname[0])

            singleImageDir = fname[0]
            self.singleInferenceDir = singleImageDir
            pixmap = QPixmap(singleImageDir)
            self.labelSingleImageShow.setPixmap(pixmap)

            self.labelSingleCAMShow.clear()
            self.labelSingleCAMShow.setText(singleImageDir)

        # self.labelSingleCAMShow = QLabel()
        # self.labelSingleCAMShow.setText("happy")

    # 개별 이미지 추론 시작
    def singleStartInference(self):
        # self.singleInferenceDir # 이미지 위치..
        pass

    # 모든 이미지 추론 시작
    @pyqtSlot()
    def allStartInference(self):
        # 사용자 지정 dir에 image, cam, merged 파일 없으면 만듦
        if "image" not in os.listdir(self.inferenceDir):
            os.mkdir(self.inferenceDir + "/image")
        if "cam" not in os.listdir(self.inferenceDir):
            os.mkdir(self.inferenceDir + "/cam")
        if "merged" not in os.listdir(self.inferenceDir):
            os.mkdir(self.inferenceDir + "/merged")

        self.threadWebsocket = Client()
        self.threadWebsocket.start()
        self.init_widget()
        self.threadWebsocket.toggle_status()
        self.startInfInit()
        self.textBrowserLogContent.append("Inference started\n")
    

    def startInfInit(self):
        self.pushButtonControlPause.clicked.connect(self.pauseInference)
        #self.pushButtonControlStatus.clicked.connect(self.statusInference)
        self.pushButtonControlRestart.clicked.connect(self.restartInference)

    # 모든 이미지 추론 정지
    def allStopInference(self):
        print("stop")
        self.textBrowserLogContent.append("Inference stoped\n")
        self.threadWebsocket.websocketFinish()
        self.threadWebsocket.stopThread()

    def pauseInference(self):
        #self.threadWebsocket.websocketFinish()
        self.textBrowserLogContent.append("Inference paused\n")
        self.threadWebsocket.pause_inference()

    # def statusInference(self):
    #     self.textBrowserLogContent.append("Inference status checked")
    #     self.threadWebsocket.status_inference()
    
    def restartInference(self):
        self.textBrowserLogContent.append("Inference restarted\n")
        self.threadWebsocket.restart_inference()
    

    def closeEvent(self, event):
        try:
            self.pauseInference()
            self.threadWebsocket.stopThread()
        except AttributeError:
            pass
        
        
    def get_data(self, log):
        if type(log) == dict:
            if log['Result'] == 'def':
                self.yy += 1
            self.total += 1
            dt = QDateTime.currentDateTime()
            ts = dt.toString('mm')
            # print(log)
        if ts != self.old_ts:
            self.old_ts = ts
        
    
    def update_line(self, i):
        y = self.yy / self.total if self.yy != 0 else 0
        old_y = self.line.get_ydata()
        new_y = np.r_[old_y[1:], y]
        self.line.set_ydata(new_y)
    
        # print(self.y)
        return [self.line]

    def update_line2(self, i):
        pass
        y2 = random.randint(0,510)
        old_y2 = self.line2.get_ydata()
        new_y2 = np.r_[old_y2[1:], y2]
        self.line2.set_ydata(new_y2)
        return [self.line2]
    
    def on_start(self):
        self.ani = animation.FuncAnimation(self.canvas.figure, self.update_line,blit=True, interval=25)

    
    def on_stop(self):
        self.ani._stop()
    
    def get_result(self, cur_result):
        
        dt = QDateTime.currentDateTime()
        # self.statusBar().showMessage(dt.toString('mm'))
        self.ticks[dt] = cur_result

        # # check whether minute changed
        # #if dt.time().minute() != self.minute_cur.time().minute():

        ts = dt.toString('mm')
        print(ts, cur_result, type(cur_result))
        
        if len(self.series.barSets())>0:
            self.a=self.series.barSets()[-1]
            print(self.series.take(self.a))
        if self.a!=0:
            cur_result=cur_result+int(self.a[0])
        new_set = QBarSet(f'{ts}')
        if self.a!=0 and new_set.label()!=a.label():
            self.series.append(self.a)
            # new_set[0]= 0
            cur_result = 0
        new_set << cur_result
        self.series.append(new_set)
        self.chartView.update()
        print('sum=',new_set[0], type(new_set[0]))
        print('count=',self.series.count())
    
    def firstAction(self):
        self.layout().removeWidget(self.lblAreaLine)
        # self.layout().removeWidget(self.lblAreaBar)
        self.lblAreaLine.setParent(None)
        # self.lblAreaBar.setParent(None)
        self.plotLine = WidgetPlotLine(self.centralwidget)  
        # self.plotBar = WidgetPlotBar(self.centralwidget)   
            
        self.gridLayoutGraph.addWidget(self.plotLine)
        # self.gridLayoutGraph.addWidget(self.plotBar)


# 그래프용 class
class WidgetPlotLine(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        
        # self.setLayout(QVBoxLayout())
        # self.canvas = PlotCanvasLine(self, width=10, height=8)
        
        
        # self.x = np.arange(50)
        # self.y = np.ones(50, dtype=np.float64)*np.nan
        # self.line, = self.canvas.axes.plot(self.x, self.y, animated=True, lw=2)
        # self.x2 = np.arange(50)
        # self.y2 = np.ones(50, dtype=np.float64)*np.nan
        # self.line2, = self.canvas.axes2.plot(self.x2, self.y2, animated=True,color='red', lw=2)
        
class PlotCanvasLine(FigureCanvas):
    def __init__(self, parent=None, width=8, height=8, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        
        self.axes = fig.add_subplot(xlim=(0, 60), ylim=(0, 1))
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['bottom'].set_position('center')
        self.axes.set_label('')
        
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, 
                QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    
    def plotLine(self):
        pass



class receiveThread(QThread, form_class):
    """
    데이터 받는 쓰레드
    (더미데이터를 1초 간격으로 emit 하는 것으로 시뮬레이션 중)
    데이터 수신 부분
    """
    # 사용자 정의 시그널 선언
    receive_inferenced_data = pyqtSignal(dict)
    update_log = pyqtSignal(str)

    def __init__(self):
        QThread.__init__(self)
        self.cond = QWaitCondition()
        self.mutex = QMutex()
        self._status = False # True로 바꿔야함
        self.input = {
            "filename":"2022_11_04_12_11_10_297", # .jpg , _can, _merge 추가해서 파일명 붙이기
            "timestamp": "2022-11-04_12:11:10:297",
            "prob": [0.7, 0.3][0],
            "label": 1,
            "img": "ccc",
            "cam": "bbb",
            "merged": "aaa",
        }
    
    def __del__(self):
        self.wait()

    def run(self):
        while True:
            
            print("allStartInference")
            self.mutex.lock()
            if not self._status:
                self.cond.wait(self.mutex)

            # for _ in range(10):
            print("receiveThread", input)
            self.receive_inferenced_data.emit(self.input)
        
        
            logDictContent = self.input

            logLabel = list(logDictContent.keys())
            print(logLabel)
            logPrintStr = "FileName, CreatedTime"
            for label in logLabel:
                logPrintStr = logPrintStr + ", " + str(label) + ": " + str(logDictContent[label])
            logPrintStr = logPrintStr + "\n"
            print(logPrintStr)

            self.update_log.emit(logPrintStr)
            
            # time.sleep(1)
            
            self.mutex.unlock()
    
    def toggle_status(self):
        self._status = not self._status
        if self._status:
            self.cond.wakeAll()
            
    @property
    def status(self):
        return self._status

# 웹소켓 websocket
def send_api(path, method):
    # API_HOST = "http://k7b306.p.ssafy.io:8080"
    API_HOST = "http://192.168.0.30:8080"
    url = API_HOST + path
    print(url)
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
    body = {
        "key1": "value1",
        "key2": "value2"
    }
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers, data=json.dumps(body, ensure_ascii=False, indent="\t"),verify=False)
        print("response status %r" % response.status_code)
        print("response text %r" % response.text)
    except Exception as ex:
        print(ex)

class Client(QThread, form_class):
    """통신용 쓰레드"""

    # 사용자 정의 시그널 선언 (dict로 바꿔주기@@@@@@)
    recieved_message = pyqtSignal(str)

    def __init__(self):
        QThread.__init__(self)
        self.cond = QWaitCondition()
        self.mutex = QMutex()
        self._status = False

        self.client = QtWebSockets.QWebSocket("",QtWebSockets.QWebSocketProtocol.Version13,None)
        self.client.error.connect(self.error)

        # # self.client.open(QUrl("ws://127.0.0.1:8000/ws"))
        # self.client.open(QUrl("ws://k7b306.p.ssafy.io:8080/ws"))
        self.client.open(QUrl("ws://192.168.0.30:8080/ws"))
        self.client.pong.connect(self.onPong)
        self.client.textMessageReceived.connect(self.handle_message)
        print("client")
        

    def run(self):
        # 에러처리
        
        while True:
            self.mutex.lock()

            # self.client.close()
            # print("client")
            # time.sleep(1)
            # print("state:",self.client.state()) # 정상 연결은 3, 연결 안됨은 0, 에러는 2
            if self.client.state()==0:
                print("not connected")

            if not self._status:
                self.cond.wait(self.mutex)
            self.mutex.unlock()

    def toggle_status(self):
        self._status = not self._status
        if self._status:
            self.cond.wakeAll()
    def websocketFinish(self):
        self._status = False
        self.client.close()

    @property
    def status(self):
        return self._status

    def __del__(self):
        self.wait()

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
        # message = json.loads(message)
        print("handle_message: ",type(message), len(message))
        # test = reverse_transfer_image(msg)
        self.recieved_message.emit(message)

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

    def pause_inference(self):
        response=send_api('/pause','POST')
        print(response)

    def restart_inference(self):
        response=send_api('/restart','POST')
        print(response)

    def status_inference(self):
        response=send_api('/status','GET')
        print(response)

    def stopThread(self):
        print('Thread Stop')
        self.power = False
        self.terminate()
        self.wait(3000)




def main():
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 
    # QTimer.singleShot(100000, quit_app)


    #WindowClass의 인스턴스 생성
    myWindow = InferenceWindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()
    
    myWindow.firstAction()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()



if __name__ == "__main__" :

    main()
















# 내용만 채워넣으면 됩니다 작동 함 (쓰레드에 변수 전달하는 예제)
# class saveThread(QThread, form_class):
#     """
#     데이터 저장하는 쓰레드
#     json 파일의 로그 저장, img, cam 이미지 저장
#     """
#     update_log = pyqtSignal(str)

#     def __init__(self, saveData):
#         QThread.__init__(self)
#         self.saveData = saveData
        
#     def run(self):
#         # print("saveThread:", self.saveData)
        
#         # logDictContent = self.saveData
#         # logDictContent["prob"] = self.saveData["prob"][0]

#         # logLabel = list(logDictContent.keys())
#         # print(logLabel)
#         # logPrintStr = ""
#         # for label in logLabel:
#         #     addLogStr = str(label) + ": " + str(logDictContent[label])
#         #     logPrintStr = logPrintStr + addLogStr + "\n"
#         # print(logPrintStr)
#         # self.update_log.emit(self.saveData)

#         time.sleep(1)


    
# class InferenceInitModal(QDialog, modal_form_class):
    
#     inferenceDir = ""
#     modelDir = ""

#     def __init__(self) :
#         super().__init__()
#         self.setupUi(self)
#         self.show()
#         self.initUI()
    

#     def initUI(self):
#         # 파일 열기 버튼 연결
#         self.pushButtonInferenceListDir.clicked.connect(self.clickOpenInferenceSet)
#         self.pushButtonModelDir.clicked.connect(self.clickModelFileSet)
#         # 완료 버튼 연결
#         self.pushButtonInitNext.clicked.connect(self.clickComplete)
    
#     # inference set 파일 경로 설정
#     def clickOpenInferenceSet(self):
#         fname = QFileDialog.getExistingDirectory(self, 'Select Directory')
#         self.inferenceDir = fname
#         self.labelInferenceListDir.setText(fname)

#     # model 파일 찾기
#     def clickModelFileSet(self):
#         fname = QFileDialog.getOpenFileName(self, '', 'Open file')
#         # fname = QFileDialog.getOpenFileName(self, '', 'Open file', 'ONNX(.onnx)') # 확장자 정해지면 설정하기
#         self.labelModelDir.setText(fname[0])
#         self.modelDir = fname[0]

#     # 화면 닫기
#     def clickComplete(self):

#         self.close()


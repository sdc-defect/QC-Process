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
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import *
from PyQt5.QtChart import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtCore import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.animation as animation
from matplotlib.figure import Figure

import json
import time
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QWaitCondition
from PyQt5.QtCore import QMutex

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

    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.initUI()
        
        # 그래프
        # self.axes = fig.add_subplot(211, xlim=(0, 50), ylim=(0, 1024))
        # self.axes2 = fig.add_subplot(212, xlim=(0, 50), ylim=(0, 600))
        # self.pushButtonAllListShow.clicked.connect(self.allImagesWindowOpen) # 모든 이미지 리스트 창 열기

        # 쓰레드 선언
        self.threadRecieve = receiveThread()
        self.init_widget()
        self.threadRecieve.start()
    
    def init_widget(self):
        # 시그널 슬롯 연결
        # self.threadRecieve.receive_inferenced_data.connect(self.saveThreadStart)
        self.threadRecieve.update_log.connect(self.logUpdate)

    # @pyqtSlot(dict)
    # def saveThreadStart(self, saveData):
    #     self.threadSave = saveThread(saveData)
    #     self.threadSave.update_log.connect(self.logUpdate)
    #     self.threadSave.start()

    def logUpdate(self, logContext):
        print("logUdate")
        self.textBrowserLogContent.append(logContext)

    # 초기화
    def initUI(self):
        _openFile = QtWidgets.QAction("다른 파일 열기", self)
        
        # Menu Bar Settings
        menu = self.menuBar()
        _file = menu.addMenu("파일")
        _file.addAction(_openFile)

        # Connect Actions
        _openFile.triggered.connect(self.editFileDir)

        # table setting
        self.tableWidgetImageList.setColumnCount(2)
        self.tableWidgetImageList.setHorizontalHeaderLabels(['FileName', 'CreatedTime'])
        self.tableWidgetImageList.horizontalHeaderItem(0).setToolTip("코드...")

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
        

        

    # 추론할 이미지 파일들 디렉토리 주소 가져오기 -> 없애고 이미지 가져오는거만 남겨놓기
    def imageFileDirButtonClicked(self):
        fname = QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.textBrowserImageFile.setText(fname)

        if fname: # 가져온 파일 안에 있는 파일 이름 가져오기 -> 큐로 보내줘야함..! 시작 버튼 눌렀을때로 옮겨야할듯
            images = {}
            images["dir"] = fname
            images["fileLst"] = os.listdir(fname)
            # print(os.listdir(fname))
            # for filename in os.listdir(fname):
            #     # images["fileLst"].append(filename)
            #     print(filename)
            #     # with open(os.path.join(fname, filename), 'r') as f: # 파일 내용 읽기
            #     #     text = f.read()
            #     #     print(text)
            # print(images)
    

    # 모달 창 - 모든 이미지 파일 리스트
    def allImagesWindowOpen(self):
        # 주소 어디에 있는지 정해지면 변경@@@@@@@@@@
        images = {}
        images["dir"] = self.inferenceDir
        images["fileLst"] = os.listdir(self.inferenceDir)
        # 주소 어디에 있는지 정해지면 변경@@@@@@@@@@

        self.allImages = AllImageWindowClass(images)
        self.allImages.show()

    # 로그 csv 파일 로그창에 출력하기
    def updateLog(self):
        nowDir = os.path.dirname(os.path.realpath(__file__)) # 현재 디렉토리 주소
        self.textBrowserLogContent.setText(nowDir) # 를 출력

        f=open(os.path.join(nowDir, '0_log.csv')) # 로그 파일 이름.. 변경해주기
        inp=f.read()
        print(len(inp))
        self.textBrowserLogContent.setText(inp)

        # with open(os.path.join(nowDir, '0_log'), 'r') as f: # 파일 내용 읽기
        #     text = f.read()
        #     print(text)


    # 메뉴에 파일 다시 열기 누르면
    def editFileDir(self):
        initModal = InferenceInitModal()
        initModal.exec_()

        self.inferenceDir = initModal.inferenceDir
        self.modelDir = initModal.modelDir

        self.textBrowserImageFile.setText(self.inferenceDir)
        self.textBrowserModelSaveFile.setText(self.modelDir)

        self.printImageListTable(self.inferenceDir)
    
    # 이미지 파일 위치 가져오면 바로 띄우기
    def printImageListTable(self, directory):
        
        if directory: # 가져온 파일 안에 있는 파일 이름 가져오기 -> 큐로 보내줘야함..! 시작 버튼 눌렀을때로 옮겨야할듯
            self.logFileInit(directory) # 로그 파일 생성

            self.imageList = os.listdir(directory) # -> 순서대로 추론에 보내줄 리스트

            images = {}
            images["dir"] = directory
            images["fileLst"] = self.imageList


        self.tableWidgetImageList.setRowCount(len(images["fileLst"]))

        for fileIdx in range(len(images["fileLst"])):
            self.tableWidgetImageList.setItem(fileIdx, 0, QTableWidgetItem(images["fileLst"][fileIdx]))


    # 로그 파일 initialize
    def logFileInit(self, directory):
        # 이미지 파일들 리스트
        imageFileList = os.listdir(directory)
        # 이미지 딕셔너리 만듦
        imageDict = {}
        for image in imageFileList:
            imageDict[image] = {}
        # 로그 json에 dict 저장
        file_path = "log.json" # 로그 파일 위치
        with open(file_path, "w") as json_file:
            json.dump(imageDict, json_file)

    # 이미지 미리보기
    def showSingleImage(self):
        
        fname = QFileDialog.getOpenFileName(self, '', 'Open file')
        # fname = QFileDialog.getOpenFileName(self, '', 'Open file', 'ONNX(.onnx)') # 확장자 정해지면 설정하기
        self.labelSingleImageDir.setText(fname[0])

        singleImageDir = fname[0]
        pixmap = QPixmap(singleImageDir)
        self.labelSingleImageShow.setPixmap(pixmap)

    # 개별 이미지 추론 시작
    def singleStartInference(self):
        pass

    # 모든 이미지 추론 시작
    @pyqtSlot()
    def allStartInference(self):
        self.threadRecieve.toggle_status()

    # 모든 이미지 추론 정지
    def allStopInference(self):
        pass
    
    # 그래프 플로팅
    def firstAction(self):
        self.layout().removeWidget(self.lblAreaLine)
        self.lblAreaLine.setParent(None)
        self.plotLine = WidgetPlotLine(self.centralwidget)
            
        self.gridLayoutGraph.addWidget(self.plotLine)
        # self.ani = animation.FuncAnimation(self.canvas.figure, self.update_line,blit=True, interval=25)

        
# 그래프용 Class 선언
class WidgetPlotLine(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.canvas = PlotCanvasLine(self, width=10, height=8)
        self.layout().addWidget(self.canvas)
        
class PlotCanvasLine(FigureCanvas):
    def __init__(self, parent=None, width=10, height=8, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.axes = fig.add_subplot(211, xlim=(0, 50), ylim=(0, 1024))
        self.axes2 = fig.add_subplot(212, xlim=(0, 50), ylim=(0, 600))
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, 
                QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()
        
    def plot(self):        
        self.x = np.arange(50)
        self.y = np.ones(50, dtype=np.float64)*np.nan
        self.line, = self.axes.plot(self.x, self.y, animated=True, lw=2)

        self.x2 = np.arange(50)
        self.y2 = np.ones(50, dtype=np.float64)*np.nan
        self.line2, = self.axes2.plot(self.x2, self.y2, animated=True,color='red', lw=2)

    def update_line(self, i):
        y = random.randint(0,1024)
        old_y = self.line.get_ydata()
        new_y = np.r_[old_y[1:], y]
        # time.sleep(10)
        self.line.set_ydata(new_y)
        
        # self.line.set_ydata(y)
        print(self.y)
        return [self.line]

    def update_line2(self, i):
        y2 = random.randint(0,510)
        old_y2 = self.line2.get_ydata()
        new_y2 = np.r_[old_y2[1:], y2]
        self.line2.set_ydata(new_y2)
        return [self.line2]
        # self.line.set_ydata(y)

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
        self.input = {"timestamp": "2022-11-04 12:11:10",
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
            
            time.sleep(1)
            
            self.mutex.unlock()
    
    def toggle_status(self):
        self._status = not self._status
        if self._status:
            self.cond.wakeAll()
            
    @property
    def status(self):
        return self._status


# 내용만 채워넣으면 됩니다 작동 함
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

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = InferenceWindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()
    
    myWindow.firstAction()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()


















    
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

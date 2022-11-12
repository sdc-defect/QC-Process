import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore, QtWidgets
import os
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QWaitCondition
from PyQt5.QtCore import QMutex
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
# graph lib
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import threading
import time
import csv

from training_init import TrainingInitWindowClass
from training_ratio import TrainingRatioWindowClass
from utils.dto import TrainConfig
from utils.trainer import Manager

import json

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("training.ui")[0]

# 그래프 띄워줄 데이터 import
log_data = pd.read_csv('./_log.csv')
log_data1=log_data['train_loss']
log_data2=log_data[ 'train_accuracy']
log_data3=log_data['train_recall']
# log_data4=log_data['train_f1']
log_data5=log_data['val_loss']
log_data6=log_data['val_accuracy']
log_data7=log_data['val_recall']
# log_data8=log_data['val_f1']

#화면을 띄우는데 사용되는 Class 선언
class trainingWindowClass(QMainWindow, form_class) :
    # set config data
    isSetFile = False
    config = TrainConfig(save_path=None, train_path=None, test_path=None, val_path=None)

    setAugmentation = True
    setFlip = True
    setSpin = True
    setSwift = True
    setMixup = True

    setEpoch = 50
    setBatchSize = 16
    setLearningRate = 0.0001
    setDecayStep = 1000

    trainSetDir = ""
    testSetDir = ""
    validationSetDir = ""
    modelSaveDir = ""

    trainFileCount = 0
    testFileCount = 0
    validationFileCount = 0

    def __init__(self) :
        # threading.Thread.__init__(self)
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Training")

        self.initUI()

        # 하이퍼파라미터 - 초기값 설정
        self.initHyperParameter()
        
        self.lblAreaAcc:QLabel
        self.lblAreaLoss:Qlabel
        self.lblAreaRecall:Qlabel
        
        
        # 쓰레드 선언
        self.th = Thread()
        self.init_widget()
        # 쓰레드 시작
        # self.th.start()

    def init_widget(self):
        # 시그널 슬롯 연결
        # self.pushButtonControlStart.clicked.connect(self.trainingStart)
        # self.th.change_value.connect(self.progressBar.setValue)
        self.th.change_value.connect(self.resultUpdate)
        self.th.update_log.connect(self.logUpdate)

    def resultUpdate(self, progress):
        self.progressBar.setValue(progress)

    def logUpdate(self, logContext):
        self.textBrowser.append(logContext + "\n")

    def test(self):
        print(self.setEpoch, self.setBatchSize, self.setLearningRate, self.setDecayStep)

    # 초기화
    def initUI(self):
        _openFile = QtWidgets.QAction("다른 파일 열기", self)
        
        # Menu Bar Settings
        menu = self.menuBar()
        _file = menu.addMenu("파일")
        _file.addAction(_openFile)

        # Connect Actions
        _openFile.triggered.connect(self.editFileDir)

        self.initData()

    # 파일 열기 모달 띄우기
    def editFileDir(self):
        initFirstModal = TrainingInitWindowClass()
        initFirstModal.exec_()

        if initFirstModal.fileSetdata != {}:
            self.config.save_path = initFirstModal.fileSetdata['save_path']
            self.config.train_path = initFirstModal.fileSetdata['train_path']
            self.config.test_path = initFirstModal.fileSetdata['test_path']
            self.config.val_path = initFirstModal.fileSetdata['val_path']
            self.isSetFile = True
     
    # 이벤트 연결
    def initData(self):

        # 어그멘테이션
        self.checkBoxAugmentation.stateChanged.connect(self.switchAugmentation)
        self.checkBoxFlip.stateChanged.connect(self.switchFlip)
        self.checkBoxSpin.stateChanged.connect(self.switchSpin)
        self.checkBoxSwift.stateChanged.connect(self.switchSwift)
        self.checkBoxMixup.stateChanged.connect(self.switchMixup)

        # 하이퍼파라미터
        self.spinBoxEpoch.valueChanged.connect(self.changeEpoch)
        self.comboBoxBatchSize.currentTextChanged.connect(self.changeBatchSize)
        self.horizontalSliderLearningRate.valueChanged.connect(self.changeLearningRate)
        self.comboBoxDecayStep.currentTextChanged.connect(self.changeDecayStep)

        self.lineEditBatchSize.textChanged.connect(self.customBatchSize)
        self.lineEditDecayStep.textChanged.connect(self.customDecayStep)
        
        self.comboBoxBatchSize.setCurrentText("16")
        self.comboBoxDecayStep.setCurrentText("1000")
        self.labelLearningRate.setText(str(self.setLearningRate))

        self.pushButtonControlStart.clicked.connect(self.trainingStart)
        self.pushButtonControlRestart.clicked.connect(self.trainingRestart)
        self.pushButtonControlPause.clicked.connect(self.trainingPause)
        self.pushButtonControlStop.clicked.connect(self.trainingStop)

        # 프로그래스바는 0부터 시작
        self.progressBar.setValue(0)
   
    # epoch
    def changeEpoch(self):
        # 5 단위만 되도록 할 지?
        epoch = self.spinBoxEpoch.value()
        if epoch%5 != 0: # 5의 배수 아니면 절삭
            epoch = epoch - epoch%5
            self.spinBoxEpoch.setValue(epoch)
        self.setEpoch = epoch
        
    # batch size
    def changeBatchSize(self):
        if self.comboBoxBatchSize.currentText() == "사용자 지정":
            self.lineEditBatchSize.setEnabled(True)
            self.lineEditBatchSize.setText(str(self.setBatchSize))
            self.setBatchSize = self.lineEditBatchSize.text()
        else:
            self.lineEditBatchSize.setEnabled(False)
            self.lineEditBatchSize.setText("")
            self.setBatchSize = self.comboBoxBatchSize.currentText()

    def customBatchSize(self):
        self.setBatchSize = self.lineEditBatchSize.text()

    # learning rate
    def changeLearningRate(self):
        self.setLearningRate = self.horizontalSliderLearningRate.value() / 10000
        self.labelLearningRate.setText(str(self.setLearningRate))

    # decay step
    def changeDecayStep(self):
        if self.comboBoxDecayStep.currentText() == "사용자 지정":
            self.lineEditDecayStep.setEnabled(True)
            self.lineEditDecayStep.setText(str(self.setDecayStep))
            self.setDecayStep = self.lineEditDecayStep.text()
        else:
            self.lineEditDecayStep.setEnabled(False)
            self.lineEditDecayStep.setText("")
            self.setDecayStep = self.comboBoxDecayStep.currentText()

    def customDecayStep(self):
        self.setDecayStep = self.lineEditDecayStep.text()

    # 하이퍼파라미터 - 초기값 설정
    def initHyperParameter(self):
        # 어그멘테이션 초기 - 전부 선택
        self.checkBoxAugmentation.setCheckState(2)
        self.checkBoxFlip.setCheckState(2)
        self.checkBoxSpin.setCheckState(2)
        self.checkBoxSwift.setCheckState(2)
        self.checkBoxMixup.setCheckState(2)

        self.switchAugmentation()

    # 어그멘테이션 전체 on/off 활성화 비활성화
    def switchAugmentation(self):
        self.setAugmentation  = self.checkBoxAugmentation.isChecked()
        isAugmentation = self.setAugmentation

        if isAugmentation:
            self.checkBoxFlip.setEnabled(True)
            self.checkBoxSpin.setEnabled(True)
            self.checkBoxSwift.setEnabled(True)
            self.checkBoxMixup.setEnabled(True)

            self.setAugmentation = True
            self.setFlip = self.checkBoxFlip.isChecked()
            self.setSpin = self.checkBoxSpin.isChecked()
            self.setSwift = self.checkBoxSwift.isChecked()
            self.setMixup = self.checkBoxMixup.isChecked()

        else:
            self.checkBoxFlip.setEnabled(False)
            self.checkBoxSpin.setEnabled(False)
            self.checkBoxSwift.setEnabled(False)
            self.checkBoxMixup.setEnabled(False)

            self.setAugmentation = False
            self.setFlip = False
            self.setSpin = False
            self.setSwift = False
            self.setMixup = False

    # 어그멘테이션 개별 on/off
    def switchFlip(self):
        self.setFlip = self.checkBoxFlip.isChecked()
    def switchSpin(self):
        self.setSpin = self.checkBoxSpin.isChecked()
    def switchSwift(self):
        self.setSwift = self.checkBoxSwift.isChecked()
    def switchMixup(self):
        self.setMixup = self.checkBoxMixup.isChecked()

    def changeProgressbar(self, progress):
        self.progressBar.setValue(progress)

    # 학습 시작
    @pyqtSlot()
    def trainingStart(self):
        # 어그멘테이션 설정
        if self.setAugmentation:
            self.config.flip = self.checkBoxFlip.isChecked()
            self.config.spin = self.checkBoxSpin.isChecked()
            self.config.shift = self.checkBoxSwift.isChecked()
            self.config.mixup = self.checkBoxMixup.isChecked()
        else:
            self.config.flip = False
            self.config.spin = False
            self.config.shift = False
            self.config.mixup = False

        # 하이퍼 파라미터 설정
        self.config.epoch = int(self.spinBoxEpoch.text())
        self.config.lr = float(self.labelLearningRate.text())

        if self.comboBoxBatchSize.currentText() == "사용자 지정":
            self.config.batch_size = int(self.lineEditBatchSize.text())
        else:
            self.config.batch_size = int(self.comboBoxBatchSize.currentText())

        if self.comboBoxDecayStep.currentText() == "사용자 지정":
            self.config.decay = int(self.lineEditDecayStep.text())
        else:
            self.config.decay = int(self.comboBoxDecayStep.currentText())

        print(self.config)
        # .json 파일 만들기
        config = json.loads(str(self.config))
        print(config)
        # self.th.toggle_status()
        # self.pushButtonControlStart.setText({True: "일시정지", False: "시작"}[self.th.status])
        
        # 시작 버튼 누르면 시작
        # if self.isSetFile:

        #     Manager().build_trainer(self.config)
        #     Manager().start(is_train=True)

        #     while True:
        #         if Manager().queue.empty():
        #             continue
        #         data = Manager().queue.get()

        #         # train, validation 종료
        #         if data == None: break
        #         print(data)

        return
    # 학습 다시시작
    def trainingRestart(self):
        pass

    # 학습 일시정지 - 없애고 시작 버튼으로 통일할 듯
    def trainingPause(self):
        pass
    
    # 학습 정지
    def trainingStop(self):
        pass

    # @staticmethod
    # def trainingStop():
    #     # 초기화 (재시작)
    #     trainingWindowClass.singleton = trainingWindowClass()
    # singleton: 'trainingWindowClass' = None

    # def updateLogLabel(self, progress):
    #     self.labelLog.setText("logText")
    #     print("asdasfa")
    #     print(progress)
    #     # self.labelLog.setText(str(90))
    
    # 그래프 플로팅
    def firstAction(self):
        self.layout().removeWidget(self.lblAreaLoss)
        self.layout().removeWidget(self.lblAreaAcc)
        self.layout().removeWidget(self.lblAreaRecall)
        self.lblAreaLoss.setParent(None)

        self.lblAreaAcc.setParent(None)
        self.lblAreaRecall.setParent(None)
        self.plotLoss = WidgetPlotLoss(self.centralwidget)  
        self.plotAcc = WidgetPlotAcc(self.centralwidget)   
        self.plotRecall = WidgetPlotRecall(self.centralwidget)      
            
        self.gridLayout.addWidget(self.plotLoss)
        self.gridLayout.addWidget(self.plotAcc)
        self.gridLayout.addWidget(self.plotRecall)
        
# 그래프용 Class 선언
class WidgetPlotLoss(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.canvas = PlotCanvasLoss(self, width=10, height=8)
        self.layout().addWidget(self.canvas)
        
class PlotCanvasLoss(FigureCanvas):
    def __init__(self, parent=None, width=10, height=8, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, 
                QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()
        
    def plot(self):        
        ax = self.figure.add_subplot(111)
        ax.plot(log_data1, color='#d62828', marker='o', linestyle='dashed', label='train_loss')
        ax.plot(log_data5, color='#003049', marker='o', linestyle='solid',label= 'val_loss')
        ax.grid(True,axis='y',linestyle='--')
        ax.legend(loc='best')
        ax.set_title('Loss')
        self.draw()

class WidgetPlotAcc(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.canvas = PlotCanvasAcc(self, width=10, height=8)
        self.layout().addWidget(self.canvas)
        
class PlotCanvasAcc(FigureCanvas):
    def __init__(self, parent=None, width=10, height=8, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, 
                QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plotacc()
        
    def plotacc(self):
        ax = self.figure.add_subplot(111)
        ax.plot(log_data2, color='#d62828', marker='o', linestyle='dashed', label='train_accuracy')
        ax.plot(log_data6, color='#003049', marker='o', linestyle='solid',label= 'val_accuracy')
        ax.grid(True,axis='y',linestyle='--')
        ax.legend(loc='best')
        ax.set_title('Accuracy')
        self.draw()
        
class WidgetPlotRecall(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.canvas = PlotCanvasRecall(self, width=10, height=8)
        self.layout().addWidget(self.canvas)
        
class PlotCanvasRecall(FigureCanvas):
    def __init__(self, parent=None, width=10, height=8, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, 
                QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plotrecall()
        
    def plotrecall(self):
        ax = self.figure.add_subplot(111)
        ax.plot(log_data3, color='#d62828', marker='o', linestyle='dashed', label='train_recall')
        ax.plot(log_data7, color='#003049', marker='o', linestyle='solid', label= 'val_recall')
        ax.grid(True,axis='y',linestyle='--')
        ax.legend(loc='best')
        ax.set_title('Recall')
        
        self.draw()
        
# 그래프 끝

# 결과 출력 쓰레드

class Thread(QThread, form_class):
    """
    단순히 0부터 100까지 카운트만 하는 쓰레드
    값이 변경되면 그 값을 change_value 시그널에 값을 emit 한다.
    """
    # 사용자 정의 시그널 선언
    change_value = pyqtSignal(int)
    update_log = pyqtSignal(str)
    def __init__(self):
        QThread.__init__(self)
        self.cond = QWaitCondition()
        self.mutex = QMutex()
        self.cnt = 0
        self._status = False # True로 바꿔야함
        print("threadProgress")

        self.logFileDir = "./_log.csv"

    def __del__(self):
        self.wait()

    def run(self):
        # 큐로 받을때 한 번만 실행하라고 while 없애면 될 듯?
        self.mut68ex.lock()

        if not self._status:
            self.cond.wait(self.mutex)

        if 100 == self.cnt:
            self.cnt = 0
        self.cnt += 1
        # self.change_value.emit(self.cnt)
        self.msleep(100)  # ※주의 QThread에서 제공하는 sleep을 사용

        # 파일에서 한 줄 씩 읽어와서 진행상황 출력
        f = open(self.logFileDir, 'r', encoding='utf-8')
        self.logCsv = list(csv.reader(f))
        f.close()

        logIndex = self.logCsv[0]
        logContent = self.logCsv[self.cnt]
        logIndexCount = len(logIndex)

        printContent = "Result" + str(self.cnt)
        for i in range(logIndexCount):
            addprintContent = logIndex[i] + ": " + logContent[i]
            printContent = printContent + ", " + addprintContent
        self.change_value.emit(int(self.logCsv[self.cnt][0])/int(trainingWindowClass.setEpoch)*100)
        
        self.update_log.emit(printContent)

        # print(self.cnt)

        self.msleep(1000)
        self.mutex.unlock()        

    def toggle_status(self):
        self._status = not self._status
        if self._status:
            self.cond.wakeAll()

    @property
    def status(self):
        return self._status

def main():
    app = QApplication(sys.argv) 
    myWindow = trainingWindowClass() 
    myWindow.show()
    myWindow.firstAction()
    exit(app.exec_())

if __name__ == "__main__" :
    main()

    # threadMain = threading.Thread(target=main)
    # # threadMain.setDaemon(True)
    # # threadLog = threading.Thread(target=showLog)

    # threadMain.start()
    # # showLogProgress()

    # threadLog.start()

    # #QApplication : 프로그램을 실행시켜주는 클래스
    # app = QApplication(sys.argv) 

    # #WindowClass의 인스턴스 생성
    # myWindow = trainingWindowClass() 

    # #프로그램 화면을 보여주는 코드
    # myWindow.show()

    # #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    # app.exec_()
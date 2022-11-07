import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore, QtWidgets
import os

import threading
import time
import csv

from training_init import TrainingInitWindowClass
from training_ratio import TrainingRatioWindowClass

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("training.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class trainingWindowClass(QMainWindow, form_class) :

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

        # self.threadclass = showLog()
        # self.threadclass.start()
        threadClass = showLogProgress(self)
        threadClass.start()

    # 파일 열기 모달 띄우기
    def editFileDir(self):
        # 첫 번째 모달
        initFirstModal = TrainingInitWindowClass()
        initFirstModal.exec_()

        self.trainSetDir = initFirstModal.trainSetDir
        self.testSetDir = initFirstModal.testSetDir
        self.validationSetDir = initFirstModal.validationSetDir
        self.modelSaveDir = initFirstModal.modelSaveDir

        self.trainFileCount = initFirstModal.trainFileCount
        self.testFileCount = initFirstModal.testFileCount
        self.validationFileCount = initFirstModal.validationFileCount

        # 두 번째 모달
        initSecondModal = TrainingRatioWindowClass(self.trainFileCount, self.testFileCount, self.validationFileCount)
        initSecondModal.exec_()

        self.trainFileCount = initSecondModal.train_cnt
        self.testFileCount = initSecondModal.test_cnt
        self.validationFileCount = initSecondModal.val_cnt

        self.labelTrainSetDir.setText(self.trainSetDir)
        self.labelTestSetDir.setText(self.testSetDir)
        self.labelValidationSetDir.setText(self.validationSetDir)
        self.labelModelSaveDir.setText(self.modelSaveDir)

        self.labelTrainSetCount.setText("(" + str(self.trainFileCount) + ")")
        self.labelTestSetCount.setText("(" + str(self.testFileCount) + ")")
        self.labelValidationSetCount.setText("(" + str(self.validationFileCount) + ")")
        
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

    # def changeProgressbar(self, progress):
    #     self.progressBar.setValue(progress)

    # 학습 시작
    def trainingStart(self):
        pass

    # 학습 다시시작
    def trainingRestart(self):
        pass

    # 학습 일시정자
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

    def updateLogLabel(self, progress):
        self.labelLog.setText("logText")
        print("asdasfa")
        print(progress)
        self.progressBar.setValue(90)
        

def main():
    app = QApplication(sys.argv) 
    myWindow = trainingWindowClass() 
    myWindow.show()
    app.exec_()

# class showLog(trainingWindowClass):
class showLogProgress(QtCore.QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.logFileDir = "C:/Users/multicampus/Desktop/3ssafy/reaaaal/GUI/training/_log.csv"
        # self.updateLogLabel()
        print("asdasfa")

    def run(self): 
        f = open(self.logFileDir, 'r', encoding='utf-8')
        self.logCsv = list(csv.reader(f))
        f.close()

        # print(self.logCsv[0])
        b=""
        for i in range(1, len(self.logCsv)):
            # print(self.logCsv[i][0])
            a = ""
            for j in range(len(self.logCsv[i])):
                a = a + ", " + self.logCsv[i][j]
                # print(self.logCsv[i])
            b = b + a + '\n'
            self.parent.labelLogContent.setText(b)

            nowEpoch = self.logCsv[i][0]
            # self.parent.updateLogLabel(int(nowEpoch))
            time.sleep(1)


    # def showProgress(self, nowEpoch):
    #     # totalEpoch = int(self.parent.setEpoch)
    #     totalEpoch = 100
    #     print((nowEpoch/totalEpoch)*100)
    #     progressRatio = (nowEpoch/totalEpoch)*100
    #     # self.parent.progressBar.setValue(12)

    


    # def __init__(self):
    #     self.logFileDir = "C:/Users/multicampus/Desktop/3ssafy/reaaaal/GUI/training/_log.csv"
    #     self.printLogFile()

    # def printLogFile(self):
    #     f = open(self.logFileDir, 'r', encoding='utf-8')
    #     logCsv = list(csv.reader(f))
    #     f.close()

    #     print(logCsv[0])
    #     logLabel = logCsv[0]
    #     # print(trainingWindowClass.labelParameter.text())
        
    #     # trainingWindowClass.labelLogContent.setText(logLabel)


if __name__ == "__main__" :
    # main()

    threadMain = threading.Thread(target=main)
    # threadMain.setDaemon(True)
    # threadLog = threading.Thread(target=showLog)

    threadMain.start()
    # showLogProgress()

    # threadLog.start()

    # #QApplication : 프로그램을 실행시켜주는 클래스
    # app = QApplication(sys.argv) 

    # #WindowClass의 인스턴스 생성
    # myWindow = trainingWindowClass() 

    # #프로그램 화면을 보여주는 코드
    # myWindow.show()

    # #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    # app.exec_()
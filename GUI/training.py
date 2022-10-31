import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore, QtWidgets
import os

from training_init import TrainingInitWindowClass

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("training.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class trainingWindowClass(QMainWindow, form_class) :

    setEpoch = 0
    setBatchSize = 0
    setLearningRate = 0
    setDecayStep = 0

    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Training")

        self.initUI()

        self.pushButtonOpenImageFile.clicked.connect(self.imageFileDirButtonClicked) # 이미지파일선텍 클릭 이벤트

        # 하이퍼파라미터 - 초기값 설정
        self.initHyperParameter()

        # 하이퍼파라미터 변경 이벤트
        self.comboBoxEpoch.currentTextChanged.connect(self.changeEpoch)
        self.comboBoxBatchSize.currentTextChanged.connect(self.changeBatchSize)
        self.comboBoxLearningRate.currentTextChanged.connect(self.changeLearningRate)
        self.comboBoxDecayStep.currentTextChanged.connect(self.changeDecayStep)

        # 메뉴로 파일 변경하기 누르면
        self.actionOpen_other_File.toggled.connect(self.editFileDir)

    def test(self):
        print(self.setEpoch)

    # 초기화
    def initUI(self):
        _openFile = QtWidgets.QAction("다른 파일 열기", self)
        
        # Menu Bar Settings
        menu = self.menuBar()
        _file = menu.addMenu("파일")
        _file.addAction(_openFile)

        # Connect Actions
        _openFile.triggered.connect(self.editFileDir)




    # 추론할 이미지 파일들 디렉토리 주소 가져오기
    def imageFileDirButtonClicked(self):
        fname = QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.labelImageFile.setText(fname)

    # 하이퍼파라미터 - 초기값 설정
    def initHyperParameter(self):
        self.setEpoch = self.comboBoxEpoch.currentText()
        self.setBatchSize = self.comboBoxBatchSize.currentText()
        self.setLearningRate = self.comboBoxLearningRate.currentText()
        self.setDecayStep = self.comboBoxDecayStep.currentText()
        print(self.setEpoch, self.setBatchSize, self.setLearningRate, self.setDecayStep)

    # 하이퍼파라미터 - 콤보박스로 변경하기
    def changeEpoch(self):
        self.setEpoch = self.comboBoxEpoch.currentText()
        print(self.setEpoch)
    def changeBatchSize(self):
        self.setBatchSize = self.comboBoxBatchSize.currentText()
        print(self.setBatchSize)
    def changeLearningRate(self):
        self.setLearningRate = self.comboBoxLearningRate.currentText()
        print(self.setLearningRate)
    def changeDecayStep(self):
        self.setDecayStep = self.comboBoxDecayStep.currentText()
        print(self.setDecayStep)

    # 메뉴에 파일 다시 열기 누르면
    def editFileDir(self):
        self.trainingInit = TrainingInitWindowClass()
        self.trainingInit.show()


    

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = trainingWindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
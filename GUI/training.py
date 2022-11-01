import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import os

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

        self.pushButtonOpenImageFile.clicked.connect(self.imageFileDirButtonClicked) # 이미지파일선텍 클릭 이벤트

        # 하이퍼파라미터 - 초기값 설정
        self.initHyperParameter()

        # 하이퍼파라미터 변경 이벤트
        self.comboBoxEpoch.currentTextChanged.connect(self.changeEpoch)
        self.comboBoxBatchSize.currentTextChanged.connect(self.changeBatchSize)
        self.comboBoxLearningRate.currentTextChanged.connect(self.changeLearningRate)
        self.comboBoxDecayStep.currentTextChanged.connect(self.changeDecayStep)

    def test(self):
        print(self.setEpoch)

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
    

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = trainingWindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
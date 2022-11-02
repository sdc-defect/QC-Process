import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore, QtWidgets
import os

# from training_init import TrainingInitWindowClass

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
        # self.initHyperParameter()

        # 하이퍼파라미터 변경 이벤트
        # self.comboBoxEpoch.currentTextChanged.connect(self.changeEpoch)
        # self.comboBoxBatchSize.currentTextChanged.connect(self.changeBatchSize)
        # self.comboBoxLearningRate.currentTextChanged.connect(self.changeLearningRate)
        # self.comboBoxDecayStep.currentTextChanged.connect(self.changeDecayStep)

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
    # def initHyperParameter(self):
    #     self.setEpoch = self.comboBoxEpoch.currentText()
    #     self.setBatchSize = self.comboBoxBatchSize.currentText()
    #     self.setLearningRate = self.comboBoxLearningRate.currentText()
    #     self.setDecayStep = self.comboBoxDecayStep.currentText()
    #     print(self.setEpoch, self.setBatchSize, self.setLearningRate, self.setDecayStep)

    # 하이퍼파라미터 - 콤보박스로 변경하기
    # def changeEpoch(self):
    #     self.setEpoch = self.comboBoxEpoch.currentText()
    #     print(self.setEpoch)
    # def changeBatchSize(self):
    #     self.setBatchSize = self.comboBoxBatchSize.currentText()
    #     print(self.setBatchSize)
    # def changeLearningRate(self):
    #     self.setLearningRate = self.comboBoxLearningRate.currentText()
    #     print(self.setLearningRate)
    # def changeDecayStep(self):
    #     self.setDecayStep = self.comboBoxDecayStep.currentText()
    #     print(self.setDecayStep)

    # 메뉴에 파일 다시 열기 누르면
    def editFileDir(self):
        self.trainingInit = TrainingInitWindowClass()
        self.trainingInit.show()


# ----------------------------------------------------------------------------------------------------
#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
init_form_class = uic.loadUiType("training_init.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class TrainingInitWindowClass(QMainWindow, init_form_class) :

    trainSetDir = ""
    testSetDir = ""
    validationSetDir = ""
    modelSaveDir = ""

    trainFileCount = 0
    testFileCount = 0
    validationFileCount = 0

    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Init")

        self.initialization()

        self.pushButtonTrainListDir.clicked.connect(self.clickOpenTrainSet)
        self.pushButtonTestListDir.clicked.connect(self.clickOpenTestSet)
        self.pushButtonValidationListDir.clicked.connect(self.clickOpenValidationSet)

        self.checkBoxTest.clicked.connect(self.changeComboTest)
        self.checkBoxValidation.clicked.connect(self.changeComboValidation)

        self.pushButtonInitNext.clicked.connect(self.clickNextButton)

    # 초기 체크 안되고 비활성화함
    def initialization(self):
        self.checkBoxTest.setChecked(False)
        self.checkBoxValidation.setChecked(False)
        self.pushButtonTestListDir.setEnabled(self.checkBoxTest.isChecked())
        self.pushButtonValidationListDir.setEnabled(self.checkBoxValidation.isChecked())
        self.labelTestListDir.setStyleSheet("Color : gray")
        self.labelValidationListDir.setStyleSheet("Color : gray")
        self.labelTestCount.setStyleSheet("Color : gray")
        self.labelValidationCount.setStyleSheet("Color : gray")
        self.labelTestSet.setStyleSheet("Color : gray")
        self.labelValidationSet.setStyleSheet("Color : gray")

    # 체크박스 눌러서 비활성화, 활성화
    def changeComboTest(self):
        print(self.trainSetDir, self.testSetDir, self.validationSetDir)
        if self.checkBoxTest.isChecked():
            self.pushButtonTestListDir.setEnabled(self.checkBoxTest.isChecked())
            self.testSetDir = self.labelTestListDir.text()
            self.testFileCount = int(self.labelTestCount.text()[1:-1])
            self.labelTestListDir.setStyleSheet("Color : black")
            self.labelTestCount.setStyleSheet("Color : black")
            self.labelTestSet.setStyleSheet("Color : black")
        else:
            self.pushButtonTestListDir.setEnabled(self.checkBoxTest.isChecked())
            self.testSetDir = ""
            self.testFileCount = 0
            self.labelTestListDir.setStyleSheet("Color : gray")
            self.labelTestCount.setStyleSheet("Color : gray")
            self.labelTestSet.setStyleSheet("Color : gray")

    def changeComboValidation(self):
        if self.checkBoxValidation.isChecked():
            self.pushButtonValidationListDir.setEnabled(self.checkBoxValidation.isChecked())
            self.validationSetDir = self.labelValidationListDir.text()
            self.validationFileCount = int(self.labelValidationCount.text()[1:-1])
            self.labelValidationListDir.setStyleSheet("Color : black")
            self.labelValidationCount.setStyleSheet("Color : black")
            self.labelValidationSet.setStyleSheet("Color : black")
        else:
            self.pushButtonValidationListDir.setEnabled(self.checkBoxValidation.isChecked())
            self.validationSetDir = ""
            self.validationFileCount = 0
            self.labelValidationListDir.setStyleSheet("Color : gray")
            self.labelValidationCount.setStyleSheet("Color : gray")
            self.labelValidationSet.setStyleSheet("Color : gray")

    
    # train set 파일 경로 설정, 파일 개수 출력
    def clickOpenTrainSet(self):
        fname = QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.trainSetDir = fname
        self.labelTrainListDir.setText(fname)

        fileCount = self.countFileNumber(fname)
        self.trainFileCount = fileCount
        self.labelTrainCount.setText("(" + str(fileCount) + ")")


    # test set 파일 경로 설정
    def clickOpenTestSet(self):
        fname = QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.testSetDir = fname
        self.labelTestListDir.setText(fname)

        fileCount = self.countFileNumber(fname)
        self.testFileCount = fileCount
        self.labelTestCount.setText("(" + str(fileCount) + ")")

    # validation set 파일 경로 설정
    def clickOpenValidationSet(self):
        fname = QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.validationSetDir = fname
        self.labelValidationListDir.setText(fname)

        fileCount = self.countFileNumber(fname)
        self.validationFileCount = fileCount
        self.labelValidationCount.setText("(" + str(fileCount) + ")")

    # 모델 저장할 위치 경로 설정
    def clickOpenModelSaveDir(self):
        fname = QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.modelSaveDir = fname
        self.labelModelSaveDir.setText(fname)

    # 디렉토리 내부 파일 개수 세기
    def countFileNumber(self, dir):
        fileCount = len(os.listdir(dir))
        return(fileCount)

    # 다음 버튼 누르면: 현재 모달 닫고 다음 모달 띄우기
    def clickNextButton(self):
        response = {
            "trainSetDir": self.trainSetDir, 
            "trainFileCount": self.trainFileCount,
            "testSetDir": self.testSetDir, 
            "testFileCount": self.testFileCount, 
            "validationSetDir": self.validationSetDir,
            "validationFileCount": self.validationFileCount,
            "modelSaveDir": self.modelSaveDir,
        }
        print(response)
        # self.ratioModal = 

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = trainingWindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
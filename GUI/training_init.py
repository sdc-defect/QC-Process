import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import os

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("training_init.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class TrainingInitWindowClass(QMainWindow, form_class) :

    trainSetDir = ""
    testSetDir = ""
    validationSetDir = ""

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

    # 초기 체크 안되고 비활성화함
    def initialization(self):
        self.checkBoxTest.setChecked(False)
        self.checkBoxValidation.setChecked(False)
        self.pushButtonTestListDir.setEnabled(self.checkBoxTest.isChecked())
        self.pushButtonValidationListDir.setEnabled(self.checkBoxValidation.isChecked())
        self.labelTestListDir.setStyleSheet("Color : gray")
        self.labelValidationListDir.setStyleSheet("Color : gray")

    # 체크박스 눌러서 비활성화, 활성화
    def changeComboTest(self):
        print(self.trainSetDir, self.testSetDir, self.validationSetDir)
        if self.checkBoxTest.isChecked():
            self.pushButtonTestListDir.setEnabled(self.checkBoxTest.isChecked())
            self.testSetDir = self.labelTestListDir.text()
            self.labelTestListDir.setStyleSheet("Color : black")
        else:
            self.pushButtonTestListDir.setEnabled(self.checkBoxTest.isChecked())
            self.testSetDir = ""
            self.labelTestListDir.setStyleSheet("Color : gray")

    def changeComboValidation(self):
        if self.checkBoxValidation.isChecked():
            self.pushButtonValidationListDir.setEnabled(self.checkBoxValidation.isChecked())
            self.validationSetDir = self.labelValidationListDir.text()
            self.labelValidationListDir.setStyleSheet("Color : black")
        else:
            self.pushButtonValidationListDir.setEnabled(self.checkBoxValidation.isChecked())
            self.validationSetDir = ""
            self.labelValidationListDir.setStyleSheet("Color : gray")

    # train set 파일 경로 설정
    def clickOpenTrainSet(self):
        fname = QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.trainSetDir = fname
        self.labelTrainListDir.setText(fname)

    # test set 파일 경로 설정
    def clickOpenTestSet(self):
        fname = QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.testSetDir = fname
        self.labelTestListDir.setText(fname)

    # validation set 파일 경로 설정
    def clickOpenValidationSet(self):
        fname = QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.validationSetDir = fname
        self.labelValidationListDir.setText(fname)

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = TrainingInitWindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
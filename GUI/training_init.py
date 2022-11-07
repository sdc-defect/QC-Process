
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import os

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
init_form_class = uic.loadUiType("training_init.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class TrainingInitWindowClass(QDialog, init_form_class) :

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

        # 버튼 클릭 시 이벤트 연결
        self.pushButtonTrainListDir.clicked.connect(self.clickOpenTrainSet)
        self.pushButtonTestListDir.clicked.connect(self.clickOpenTestSet)
        self.pushButtonValidationListDir.clicked.connect(self.clickOpenValidationSet)
        self.pushButtonModelSaveDir.clicked.connect(self.clickOpenModelSaveDir)


        self.checkBoxTest.clicked.connect(self.changeComboTest)
        self.checkBoxValidation.clicked.connect(self.changeComboValidation)

        self.pushButtonInitNext.clicked.connect(self.clickNextButton)

    def test(self):
        print("test")

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
        print("as")
        fname = QFileDialog.getExistingDirectory(self, 'Select Directory')
        print(fname)
        self.modelSaveDir = fname
        self.labelModelSaveDir.setText(fname)

    # 디렉토리 내부 파일 개수 세기
    def countFileNumber(self, dir):
        fileCount = len(os.listdir(dir))
        return(fileCount)

    # 다음 버튼 누르면: 현재 모달 닫고 다음 모달 띄우기
    def clickNextButton(self):
        # response = {
        #     "trainSetDir": self.trainSetDir, 
        #     "trainFileCount": self.trainFileCount,
        #     "testSetDir": self.testSetDir, 
        #     "testFileCount": self.testFileCount, 
        #     "validationSetDir": self.validationSetDir,
        #     "validationFileCount": self.validationFileCount,
        #     "modelSaveDir": self.modelSaveDir,
        # }
        # print(response)
        self.close()




    
    

    # 데코레이터 못하겠다 프린트하기
    # def printOutput(func):
    #     def wrapper():
    #         func()
    #         print("test:", func.trainSetDir, func.trainFileCount)
    #     return wrapper
    # def printout(self):
    #     print("train:", self.trainSetDir, self.trainFileCount)
    #     print("test:", self.testSetDir, self.testFileCount)
    #     print("validation:", self.validationSetDir, self.validationFileCount)
    

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = TrainingInitWindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
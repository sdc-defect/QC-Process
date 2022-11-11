import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import os
import glob

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
        # Train
        self.pushButtonOkTrainListDir.clicked.connect(self.clickOpenOkTrainSet)
        self.pushButtonDefTrainListDir.clicked.connect(self.clickOpenDefTrainSet)
        # Test
        self.pushButtonOkTestListDir.clicked.connect(self.clickOpenOkTestSet)
        self.pushButtonDefTestListDir.clicked.connect(self.clickOpenDefTestSet)
        # Val
        self.pushButtonOkValidationListDir.clicked.connect(self.clickOpenOkValidationSet)
        self.pushButtonDefValidationListDir.clicked.connect(self.clickOpenDefValidationSet)
        
        
        self.pushButtonModelSaveDir.clicked.connect(self.clickOpenModelSaveDir)
        self.checkBoxTest.clicked.connect(self.changeComboTest)
        self.checkBoxValidation.clicked.connect(self.changeComboValidation)

        self.pushButtonInitNext.clicked.connect(self.clickNextButton)
        
        # Test 비율 설정 값이 바뀔 때 호출
        self.spinBoxTotalRatioTestCount.valueChanged.connect(self.totalTestValueChanged)

        # Validation 비율 설정 값이 바뀔 때 호출
        self.spinBoxTotalRatioValidationCount.valueChanged.connect(self.totalValidationValueChanged)

    def test(self):
        print("test")

    # 초기 체크 안되고 비활성화함
    def initialization(self):
        # Test 
        self.checkBoxTest.setChecked(False)
        # ok
        self.pushButtonOkTestListDir.setEnabled(self.checkBoxTest.isChecked())
        self.labelOkTestCount.setStyleSheet("Color : gray")
        self.labelOkTestListDir.setStyleSheet("Color : gray")
        self.labelOkTestTitle.setStyleSheet("Color : gray")
        # def
        self.pushButtonDefTestListDir.setEnabled(self.checkBoxTest.isChecked())
        self.labelDefTestCount.setStyleSheet("Color : gray")
        self.labelDefTestListDir.setStyleSheet("Color : gray")
        self.labelDefTestTitle.setStyleSheet("Color : gray")

        # Val
        self.checkBoxValidation.setChecked(False)
        # ok
        self.pushButtonOkValidationListDir.setEnabled(self.checkBoxTest.isChecked())
        self.labelOkValidationCount.setStyleSheet("Color : gray")
        self.labelOkValidationListDir.setStyleSheet("Color : gray")
        self.labelOkValidationTitle.setStyleSheet("Color : gray")
        # def
        self.pushButtonDefValidationListDir.setEnabled(self.checkBoxTest.isChecked())
        self.labelDefValidationCount.setStyleSheet("Color : gray")
        self.labelDefValidationListDir.setStyleSheet("Color : gray")
        self.labelDefValidationTitle.setStyleSheet("Color : gray")  

    # 체크박스 눌러서 비활성화, 활성화
    def changeComboTest(self):
        print(self.trainSetDir, self.testSetDir, self.validationSetDir)
        if self.checkBoxTest.isChecked():
            # 직접 데이터를 주는 영역
            self.spinBoxTotalRatioTestCount.setEnabled(not self.checkBoxTest.isChecked())            
            self.labelTotalRatioTestCount.setStyleSheet("Color : gray")
            self.labelTotalRatioTestTitle.setStyleSheet("Color : gray")
            # ok
            self.pushButtonOkTestListDir.setEnabled(self.checkBoxTest.isChecked())
            self.labelOkTestCount.setStyleSheet("Color : black")
            self.labelOkTestListDir.setStyleSheet("Color : black")
            self.labelOkTestTitle.setStyleSheet("Color : black")
            # def
            self.pushButtonDefTestListDir.setEnabled(self.checkBoxTest.isChecked())
            self.labelDefTestCount.setStyleSheet("Color : black")
            self.labelDefTestListDir.setStyleSheet("Color : black")
            self.labelDefTestTitle.setStyleSheet("Color : black")
            
        else:
            # 직접 데이터를 주는 영역         
            self.spinBoxTotalRatioTestCount.setEnabled(not self.checkBoxTest.isChecked())            
            self.labelTotalRatioTestCount.setStyleSheet("Color : black")
            self.labelTotalRatioTestTitle.setStyleSheet("Color : black")
            # ok
            self.pushButtonOkTestListDir.setEnabled(self.checkBoxTest.isChecked())
            self.labelOkTestCount.setStyleSheet("Color : gray")
            self.labelOkTestListDir.setStyleSheet("Color : gray")
            self.labelOkTestTitle.setStyleSheet("Color : gray")
            # def
            self.pushButtonDefTestListDir.setEnabled(self.checkBoxTest.isChecked())
            self.labelDefTestCount.setStyleSheet("Color : gray")
            self.labelDefTestListDir.setStyleSheet("Color : gray")
            self.labelDefTestTitle.setStyleSheet("Color : gray")

    def changeComboValidation(self):
        if self.checkBoxValidation.isChecked():
            # select
            self.spinBoxTotalRatioValidationCount.setEnabled(not self.checkBoxValidation.isChecked())            
            self.labelTotalRatioValidationCount.setStyleSheet("Color : gray")
            self.labelTotalRatioValidationTitle.setStyleSheet("Color : gray")
            # ok
            self.pushButtonOkValidationListDir.setEnabled(self.checkBoxValidation.isChecked())
            self.labelOkValidationCount.setStyleSheet("Color : black")
            self.labelOkValidationListDir.setStyleSheet("Color : black")
            self.labelOkValidationTitle.setStyleSheet("Color : black")
            # def
            self.pushButtonDefValidationListDir.setEnabled(self.checkBoxValidation.isChecked())
            self.labelDefValidationCount.setStyleSheet("Color : black")
            self.labelDefValidationListDir.setStyleSheet("Color : black")
            self.labelDefValidationTitle.setStyleSheet("Color : black")
        else:
            # select
            self.spinBoxTotalRatioValidationCount.setEnabled(not self.checkBoxValidation.isChecked())            
            self.labelTotalRatioValidationCount.setStyleSheet("Color : black")
            self.labelTotalRatioValidationTitle.setStyleSheet("Color : black")
            # ok       
            self.pushButtonOkValidationListDir.setEnabled(self.checkBoxValidation.isChecked())
            self.labelOkValidationCount.setStyleSheet("Color : grey")
            self.labelOkValidationListDir.setStyleSheet("Color : grey")
            self.labelOkValidationTitle.setStyleSheet("Color : grey")
            # def
            self.pushButtonDefValidationListDir.setEnabled(self.checkBoxValidation.isChecked())
            self.labelDefValidationCount.setStyleSheet("Color : grey")
            self.labelDefValidationListDir.setStyleSheet("Color : grey")
            self.labelDefValidationTitle.setStyleSheet("Color : grey")

    # train set 파일 경로 설정, 파일 개수 출력
    def clickOpenOkTrainSet(self):
        fname = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if fname == '': return
        self.trainSetDir = fname
        self.labelOkTrainListDir.setText(fname)

        fileCount = self.countFileNumber(fname)
        self.trainFileCount = fileCount
        self.labelOkTrainCount.setText(f'{fileCount}')

        if self.labelOkTrainListDir.text() != '이미지 dir 위치' and self.labelDefTrainListDir.text() != '이미지 dir 위치':
            testFileCount = round(int(self.spinBoxTotalRatioTestCount.value())/ 100 * (self.countFileNumber(self.labelOkTrainListDir.text()) + self.countFileNumber(self.labelDefTrainListDir.text())))
            self.labelTotalRatioTestCount.setText(f'{testFileCount}')

            validationCount = round(int(self.spinBoxTotalRatioValidationCount.value())/ 100 * (self.countFileNumber(self.labelOkTrainListDir.text()) + self.countFileNumber(self.labelDefTrainListDir.text()) - testFileCount))
            self.labelTotalRatioValidationCount.setText(f'{validationCount}')

    def clickOpenDefTrainSet(self):
        fname = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if fname == '': return
        self.trainSetDir = fname
        self.labelDefTrainListDir.setText(fname)

        fileCount = self.countFileNumber(fname)
        self.trainFileCount = fileCount
        self.labelDefTrainCount.setText(f'{fileCount}')

        if self.labelOkTrainListDir.text() != '이미지 dir 위치' and self.labelDefTrainListDir.text() != '이미지 dir 위치':
            testFileCount = round(int(self.spinBoxTotalRatioTestCount.value())/ 100 * (self.countFileNumber(self.labelOkTrainListDir.text()) + self.countFileNumber(self.labelDefTrainListDir.text())))
            self.labelTotalRatioTestCount.setText(f'{testFileCount}')

            validationCount = round(int(self.spinBoxTotalRatioValidationCount.value())/ 100 * (self.countFileNumber(self.labelOkTrainListDir.text()) + self.countFileNumber(self.labelDefTrainListDir.text()) - testFileCount))
            self.labelTotalRatioValidationCount.setText(f'{validationCount}')

    # test set 파일 경로 설정
    def clickOpenOkTestSet(self):
        fname = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if fname == '': return
        self.testSetDir = fname
        self.labelOkTestListDir.setText(fname)

        fileCount = self.countFileNumber(fname)
        self.testFileCount = fileCount
        self.labelOkTestCount.setText(f'{fileCount}' )            

    def clickOpenDefTestSet(self):
        fname = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if fname == '': return
        self.testSetDir = fname
        self.labelDefTestListDir.setText(fname)

        fileCount = self.countFileNumber(fname)
        self.testFileCount = fileCount
        self.labelDefTestCount.setText(f'{fileCount}')

    # test에 있는 spinbox의 값이 바뀌었을 때 호출
    def totalTestValueChanged(self):
        if self.labelOkTrainListDir.text() == '이미지 dir 위치' or self.labelDefTrainListDir.text() == '이미지 dir 위치': return
        testFileCount = round(int(self.spinBoxTotalRatioTestCount.value())/ 100 * (self.countFileNumber(self.labelOkTrainListDir.text()) + self.countFileNumber(self.labelDefTrainListDir.text())))
        self.labelTotalRatioTestCount.setText(f'{testFileCount}')

        validationCount = round(int(self.spinBoxTotalRatioValidationCount.value())/ 100 * (self.countFileNumber(self.labelOkTrainListDir.text()) + self.countFileNumber(self.labelDefTrainListDir.text()) - testFileCount))
        self.labelTotalRatioValidationCount.setText(f'{validationCount}')
  
    # validation set 파일 경로 설정
    def clickOpenOkValidationSet(self):
        fname = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if fname == '': return
        self.labelOkValidationListDir.setText(fname)

        fileCount = self.countFileNumber(fname)
        self.labelOkValidationCount.setText(f'{fileCount}')        

    def clickOpenDefValidationSet(self):
        fname = QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.labelDefValidationListDir.setText(fname)

        fileCount = self.countFileNumber(fname)
        self.labelDefValidationCount.setText(f'{fileCount}')
        
    # 모델 저장할 위치 경로 설정
    def clickOpenModelSaveDir(self):
        print("as")
        fname = QFileDialog.getExistingDirectory(self, 'Select Directory')
        print(fname)
        self.modelSaveDir = fname
        self.labelModelSaveDir.setText(fname)

    #  Validation spinbox의 값이 바뀌었을 때 호출
    def totalValidationValueChanged(self):
        if self.labelOkTrainListDir.text() == '이미지 dir 위치' or self.labelDefTrainListDir.text() == '이미지 dir 위치': return
        testFileCount = round(int(self.spinBoxTotalRatioTestCount.value())/ 100 * (self.countFileNumber(self.labelOkTrainListDir.text()) + self.countFileNumber(self.labelDefTrainListDir.text())))

        validationCount = round(int(self.spinBoxTotalRatioValidationCount.value())/ 100 * (self.countFileNumber(self.labelOkTrainListDir.text()) + self.countFileNumber(self.labelDefTrainListDir.text()) - testFileCount))
        self.labelTotalRatioValidationCount.setText(f'{validationCount}')

    # 디렉토리 내부 이미지 개수 세기
    def countFileNumber(self, dir):
        print(dir)
        fileList = glob.glob(f'{dir}/*[png$|jpg$|jpeg$|tif$]')
        fileCount = len(fileList)
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
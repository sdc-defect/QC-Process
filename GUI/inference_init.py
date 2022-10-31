
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import os

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("inference_init.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class InferenceInitWindowClass(QMainWindow, form_class) :

    inferenceDir = ""
    modelDir = ""

    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("All")

        self.initUI()
    
    def initUI(self):
        self.pushButtonInferenceListDir.clicked.connect(self.clickOpenInferenceSet)
        self.pushButtonModelDir.clicked.connect(self.clickModelFileSet)

    # inference set 파일 경로 설정
    def clickOpenInferenceSet(self):
        fname = QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.inferenceDir = fname
        self.labelInferenceListDir.setText(fname)

    # model 파일 찾기
    def clickModelFileSet(self):
        fname = QFileDialog.getOpenFileName(self, '', 'Open file')
        # fname = QFileDialog.getOpenFileName(self, '', 'Open file', 'ONNX(.onnx)') # 확장자 정해지면 설정하기
        self.labelModelDir.setText(fname[0])

        


if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = InferenceInitWindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
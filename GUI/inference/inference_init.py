# #!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QStandardItemModel, QStandardItem
# from PyQt5 import QtCore, QtGui, QtWidgets

# from inference import WindowClass

import os

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_init = uic.loadUiType("inference_init_dialog.ui")[0]

class InferenceInitModal(QDialog, form_init):
    

    inferenceDir = ""
    modelDir = ""

    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.show()
        self.initUI()
    

    def initUI(self):
        # 파일 열기 버튼 연결
        self.pushButtonInferenceListDir.clicked.connect(self.clickOpenInferenceSet)
        self.pushButtonModelDir.clicked.connect(self.clickModelFileSet)
        
        # 완료 버튼 연결
        self.pushButtonInitNext.clicked.connect(self.clickComplete)
    
    # inference set 파일 경로 설정
    def clickOpenInferenceSet(self):
        fname = QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.inferenceDir = fname
        print("self.inferenceDir: ", self.inferenceDir)
        self.labelInferenceListDir.setText(fname)


    # model 파일 찾기
    def clickModelFileSet(self):
        fname = QFileDialog.getOpenFileName(self, '', 'Open file')
        # fname = QFileDialog.getOpenFileName(self, '', 'Open file', 'ONNX(.onnx)') # 확장자 정해지면 설정하기
        self.labelModelDir.setText(fname[0])
        self.modelDir = fname[0]


    # 화면 닫기
    def clickComplete(self):
        print("self.inferenceDir: ", self.inferenceDir)
        self.close()



if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = InferenceInitModal() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
    # sys.exit(app.exec_())













# import sys
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *

# class InferenceInitWindowClass(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         # 윈도우 설정
#         self.setGeometry(300, 300, 400, 300)  # x, y, w, h
#         self.setWindowTitle('Status Window')

#         # QButton 위젯 생성
#         self.button = QPushButton('Dialog Button', self)
#         self.button.clicked.connect(self.dialog_open)
#         self.button.setGeometry(10, 10, 200, 50)

#         # QDialog 설정
#         self.dialog = QDialog()

#     # 버튼 이벤트 함수
#     def dialog_open(self):
#         # 버튼 추가
#         btnDialog = QPushButton("OK", self.dialog)
#         btnDialog.move(100, 100)
#         btnDialog.clicked.connect(self.dialog_close)

#         # QDialog 세팅
#         self.dialog.setWindowTitle('Dialog')
#         self.dialog.setWindowModality(Qt.ApplicationModal)
#         self.dialog.resize(300, 200)
#         self.dialog.show()

#     # Dialog 닫기 이벤트
#     def dialog_close(self):
#         self.dialog.close()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     mainWindow = InferenceInitWindowClass()
#     mainWindow.show()
#     sys.exit(app.exec_())











    
#화면을 띄우는데 사용되는 Class 선언
# class InferenceInitWindowClass(QDialog, form_class) :

#     inferenceDir = ""
#     modelDir = ""

#     # 데이터를 전달하는 통로
#     command = pyqtSignal(list)

#     def __init__(self) :
#         super().__init__()
#         self.setupUi(self)
#         self.setWindowTitle("All")

#         self.initUI()
    
#     def initUI(self):
#         # self.dialog = QDialog()

#         self.pushButtonInferenceListDir.clicked.connect(self.clickOpenInferenceSet)
#         self.pushButtonModelDir.clicked.connect(self.clickModelFileSet)

#         # 완료 버튼 누르면 창 닫기
#         self.pushButtonInitNext.clicked.connect(self.clickComplete)
#         # self.pushButtonInitNext.clicked.connect(QCoreApplication.instance().quit)
        
    
#     def test(self):
#         print("test")

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

#     # 완료 버튼 누르기
#     def clickComplete(self):
#         # msgInferenceDir = self.inferenceDir
#         # self.command.emit(msgInferenceDir)

#         print("happy")
#         self.pushButtonInitNext.clicked.connect(self.sendCommand)

#     # @pyqtSlot()
#     def sendCommand(self):
#         msg = [self.inferenceDir, self.modelDir]
#         # self.command.emit(msg)
#         print(msg)
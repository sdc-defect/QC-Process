import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import os
from PyQt5 import QtCore, QtWidgets
# from PyQt5.QtCore import *
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap

from all_images import AllImageWindowClass
from inference_init import InferenceInitModal
# import inference_init

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.

form_class = uic.loadUiType("inference.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class InferenceWindowClass(QMainWindow, form_class) :
    inferenceDir = ""
    modelDir = ""

    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.updateLog()
        self.initUI()

        # self.pushButtonAllListShow.clicked.connect(self.allImagesWindowOpen) # 모든 이미지 리스트 창 열기


    # 초기화
    def initUI(self):
        _openFile = QtWidgets.QAction("다른 파일 열기", self)
        
        # Menu Bar Settings
        menu = self.menuBar()
        _file = menu.addMenu("파일")
        _file.addAction(_openFile)

        # Connect Actions
        _openFile.triggered.connect(self.editFileDir)

        # table setting
        self.tableWidgetImageList.setColumnCount(2)
        self.tableWidgetImageList.setHorizontalHeaderLabels(['FileName', 'CreatedTime'])
        self.tableWidgetImageList.horizontalHeaderItem(0).setToolTip("코드...")

        # 이미지 미리보기
        self.pushButtonOpenSingleImageDir.clicked.connect(self.showSingleImage)

        # 추론 모든 이미지 보기
        self.pushButtonAllListShow.clicked.connect(self.allImagesWindowOpen)

        # 개별 이미지 추론 시작 버튼
        self.pushButtonSingleStartInference.clicked.connect(self.singleStartInference)

        # 전체 이미지 추론 시작 버튼
        self.pushButtonControlStart.clicked.connect(self.allStartInference)
        # 전체 이미지 추론 정지 버튼
        self.pushButtonControlStop.clicked.connect(self.allStopInference)
        

        

    # 추론할 이미지 파일들 디렉토리 주소 가져오기 -> 없애고 이미지 가져오는거만 남겨놓기
    def imageFileDirButtonClicked(self):
        fname = QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.textBrowserImageFile.setText(fname)

        if fname: # 가져온 파일 안에 있는 파일 이름 가져오기 -> 큐로 보내줘야함..! 시작 버튼 눌렀을때로 옮겨야할듯
            images = {}
            images["dir"] = fname
            images["fileLst"] = os.listdir(fname)
            # print(os.listdir(fname))
            # for filename in os.listdir(fname):
            #     # images["fileLst"].append(filename)
            #     print(filename)
            #     # with open(os.path.join(fname, filename), 'r') as f: # 파일 내용 읽기
            #     #     text = f.read()
            #     #     print(text)
            # print(images)
    

    # 모달 창 - 모든 이미지 파일 리스트
    def allImagesWindowOpen(self):
        # 주소 어디에 있는지 정해지면 변경@@@@@@@@@@
        images = {}
        images["dir"] = self.inferenceDir
        images["fileLst"] = os.listdir(self.inferenceDir)
        # 주소 어디에 있는지 정해지면 변경@@@@@@@@@@

        self.allImages = AllImageWindowClass(images)
        self.allImages.show()

    # 로그 csv 파일 로그창에 출력하기
    def updateLog(self):
        nowDir = os.path.dirname(os.path.realpath(__file__)) # 현재 디렉토리 주소
        self.textBrowserLogContent.setText(nowDir) # 를 출력

        f=open(os.path.join(nowDir, '0_log.csv')) # 로그 파일 이름.. 변경해주기
        inp=f.read()
        print(len(inp))
        self.textBrowserLogContent.setText(inp)

        # with open(os.path.join(nowDir, '0_log'), 'r') as f: # 파일 내용 읽기
        #     text = f.read()
        #     print(text)


    # 메뉴에 파일 다시 열기 누르면
    def editFileDir(self):
        initModal = InferenceInitModal()
        initModal.exec_()

        self.inferenceDir = initModal.inferenceDir
        self.modelDir = initModal.modelDir

        self.textBrowserImageFile.setText(self.inferenceDir)
        self.textBrowserModelSaveFile.setText(self.modelDir)

        self.printImageListTable(self.inferenceDir)
    
    # 이미지 파일 위치 가져오면 바로 띄우기
    def printImageListTable(self, directory):
        
        if directory: # 가져온 파일 안에 있는 파일 이름 가져오기 -> 큐로 보내줘야함..! 시작 버튼 눌렀을때로 옮겨야할듯
            images = {}
            images["dir"] = directory
            images["fileLst"] = os.listdir(directory)
            # for filename in os.listdir(directory):
            #     # images["fileLst"].append(filename)
            #     print(filename)
            #     # with open(os.path.join(fname, filename), 'r') as f: # 파일 내용 읽기
            #     #     text = f.read()
            #     #     print(text)
            # print(images)

        self.tableWidgetImageList.setRowCount(len(images["fileLst"]))

        for fileIdx in range(len(images["fileLst"])):
            self.tableWidgetImageList.setItem(fileIdx, 0, QTableWidgetItem(images["fileLst"][fileIdx]))

    # 이미지 미리보기
    def showSingleImage(self):
        
        fname = QFileDialog.getOpenFileName(self, '', 'Open file')
        # fname = QFileDialog.getOpenFileName(self, '', 'Open file', 'ONNX(.onnx)') # 확장자 정해지면 설정하기
        self.labelSingleImageDir.setText(fname[0])

        singleImageDir = fname[0]
        pixmap = QPixmap(singleImageDir)
        self.labelSingleImageShow.setPixmap(pixmap)

    # 개별 이미지 추론 시작
    def singleStartInference(self):
        pass

    # 모든 이미지 추론 시작
    def allStartInference(self):
        pass

    # 모든 이미지 추론 정지
    def allStopInference(self):
        pass


if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = InferenceWindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()


















    
# class InferenceInitModal(QDialog, modal_form_class):
    
#     inferenceDir = ""
#     modelDir = ""

#     def __init__(self) :
#         super().__init__()
#         self.setupUi(self)
#         self.show()
#         self.initUI()
    

#     def initUI(self):
#         # 파일 열기 버튼 연결
#         self.pushButtonInferenceListDir.clicked.connect(self.clickOpenInferenceSet)
#         self.pushButtonModelDir.clicked.connect(self.clickModelFileSet)
#         # 완료 버튼 연결
#         self.pushButtonInitNext.clicked.connect(self.clickComplete)
    
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

#     # 화면 닫기
#     def clickComplete(self):

#         self.close()


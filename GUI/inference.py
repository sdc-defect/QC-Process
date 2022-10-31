import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import os
from PyQt5.QtCore import *

from all_images import AllImageWindowClass


#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("inference.ui")[0]


#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :


    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.updateLog()

        self.pushButtonOpenImageFile.clicked.connect(self.imageFileDirButtonClicked) # 이미지파일선택 클릭 이벤트
        self.pushButtonOpenModelSaveFile.clicked.connect(self.modelFileButtonClicked) # 모델파일선택 클릭 이벤트

        self.pushButtonAllListShow.clicked.connect(self.allImagesWindowOpen) # 모든 이미지 리스트 창 열기


    # 추론할 이미지 파일들 디렉토리 주소 가져오기
    def imageFileDirButtonClicked(self):
        fname = QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.textBrowserImageFile.setText(fname)
        if fname: # 가져온 파일 안에 있는 파일 이름 가져오기 -> 큐로 보내줘야함..! 시작 버튼 눌렀을때로 옮겨야할듯
            
            global images
            # images = "hello!!!!!!!"
            images = {}

            images["dir"] = fname
            images["fileLst"] = os.listdir(fname)
            print(os.listdir(fname))
            for filename in os.listdir(fname):
                # images["fileLst"].append(filename)
                print(filename)
                
                # with open(os.path.join(fname, filename), 'r') as f: # 파일 내용 읽기
                #     text = f.read()
                #     print(text)
            print(images)
    
    # 사용할 모델 주소 가져오기
    def modelFileButtonClicked(self):
        fname = QFileDialog.getOpenFileName(self, '', 'Open file')
        # fname = QFileDialog.getOpenFileName(self, '', 'Open file', 'ONNX(.onnx)') # 확장자 정해지면 설정하기
        self.textBrowserModelSaveFile.setText(fname[0])


    # 창 열기 - 모든 이미지 파일 리스트
    def allImagesWindowOpen(self):
        
        global images
        self.allImages = AllImageWindowClass(images)
        self.allImages.show()
        # self.allImages.textBrowserSelectedImage.setText(text)

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




if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
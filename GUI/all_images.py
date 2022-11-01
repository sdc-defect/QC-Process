import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import os

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("all_images.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class AllImageWindowClass(QMainWindow, form_class) :
    def __init__(self, images) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("All")

        self.showList(images)

        global imageSourceDir
        imageSourceDir = images["dir"]
        global imageNameLst
        imageNameLst = images["fileLst"]

        # 리스트에서 이미지 선택할때..
        # imageDir = images["dir"] + "/"+ images["fileLst"][0]
        # self.showDetail(imageDir)

        # 테이블 클릭 이벤트
        self.tableWidgetAllFile.clicked.connect(self.clickTableAllImages)


    # 파일 리스트에 데이터 넣기
    def showList(self, images):
        self.tableWidgetAllFile.setColumnCount(2)
        self.tableWidgetAllFile.setRowCount(len(images["fileLst"]))
        print(len(images["fileLst"]))

        self.tableWidgetAllFile.setHorizontalHeaderLabels(['FileName', 'CreatedTime'])
        self.tableWidgetAllFile.horizontalHeaderItem(0).setToolTip("코드...")
        
        for fileIdx in range(len(images["fileLst"])):
            self.tableWidgetAllFile.setItem(fileIdx, 0, QTableWidgetItem(images["fileLst"][fileIdx]))

    # self.tableWidgetAllFile

    # 이미지, 내용 출력
    def showDetail(self, imageIdx):
        global imageSourceDir
        global imageNameLst

        imageDir = imageSourceDir + "/"+ imageNameLst[imageIdx]
        print(imageDir)

        pixmap = QPixmap(imageDir)
        self.imageOriginal.setPixmap(pixmap)

    # 테이블 클릭 이벤트
    def clickTableAllImages(self):
        row = self.tableWidgetAllFile.currentIndex().row()
        print(row)
        self.showDetail(row)

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = AllImageWindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
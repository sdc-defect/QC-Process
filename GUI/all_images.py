import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import os
from PyQt5.QtGui import QStandardItemModel

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("all_images.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class AllImageWindowClass(QMainWindow, form_class) :
    def __init__(self, images) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("All")

        # self.showList(images)

        # global imageSourceDir
        self.imageSourceDir = images["dir"]
        # global imageNameLst
        self.imageNameLst = images["fileLst"]

        # view와 model 연결
        self.allImageModel = AllImageModel()
        self.okImageModel = OkImageModel()
        self.defImageModel = DefImageModel()
        # self.imageViewMode = ImageViewModel(self.tableViewImageList, self.allImageModel)
        print(self.allImageModel)

        self.allList()
        # self.dataInit()

        # 리스트에서 이미지 선택할때..
        # imageDir = images["dir"] + "/"+ images["fileLst"][0]
        # self.showDetail(imageDir)

        # 테이블 클릭 이벤트
        self.tableWidgetAllFile.clicked.connect(self.clickTableAllImages)

    # def dataInit(self):
    #     self.tableViewImageList.setModel(self.allImageModel.model)

    # 초기 테이블 세팅
    def initTabel(self):
        self.tableWidgetAllFile.setColumnCount(2)
        self.tableWidgetAllFile.setHorizontalHeaderLabels(['FileName', 'CreatedTime'])

        pass

    # 모든 이미지 파일 리스트 클래스에 데이터 넣기
    def allList(self):
        imageList = self.allImageModel.data
        self.tableWidgetAllFile.setRowCount(len(imageList))
        for fileIdx in range(len(imageList)):
            self.tableWidgetAllFile.setItem(fileIdx, 0, QTableWidgetItem(imageList[fileIdx][0]))

        pass

    # 파일 리스트에 데이터 넣기
    def showList(self, images):
        
        print("images:::", images)
        self.tableWidgetAllFile.setColumnCount(2)
        self.tableWidgetAllFile.setRowCount(len(images["fileLst"]))
        print(len(images["fileLst"]))

        self.tableWidgetAllFile.setHorizontalHeaderLabels(['FileName', 'CreatedTime'])
        self.tableWidgetAllFile.horizontalHeaderItem(0).setToolTip("코드...")
        
        for fileIdx in range(len(images["fileLst"])):
            self.tableWidgetAllFile.setItem(fileIdx, 0, QTableWidgetItem(images["fileLst"][fileIdx]))

    # self.tableWidgetAllFile





    # 이미지, 내용 출력
    # def showDetail(self, imageIdx):
    #     global imageSourceDir
    #     global imageNameLst

    #     imageDir = imageSourceDir + "/"+ imageNameLst[imageIdx]
    #     print(imageDir)

    #     pixmap = QPixmap(imageDir)
    #     self.imageOriginal.setPixmap(pixmap)

    # 테이블 클릭 이벤트
    def clickTableAllImages(self):
        row = self.tableWidgetAllFile.currentIndex().row()
        print(row)
        self.showDetail(row)


class AllImageModel(list):
    # def __init__(self, )

    def __init__(self):
        self.data = [
            ['cast_def_0_3047.jpeg', 'def', {'ok':0.213, 'def':0.787}],
            ['cast_def_0_3046.jpeg', 'ok', {'ok':0.787, 'def':0.213}],
            ['cast_def_0_3046.jpeg', 'ok', {'ok':0.787, 'def':0.213}],
            ['cast_def_0_3046.jpeg', 'ok', {'ok':0.787, 'def':0.213}],
        ]
        self.model = QStandardItemModel()
        
class DefImageModel(list):
    def __init__(self, l=[]):
        self.data = [
            ['cast_def_0_3047.jpeg', 'def', {'ok':0.213, 'def':0.787}],
            ['cast_def_0_3046.jpeg', 'def', {'ok':0.213, 'def':0.787}],
        ]
        self.model = QStandardItemModel()

class OkImageModel(list):
    def __init__(self, l=[]):
        self.data = [
            ['cast_def_0_3047.jpeg', 'ok', {'ok':0.787, 'def':0.213}],
            ['cast_def_0_3046.jpeg', 'ok', {'ok':0.787, 'def':0.213}],
            ['cast_def_0_3046.jpeg', 'ok', {'ok':0.787, 'def':0.213}],
        ]
        self.model = QStandardItemModel()

# viewmodel에 view와 model 전달
# class ImageViewModel:
#     def __init__(self, view, model):
#         self.view = view
#         self.model = model
#         self.dataInit()

#     def dataInit(self):
#         self.view.setModel(self.model.model)


if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = AllImageWindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
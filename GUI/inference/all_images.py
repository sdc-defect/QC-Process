import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QBrush, QColor

import utils

# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form = utils.resource_path('ui/all_images.ui')
form_class = uic.loadUiType(form)[0]


# form_class = uic.loadUiType(r"C:\Users\multicampus\Desktop\guiFILE\6try1\inference\all_images.ui")[0]

# 화면을 띄우는데 사용되는 Class 선언
class AllImageWindowClass(QMainWindow, form_class):
    def __init__(self, allInferencedFile, allFileLst, okInferencedFile, okFileLst, defInferencedFile, defFileLst):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Inferenced Image List")
        self.allInferencedFile = allInferencedFile
        self.allFileLst = allFileLst
        self.okInferencedFile = okInferencedFile
        self.okFileLst = okFileLst
        self.defInferencedFile = defInferencedFile
        self.defFileLst = defFileLst

        self.initTabel()

        self.allList(self.allFileLst, self.allInferencedFile)

        # 테이블 클릭 이벤트
        self.tableWidgetAllFile.clicked.connect(self.clickTableAllImages)

        # 버튼 클릭 이벤트
        self.pushButtonAll.clicked.connect(self.clickPushButtonAll)
        self.pushButtonOk.clicked.connect(self.clickPushButtonOk)
        self.pushButtonDef.clicked.connect(self.clickPushButtonDef)

    def clickPushButtonAll(self):
        self.allList(self.allFileLst, self.allInferencedFile)

    def clickPushButtonOk(self):
        self.allList(self.okFileLst, self.okInferencedFile)

    def clickPushButtonDef(self):
        self.allList(self.defFileLst, self.defInferencedFile)

    # 초기 테이블 세팅
    def initTabel(self):
        self.tableWidgetAllFile.setColumnCount(3)
        self.tableWidgetAllFile.setHorizontalHeaderLabels(['File Name', 'Created Time', 'Result'])

    # 모든 이미지 파일 리스트 클래스에 데이터 넣기
    def allList(self, nameLst, fileDict):
        self.tableWidgetAllFile.setRowCount(len(nameLst))

        # 리스트에 값이 하나도 없으면
        cnt = 0
        if len(nameLst):
            for name in nameLst:
                # print(name, fileDict[name]["Timestamp"],fileDict[name]["Result"] )
                self.tableWidgetAllFile.setItem(cnt, 0, QTableWidgetItem(name))
                self.tableWidgetAllFile.setItem(cnt, 1, QTableWidgetItem(fileDict[name]["Timestamp"]))
                resultItem=QTableWidgetItem(fileDict[name]["Result"])
                if fileDict[name]["Result"]=='불량':
                    resultItem.setForeground(QBrush(QColor(255, 0,0)))
                self.tableWidgetAllFile.setItem(cnt, 2, resultItem)
                

                cnt = cnt + 1
        else:
            self.tableWidgetAllFile.clear()
        # pass

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

    # 이미지, 내용 출력
    def showDetail(self, filename):
        detail = self.allInferencedFile[filename]

        printContent = "File name: " + detail["File_name"] + "\nTime stamp: " + detail[
            "Timestamp"] + "\nProbability_ok: " + detail["Probability_ok"] + "\nProbability_def: " + detail[
                           "Probability_def"] + "\nResult: " + detail["Result"] + "\nImage_path: " + detail[
                           "Image_path"] + "\nCAM_path: " + detail["CAM_path"] + "\nMerged_path: " + detail[
                           "Merged_path"]

        self.textBrowserSelectedImage.clear()
        self.textBrowserSelectedImage.append(printContent)

        imageDir = detail["Image_path"]
        camDir = detail["CAM_path"]
        mergedDir = detail["Merged_path"]

        imageDirPixmap = QPixmap(imageDir)
        camDirPixmap = QPixmap(camDir)
        mergedDirPixmap = QPixmap(mergedDir)
        self.imageOriginal.setPixmap(imageDirPixmap)
        self.imageCAM.setPixmap(camDirPixmap)
        self.imageMerged.setPixmap(mergedDirPixmap)

    # 테이블 클릭 이벤트
    def clickTableAllImages(self):
        row = self.tableWidgetAllFile.currentIndex().row()
        self.tableWidgetAllFile.selectRow(row)
        filename = self.tableWidgetAllFile.item(row, 0).text()
        # 첫 열 값 넘김
        self.showDetail(filename)


if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    myWindow = AllImageWindowClass()

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()

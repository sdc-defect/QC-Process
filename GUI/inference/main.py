import sys
from typing import Optional
from PyQt5.QtCore import QTimerEvent
from PyQt5 import uic
import os
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtChart import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtCore import *
from PyQt5.QtCore import pyqtSlot

import matplotlib.animation as animation

import json
from PyQt5.QtWidgets import QApplication

import logging

import utils
from all_images import AllImageWindowClass
import utils.client as client
import utils.plot as plot
import utils.highlight as highlight
import datetime
import pyqtgraph as pg
import numpy as np
from PyQt5.QtWidgets import *

# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form = utils.resource_path('ui/inference.ui')
form_class = uic.loadUiType(form)[0]
ip = "k7b306.p.ssafy.io:8080"


# 화면을 띄우는데 사용되는 Class 선언
class InferenceWindowClass(QMainWindow, form_class):

    def __init__(self):
        super().__init__()
        self.websocket: Optional[client.Client] = None
        self.setupUi(self)

        self.inferenceDir = os.path.abspath(os.path.join('.', 'temp'))
        utils.create_folder(self.inferenceDir)
        self.modelName = ""
        self.singleInferenceDir = ""

        self.allFileLst = []
        self.okFileLst = []
        self.defFileLst = []

        self.allInferencedFile = {}
        self.okInferencedFile = {}
        self.defInferencedFile = {}


        self.ts=0

        self.initUI()
        self.setWindowTitle("Inference")
        self.setWindowIcon(QIcon('logo.png'))


        # chart object
        pg.setConfigOptions(background='w', foreground='black') 

        self.barX = list(range(60))
        self.barY = np.array([0]*60)
        self.lineX = list(range(60))
        self.lineY= np.array([0]*60)
        self.lineChart = pg.PlotWidget(title="불량률")
        self.lineChart.setLabel('left', '불량률 (%)')
        self.lineChart.setLabel('bottom', '시간 (분)')
        self.barChart = pg.PlotWidget(title="생산량")
        self.barChart.setLabel('left', '생산량 (개)')
        self.barChart.setLabel('bottom', '시간 (분)')
        self.lineChart.showGrid(x=False, y=True)
        self.barChart.showGrid(x=False, y=True)
        self.barChart.setXRange(0, 60, padding=0)   
        self.barChart.setYRange(0, 100, padding=0) 
        self.lineChart.setXRange(0, 60, padding=0)   
        self.lineChart.setYRange(0, 100, padding=0)
        self.lineChart.plot(self.barX, self.barY, pen='r')
        self.gridLayoutGraph.addWidget(self.lineChart)
        self.gridLayoutGraph.addWidget(self.barChart)
        
        #로그 하이라이트
        self.highlighter = highlight.Highlighter(self.textBrowserLogContent)

        
    
    
    # 웹소켓에서 데이터 받았을 때 실행
    def logSave(self, logContext):
        imgDescription = json.loads(logContext.replace("'", "\""))

        # 이미지 파일 저장 위치 정하기
        imagePath = self.inferenceDir + '/image/' + imgDescription["filename"] + '.jpg'
        camPath = self.inferenceDir + '/cam/' + imgDescription["filename"] + '_cam.jpg'
        mergedPath = self.inferenceDir + '/merged/' + imgDescription["filename"] + '_merged.jpg'

        # 로그 파일 저장용
        logMessage = {
            "Timestamp": imgDescription["timestamp"],
            "File_name": imgDescription["filename"],
            "Probability_ok": str(format(round(imgDescription["prob"][0], 6),'.6f')),
            "Probability_def": str(format(round(imgDescription["prob"][1], 6),'.6f')),
            "Result": "양품" if imgDescription["label"] == 0 else "불량",
            "Image_path": imagePath,
            "CAM_path": camPath,
            "Merged_path": mergedPath
        }

        tmpTimestamp=logMessage['Timestamp'].split('_')
        tmpTime=tmpTimestamp[1].split(':')
        self.textBrowserLogContent.append(
            tmpTimestamp[0] +' ' +tmpTime[0]+':'+tmpTime[1]+':'+ tmpTime[2] + ' -> '+ logMessage["Result"]+' [' + logMessage["Probability_ok"] + " , "+ logMessage["Probability_def"] + "]")
        self.get_result(logMessage)

        # 메인 화면 이미지 리스트에 계속 추가해주기
        row = self.tableWidgetLog.rowCount() - 1
        font = QFont()
        font.setBold(True)
        resultItem=QTableWidgetItem(logMessage["Result"])
        if logMessage["Result"]=='불량':
            resultItem.setForeground(QBrush(QColor(255, 0,0)))
        self.tableWidgetLog.setItem(row, 0, QTableWidgetItem(logMessage["File_name"]))
        self.tableWidgetLog.setItem(row, 1, QTableWidgetItem(logMessage["Timestamp"]))
        self.tableWidgetLog.setItem(row, 2, QTableWidgetItem(f'{(float(logMessage["Probability_ok"]))* 100:.2f}%'))
        self.tableWidgetLog.setItem(row, 3, QTableWidgetItem(f'{(float(logMessage["Probability_def"]))* 100:.2f}%'))
        self.tableWidgetLog.setItem(row, 4, resultItem)
        self.tableWidgetLog.insertRow(row + 1)
        if float(logMessage["Probability_ok"]) > float(logMessage["Probability_def"]):
            self.tableWidgetLog.item(row,2).setFont(font)
        else:
            self.tableWidgetLog.item(row,3).setFont(font)

        filename = logMessage["File_name"]

        self.allInferencedFile[filename] = logMessage
        self.allFileLst.append(filename)
        if imgDescription["label"] == 0:  # 양품
            self.okInferencedFile[filename] = logMessage
            self.okFileLst.append(filename)
        else:  # 불량
            self.defInferencedFile[filename] = logMessage
            self.defFileLst.append(filename)

        logger = self.initLogger("Inferenced")
        logger.info(logMessage)

        # 이미지 파일 jpg로 변환해서 저장
        utils.saveImageFile(imgDescription["img"], imagePath)
        utils.saveImageFile(imgDescription["cam"], camPath)
        utils.saveImageFile(imgDescription["merged"], mergedPath)

    # 초기화
    def initUI(self):
        self.textBrowserImageFile.setText(self.inferenceDir)
        self.logDirBtn.clicked.connect(self.editFileDir)
        self.modelDirBtn.clicked.connect(self.editModelDir)
        self.pushButtonLogClear.clicked.connect(lambda x: self.textBrowserLogContent.clear())
        self.modelListBtn.clicked.connect(self.getModelList)
        self.modelBox.activated[str].connect(self.modelSelect)

        response = utils.send_api(ip, '/model/list', 'GET')
        self.modelName = self.modelBox.currentText()
        if response.status_code == 200:
            models = json.loads(response.content.decode('utf-8'))['models']
            for model in models:
                self.modelBox.addItem(model)
            self.modelBox.setCurrentIndex(0)

        # log table setting
        
        self.tableWidgetLog.clicked.connect(self.clickTableImages)
    
        self.tableWidgetLog.setColumnCount(5)
        self.tableWidgetLog.setHorizontalHeaderLabels(
            ['File Name', 'Created Time', 'Probability_ok', 'Probability_def', 'Result'])
        self.tableWidgetLog.insertRow(0)
        self.tableWidgetLog.horizontalHeaderItem(0).setToolTip("코드...")

        self.tableWidgetLog.setColumnWidth(0, self.tableWidgetLog.width() * 1 / 5)
        self.tableWidgetLog.setColumnWidth(1, self.tableWidgetLog.width() * 1 / 5)
        self.tableWidgetLog.setColumnWidth(2, self.tableWidgetLog.width() * 1 / 5)
        self.tableWidgetLog.setColumnWidth(3, self.tableWidgetLog.width() * 1 / 5)
        self.tableWidgetLog.setColumnWidth(4, self.tableWidgetLog.width() * 1 / 6)

        # 이미지 미리보기
        self.pushButtonOpenSingleImageDir.clicked.connect(self.openSingleImage)

        # 추론 모든 이미지 보기
        self.pushButtonAllListShow.clicked.connect(self.allImagesWindowOpen)

        # 개별 이미지 추론 시작 버튼
        self.pushButtonSingleStartInference.clicked.connect(self.singleStartInference)

        # 전체 이미지 추론 시작 버튼
        self.pushButtonControlStart.clicked.connect(self.allStartInference)
        # 전체 이미지 추론 정지 버튼
        self.pushButtonControlStop.clicked.connect(self.allStopInference)
        # 전체 이미지 추론 일시 정지 버튼
        self.pushButtonControlPause.clicked.connect(self.pauseInference)
        # 전체 이미지 추론 다시 시작 버튼
        self.pushButtonControlRestart.clicked.connect(self.restartInference)

    # 로깅 초기화
    def initLogger(self, logger_name):
        self.logger = logging.getLogger(logger_name)
        if len(self.logger.handlers) > 0:
            return self.logger

        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(message)s")

        streamHandler = logging.StreamHandler()
        streamHandler.setLevel(logging.INFO)
        streamHandler.setFormatter(formatter)

        file_handler = logging.FileHandler(self.inferenceDir + '/log.log')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        self.logger.addHandler(streamHandler)
        return self.logger




    # 테이블 클릭시 이미지 띄우기
    def clickTableImages(self):
        row = self.tableWidgetLog.currentIndex().row()
        try:
            filename = self.tableWidgetLog.item(row, 0).text()
            detail = self.allInferencedFile[filename]
            self.tableWidgetLog.selectRow(row)

            imageDir = detail["Image_path"]
            self.singleInferenceDir = detail["Image_path"]
            self.labelSingleImageDir.setText(detail["Image_path"])
            mergedDir = detail["Merged_path"]

            imageDirPixmap = QPixmap(imageDir)
            merDirPixmap = QPixmap(mergedDir)
            self.labelSingleImageShow.setPixmap(imageDirPixmap)
            self.labelSingleCAMShow.setPixmap(merDirPixmap)

            if self.tableWidgetLog.item(row, 4).text() == '양품':
                self.textBrowserSingleResult.setText("양품")
            else:
                self.textBrowserSingleResult.setText("불량")
            self.textBrowserSingleResult_2.setText(self.tableWidgetLog.item(row, 2).text())
            self.textBrowserSingleResult_3.setText(self.tableWidgetLog.item(row, 3).text())

        except AttributeError:
            pass

    # 모달 창 - 모든 이미지 파일 리스트
    def allImagesWindowOpen(self):
        self.allImages = AllImageWindowClass(self.allInferencedFile, self.allFileLst, self.okInferencedFile,
                                             self.okFileLst, self.defInferencedFile, self.defFileLst)
        self.allImages.show()

    # 메뉴에 파일 다시 열기 누르면
    def editFileDir(self):
        fname = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if fname:
            self.inferenceDir = fname
            self.textBrowserImageFile.setText(fname)
            tmpSystemTime=str(datetime.datetime.now()).split('.')
            self.textBrowserLogContent.append(tmpSystemTime[0]+" -> Direcotry selected")

    # 메뉴에 모델 열기 누르면
    def editModelDir(self):
        fname = QFileDialog.getOpenFileName(self, '', 'Open file', 'ONNX(*.onnx)')  # 확장자 정해지면 설정하기
        if fname:
            self.modelDir = fname[0]
            QApplication.setOverrideCursor(Qt.WaitCursor)
            response = utils.send_file_put(ip, "/model/upload", fname[0])
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            if response.status_code == 200:
                QMessageBox.information(self, '모델 업로드', "업로드 성공")
                self.getModelList()
                tmpSystemTime=str(datetime.datetime.now()).split('.')
                self.textBrowserLogContent.append(tmpSystemTime[0]+" -> Model uploaded")
            else:
                QMessageBox.critical(self, '모델 업로드', "업로드 실패")

    def getModelList(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        response = utils.send_api(ip, '/model/list', 'GET')
        QApplication.setOverrideCursor(Qt.ArrowCursor)
        self.modelBox.clear()
        if response.status_code == 200:
            tmpSystemTime=str(datetime.datetime.now()).split('.')
            self.textBrowserLogContent.append(tmpSystemTime[0]+" -> Model refreshed")
            models = json.loads(response.content.decode('utf-8'))['models']
            for model in models:
                self.modelBox.addItem(model)
        self.modelBox.setCurrentIndex(0)
        self.modelName = self.modelBox.currentText()

    def modelSelect(self, text):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        response = utils.send_api(ip, f'/model/update/{text}', 'PUT')
        QApplication.setOverrideCursor(Qt.ArrowCursor)
        if response.status_code == 200:
            QMessageBox.information(self, '모델 변경', "성공")
            tmpSystemTime=str(datetime.datetime.now()).split('.')
            self.textBrowserLogContent.append(tmpSystemTime[0]+" -> Model changed")
        else:
            QMessageBox.critical(self, '모델 변경', "실패")

    # 개별 이미지 추론 열기
    def openSingleImage(self):
        fname = QFileDialog.getOpenFileName(self, '', 'Open file')
        if fname:
            self.labelSingleImageDir.clear()
            self.labelSingleImageDir.setText('원본 이미지')
            self.labelSingleImageShow.clear()
            self.labelSingleImageShow.setText('CAM 이미지')
            self.labelSingleCAMShow.clear()

            self.labelSingleImageDir.setText(fname[0])

            singleImageDir = fname[0]
            self.singleInferenceDir = singleImageDir
            pixmap = QPixmap(singleImageDir)
            self.labelSingleImageShow.setPixmap(pixmap)

            self.labelSingleCAMShow.clear()
            self.labelSingleCAMShow.setText(singleImageDir)

    # 개별 이미지 추론 시작
    def singleStartInference(self):
        if not self.singleInferenceDir:
            QMessageBox.critical(self, '개별 이미지 추론', "이미지 입력이 필요합니다.")
            return
        QApplication.setOverrideCursor(Qt.WaitCursor)
        response = utils.send_file_post(ip, '/single', self.singleInferenceDir)
        QApplication.setOverrideCursor(Qt.ArrowCursor)
        content = response.content.decode('utf-8')
        result: dict = json.loads(content[1:-1].replace("\\", ""))

        save = self.inferenceDir + '/single/' + result['filename']
        utils.saveImageFile(result['img'], f'{save}.jpg')
        utils.saveImageFile(result['cam'], f'{save}_cam.jpg')
        utils.saveImageFile(result['merged'], f'{save}_merged.jpg')
        self.labelSingleCAMShow.setPixmap(QPixmap(f'{save}_merged.jpg'))

        tmpResult="양품"
        if result['label'] == 1:
            tmpResult="불량"
        self.textBrowserSingleResult.setText(tmpResult)
        self.textBrowserSingleResult_2.setText(f'{(result["prob"][0] * 100):.2f}%')
        self.textBrowserSingleResult_3.setText(f'{(result["prob"][1] * 100):.2f}%')

        tmpTimestamp=result['timestamp'].split('_')
        tmpTime=tmpTimestamp[1].split(':')
        self.textBrowserLogContent.append(
            tmpTimestamp[0] +' ' +tmpTime[0]+':'+tmpTime[1]+':'+ tmpTime[2] + ' -> '+ tmpResult+' [' + str(format(round(result["prob"][0], 6),'.6f'))+ " , "+ str(format(round(result["prob"][1], 6),'.6f')) + "]")

        tmpSystemTime=str(datetime.datetime.now()).split('.')
        self.textBrowserLogContent.append(tmpSystemTime[0]+" -> Inference stopped")

    # 모든 이미지 추론 시작
    @pyqtSlot()
    def allStartInference(self):
        if not self.inferenceDir:
            QtWidgets.QMessageBox.critical(self, "저장 경로 미설정", "파일 저장 경로를 설정해주세요.")
        else:
            # 사용자 지정 dir에 image, cam, merged 파일 없으면 만듦
            if "image" not in os.listdir(self.inferenceDir):
                os.mkdir(self.inferenceDir + "/image")
            if "cam" not in os.listdir(self.inferenceDir):
                os.mkdir(self.inferenceDir + "/cam")
            if "merged" not in os.listdir(self.inferenceDir):
                os.mkdir(self.inferenceDir + "/merged")

            if self.websocket is not None:
                self.websocket.close()

            self.websocket = client.Client(f"ws://{ip}/ws")
            self.websocket.signal.connect(self.logSave)
            tmpSystemTime=str(datetime.datetime.now()).split('.')
            self.textBrowserLogContent.append(tmpSystemTime[0]+" -> Inference started")

            # 정지, 일시정지 버튼 활성화
            self.pushButtonControlStart.setEnabled(False)
            self.pushButtonControlRestart.setEnabled(False)
            self.pushButtonControlPause.setEnabled(True)
            self.pushButtonControlStop.setEnabled(True)
            # 개별 추론 버튼 비활성화
            self.pushButtonSingleStartInference.setEnabled(False)

    # 모든 이미지 추론 정지
    def allStopInference(self):
        tmpSystemTime=str(datetime.datetime.now()).split('.')
        self.textBrowserLogContent.append(tmpSystemTime[0]+" -> Inference stopped")
        self.websocket.close()

        # 시작 버튼 활성화, 나머지 비활성화
        self.pushButtonControlStart.setEnabled(True)
        self.pushButtonControlRestart.setEnabled(False)
        self.pushButtonControlPause.setEnabled(False)
        self.pushButtonControlStop.setEnabled(False)
        # 개별 추론 버튼 활성화
        self.pushButtonSingleStartInference.setEnabled(True)

    def pauseInference(self):
        tmpSystemTime=str(datetime.datetime.now()).split('.')
        self.textBrowserLogContent.append(tmpSystemTime[0]+" -> Inference paused")
        response = utils.send_api(ip, '/pause', 'POST')

        # 다시 시작, 정지 활성화
        if response.status_code == 200:
            self.pushButtonControlStart.setEnabled(False)
            self.pushButtonControlRestart.setEnabled(True)
            self.pushButtonControlPause.setEnabled(False)
            self.pushButtonControlStop.setEnabled(True)

    def restartInference(self):
        tmpSystemTime=str(datetime.datetime.now()).split('.')
        self.textBrowserLogContent.append(tmpSystemTime[0]+" -> Inference restarted")
        response = utils.send_api(ip, '/restart', 'POST')

        # 정지, 일시정지 버튼 활성화
        if response.status_code == 200:
            self.pushButtonControlStart.setEnabled(False)
            self.pushButtonControlRestart.setEnabled(False)
            self.pushButtonControlPause.setEnabled(True)
            self.pushButtonControlStop.setEnabled(True)


    def get_result(self, data):
        dt = QDateTime.currentDateTime()
        if int(self.ts)>int(dt.toString('mm')):
            self.barChart.clear()
            self.lineChart.clear()
            self.lineY=[0]*60
            self.barY=[0]*60
        self.ts = dt.toString('mm')
        self.barY[int(self.ts)]+=1
        if data["Result"]=='불량':
            self.lineY[int(self.ts)]+=1
        self.drawChart(self.barX, self.barY, self.lineY)
        
        
    def drawChart(self, x, y,Y):
        """ clear() 로 이전에 그린 차트 제거함. """
        
        dt = QDateTime.currentDateTime()
        self.lineChart.clear()
        self.barChart.clear() 
        self.barChart.setXRange(0, 60, padding=0)   
        self.barChart.setYRange(0, 100, padding=0) 
        self.lineChart.setXRange(0, 60, padding=0)   
        self.lineChart.setYRange(0, 100, padding=0)
        if int(dt.toString('mm'))>0:
            self.lineChart.plot(self.barX[0:int(dt.toString('mm'))], 100*np.array(Y[0:int(dt.toString('mm'))])/(np.array(y[0:int(dt.toString('mm'))])+0.000000001), pen='r', symbol='o',symbolSize=8 ,symbolBrush=('r'))
        bar_chart2 = pg.BarGraphItem(x=x, height=y, width=1, brush=QColor(52, 152, 219))
        self.barChart.addItem(bar_chart2)  

    def firstAction(self):
        self.layout().removeWidget(self.lblAreaLine)
        self.lblAreaLine.setParent(None)


    # 창 닫을 떄 발생하는 이벤트
    def closeEvent(self, event):
        try:
            self.websocket.close()
        except AttributeError:
            pass


def main():
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)
    # QTimer.singleShot(100000, quit_app)

    # WindowClass의 인스턴스 생성
    myWindow = InferenceWindowClass()

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    myWindow.firstAction()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()


if __name__ == "__main__":
    main()

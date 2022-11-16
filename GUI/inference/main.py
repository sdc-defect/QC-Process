import sys
from typing import Optional

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
from utils import saveImageFile

# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("ui/inference.ui")[0]
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

        self.yy = 0
        self.total = 0
        self.old_ts = 0
        self.a = 0
        self.cur_result = 0

        self.initUI()
        self.setWindowTitle("Inference")
        self.setWindowIcon(QIcon('logo.png'))

        # 그래프
        self.canvas = plot.PlotCanvasLine(self, width=10, height=8)
        self.gridLayoutGraph.addWidget(self.canvas)
        self.x = np.arange(60)
        self.y = np.ones(60, dtype=np.float64) * np.nan
        self.line, = self.canvas.axes.plot(self.x, self.y, animated=True, color='red', lw=2)
        self.ani = animation.FuncAnimation(self.canvas.figure, self.update_line, blit=True, interval=1000)
        self.pushButtonControlStart.clicked.connect(lambda x: self.ani.event_source.start())
        self.pushButtonControlStop.clicked.connect(lambda x: self.ani.event_source.stop())
        self.ani.event_source.stop()

        self.series = QBarSeries()

        # chart object
        chart = QChart()
        chart.addSeries(self.series)
        chart.layout().setContentsMargins(0, 0, 0, 0)

        chart.setTitle('수율')
        chart.setAnimationOptions(QChart.SeriesAnimations)

        dt = QDateTime.currentDateTime()
        self.ts = dt.toString('mm')

        axisX = QBarCategoryAxis()
        axisX.append('시간')

        axisY = QValueAxis()
        axisY.setRange(0, 500)

        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)
        self.series.attachAxis(axisX)
        self.series.attachAxis(axisY)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        self.chartView = QChartView(chart)

        self.gridLayoutGraph.addWidget(self.chartView)

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
            "Probability_ok": str(round(imgDescription["prob"][0], 6)),
            "Probability_def": str(round(imgDescription["prob"][1], 6)),
            "Result": "ok" if imgDescription["label"] == 0 else "def",
            "Image_path": imagePath,
            "CAM_path": camPath,
            "Merged_path": mergedPath
        }

        self.textBrowserLogContent.append(
            "Timestamp: " + logMessage["Timestamp"] + ", File_name: " + logMessage["File_name"] + ", Probability_ok: " +
            logMessage["Probability_ok"] + ", Probability_def: " + logMessage["Probability_def"] + ", Result: " +
            logMessage["Result"] + ", Image_path: " + logMessage["Image_path"] + ", CAM_path: " + logMessage[
                "CAM_path"] + ", Merged_path: " + logMessage["Merged_path"] + "\n")
        self.get_data(logMessage)
        self.get_result(logMessage)

        # 메인 화면 이미지 리스트에 계속 추가해주기
        row = self.tableWidgetLog.rowCount() - 1
        self.tableWidgetLog.setItem(row, 0, QTableWidgetItem(logMessage["File_name"]))
        self.tableWidgetLog.setItem(row, 1, QTableWidgetItem(logMessage["Timestamp"]))
        self.tableWidgetLog.setItem(row, 2, QTableWidgetItem(logMessage["Probability_ok"]))
        self.tableWidgetLog.setItem(row, 3, QTableWidgetItem(logMessage["Probability_def"]))
        self.tableWidgetLog.setItem(row, 4, QTableWidgetItem(logMessage["Result"]))
        self.tableWidgetLog.insertRow(row + 1)

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
        saveImageFile(imgDescription["img"], imagePath)
        saveImageFile(imgDescription["cam"], camPath)
        saveImageFile(imgDescription["merged"], mergedPath)

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

            imageDir = detail["Image_path"]
            camDir = detail["CAM_path"]
            self.singleInferenceDir = detail["Image_path"]
            self.labelSingleImageDir.setText(detail["Image_path"])
            # mergedDir = detail["Merged_path"]

            imageDirPixmap = QPixmap(imageDir)
            camDirPixmap = QPixmap(camDir)
            self.labelSingleImageShow.setPixmap(imageDirPixmap)
            self.labelSingleCAMShow.setPixmap(camDirPixmap)

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
            else:
                QMessageBox.critical(self, '모델 업로드', "업로드 실패")

    def getModelList(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        response = utils.send_api(ip, '/model/list', 'GET')
        QApplication.setOverrideCursor(Qt.ArrowCursor)
        self.modelBox.clear()
        self.modelBox.addItem('default')
        self.modelBox.setCurrentIndex(0)
        self.modelName = self.modelBox.currentText()
        if response.status_code == 200:
            models = json.loads(response.content.decode('utf-8'))['models']
            for model in models:
                self.modelBox.addItem(model)

    def modelSelect(self, text):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        response = utils.send_api(ip, f'/model/update/{text}', 'PUT')
        QApplication.setOverrideCursor(Qt.ArrowCursor)
        if response.status_code == 200:
            QMessageBox.information(self, '모델 변경', "성공")
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
        saveImageFile(result['img'], f'{save}.jpg')
        saveImageFile(result['cam'], f'{save}_cam.jpg')
        saveImageFile(result['merged'], f'{save}_merged.jpg')
        self.labelSingleCAMShow.setPixmap(QPixmap(f'{save}_merged.jpg'))

        if result['label'] == 0:
            self.textBrowserSingleResult.setText("양품")
        else:
            self.textBrowserSingleResult.setText("불량품")
        self.textBrowserSingleResult_2.setText(f'{(result["prob"][0] * 100):.2f}%')
        self.textBrowserSingleResult_3.setText(f'{(result["prob"][1] * 100):.2f}%')

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
                print("websocket already exist")
                self.websocket.close()

            self.websocket = client.Client(f"ws://{ip}/ws")
            self.websocket.signal.connect(self.logSave)
            self.textBrowserLogContent.append("Inference started\n")

            # 정지, 일시정지 버튼 활성화
            self.pushButtonControlStart.setEnabled(False)
            self.pushButtonControlRestart.setEnabled(False)
            self.pushButtonControlPause.setEnabled(True)
            self.pushButtonControlStop.setEnabled(True)
            # 개별 추론 버튼 비활성화
            self.pushButtonSingleStartInference.setEnabled(False)

    # 모든 이미지 추론 정지
    def allStopInference(self):
        self.textBrowserLogContent.append("Inference stoped\n")
        self.websocket.close()

        # 시작 버튼 활성화, 나머지 비활성화
        self.pushButtonControlStart.setEnabled(True)
        self.pushButtonControlRestart.setEnabled(False)
        self.pushButtonControlPause.setEnabled(False)
        self.pushButtonControlStop.setEnabled(False)
        # 개별 추론 버튼 활성화
        self.pushButtonSingleStartInference.setEnabled(True)

    def pauseInference(self):
        self.textBrowserLogContent.append("Inference paused\n")
        response = utils.send_api(ip, '/pause', 'POST')

        # 다시 시작, 정지 활성화
        if response.status_code == 200:
            self.pushButtonControlStart.setEnabled(False)
            self.pushButtonControlRestart.setEnabled(True)
            self.pushButtonControlPause.setEnabled(False)
            self.pushButtonControlStop.setEnabled(True)

    def restartInference(self):
        self.textBrowserLogContent.append("Inference restarted\n")
        response = utils.send_api(ip, '/restart', 'POST')

        # 정지, 일시정지 버튼 활성화
        if response.status_code == 200:
            self.pushButtonControlStart.setEnabled(False)
            self.pushButtonControlRestart.setEnabled(False)
            self.pushButtonControlPause.setEnabled(True)
            self.pushButtonControlStop.setEnabled(True)

    def get_data(self, log):
        if type(log) == dict:
            if log['Result'] == 'def':
                self.yy += 1
            self.total += 1
            dt = QDateTime.currentDateTime()
            ts = dt.toString('mm')
            if ts != self.old_ts:
                self.old_ts = ts

    def update_line(self, i):
        y = self.yy / self.total if self.yy != 0 else 0
        old_y = self.line.get_ydata()
        new_y = np.r_[old_y[1:], y]
        self.line.set_ydata(new_y)

        return [self.line]

    def get_result(self, data):
        if type(data) == dict:
            self.cur_result += 1
        dt = QDateTime.currentDateTime()

        ts = dt.toString('mm')

        if len(self.series.barSets()) > 0:
            self.a = self.series.barSets()[-1]
            self.series.take(self.a)
        new_set = QBarSet(f'{ts}')
        if self.a != 0 and new_set.label() != self.a.label():
            self.series.append(self.a)
            self.cur_result = 0
        new_set << self.cur_result
        self.series.append(new_set)
        self.chartView.update()

    def firstAction(self):
        self.layout().removeWidget(self.lblAreaLine)
        self.lblAreaLine.setParent(None)

        self.gridLayoutGraph.addWidget(plot.WidgetPlotLine(self.centralwidget))

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

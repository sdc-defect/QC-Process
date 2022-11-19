import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtWidgets
import os

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QProcess

import utils
from training_init import TrainingInitWindowClass
from utils.dto import TrainConfig

import json

import pyqtgraph as pg

# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("training.ui")[0]

# 그래프 띄워줄 데이터 import
log_data1 = []
log_data2 = []
log_data3 = []
log_data5 = []
log_data6 = []
log_data7 = []


# 화면을 띄우는데 사용되는 Class 선언
class trainingWindowClass(QMainWindow, form_class):
    # set config data
    isSetFile = False
    config = TrainConfig(save_path=None, train_path=None, test_path=None, test_per=None, val_path=None, val_per=None)

    setAugmentation = True
    setFlip = True
    setSpin = True
    setSwift = True
    setMixup = True

    setEpoch = 50
    setBatchSize = 16
    setLearningRate = 0.0001
    setDecayStep = 1000

    trainSetDir = ""
    testSetDir = ""
    validationSetDir = ""
    modelSaveDir = ""

    trainFileCount = 0
    testFileCount = 0
    validationFileCount = 0

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Training")
        self.initUI()

        self.text = QPlainTextEdit()

        # 하이퍼파라미터 - 초기값 설정
        self.initHyperParameter()

        # log clear
        self.pushClearButton.clicked.connect(self.clickClearButton)

        # 학습 종료
        self.pushButtonControlStop.clicked.connect(self.trainingStop)

        #
        self.graphLoss = Graph_Widget(Xaxis='epoch', Yaxis='Loss', trainName='Train Loss', valName='Validation Loss',
                                      title='Loss')
        self.graphAcc = Graph_Widget(Xaxis='epoch', Yaxis='Acc', trainName='Train Accuracy',
                                     valName='Validation Accuracy', title='Accuracy')
        self.graphRecall = Graph_Widget(Xaxis='epoch', Yaxis='Recall', trainName='Train Recall',
                                        valName='Validation Recall', title='Recall')
        self.graphLayout.addWidget(self.graphLoss.graph, 0, 0)
        self.graphLayout.addWidget(self.graphAcc.graph, 0, 1)
        self.graphLayout.addWidget(self.graphRecall.graph, 0, 2)

    def clickClearButton(self):
        self.textBrowser.clear()

    # 초기화
    def initUI(self):
        _openFile = QtWidgets.QAction("다른 파일 열기", self)

        # Menu Bar Settings
        menu = self.menuBar()
        _file = menu.addMenu("파일")
        _file.addAction(_openFile)

        # Connect Actions
        _openFile.triggered.connect(self.editFileDir)

        self.initData()

    # 파일 열기 모달 띄우기
    def editFileDir(self):
        initFirstModal = TrainingInitWindowClass()
        initFirstModal.exec_()

        if initFirstModal.fileSetdata != {}:
            self.labelFileDir.setText('파일 위치')
            self.config.save_path = initFirstModal.fileSetdata['save_path']
            self.config.train_path = initFirstModal.fileSetdata['train_path']
            self.config.test_path = initFirstModal.fileSetdata['test_path']
            self.config.test_per = initFirstModal.fileSetdata['test_per']
            self.config.val_path = initFirstModal.fileSetdata['val_path']
            self.config.val_per = initFirstModal.fileSetdata['val_per']
            self.isSetFile = True

            # main.ui에 플롯되는 내용
            # Train
            self.labelTrainOkDir.setText(initFirstModal.fileSetdata['train_path'][0])
            self.labelTrainDefDir.setText(initFirstModal.fileSetdata['train_path'][1])
            self.labelTrainOkCount.setText(initFirstModal.fileSetdata['trainOkCount'])
            self.labelTrainDefCount.setText(initFirstModal.fileSetdata['trainDefCount'])

            # Test
            if self.config.test_path == None:
                self.labelTestOkCount.setStyleSheet("Color : gray")
                self.labelTestOkDir.setStyleSheet("Color : gray")
                self.labelTestOkTitle.setStyleSheet("Color : gray")
                self.labelTestDefCount.setStyleSheet("Color : gray")
                self.labelTestDefDir.setStyleSheet("Color : gray")
                self.labelTestDefTitle.setStyleSheet("Color : gray")

                self.labelTestRatioCount.setStyleSheet("Color : black")
                self.labelTestRatioDir.setStyleSheet("Color : black")
                self.labelTestRatioTitle.setStyleSheet("Color : black")

                self.labelTestRatioDir.setText(str(int(initFirstModal.fileSetdata['test_per'] * 100)) + '%')
                self.labelTestRatioCount.setText(initFirstModal.fileSetdata['testTotalCount'])
            else:
                self.labelTestOkCount.setStyleSheet("Color : black")
                self.labelTestOkDir.setStyleSheet("Color : black")
                self.labelTestOkTitle.setStyleSheet("Color : black")
                self.labelTestDefCount.setStyleSheet("Color : black")
                self.labelTestDefDir.setStyleSheet("Color : black")
                self.labelTestDefTitle.setStyleSheet("Color : black")

                self.labelTestRatioCount.setStyleSheet("Color : gray")
                self.labelTestRatioDir.setStyleSheet("Color : gray")
                self.labelTestRatioTitle.setStyleSheet("Color : gray")

                self.labelTestOkDir.setText(initFirstModal.fileSetdata['test_path'][0])
                self.labelTestDefDir.setText(initFirstModal.fileSetdata['test_path'][1])
                self.labelTestOkCount.setText(initFirstModal.fileSetdata['testOkCount'])
                self.labelTestDefCount.setText(initFirstModal.fileSetdata['testDefCount'])

            # Validation
            if self.config.val_path == None:
                self.labelValidationOkCount.setStyleSheet("Color : gray")
                self.labelValidationOkDir.setStyleSheet("Color : gray")
                self.labelValidationOkTitle.setStyleSheet("Color : gray")
                self.labelValidationDefCount.setStyleSheet("Color : gray")
                self.labelValidationDefDir.setStyleSheet("Color : gray")
                self.labelValidationDefTitle.setStyleSheet("Color : gray")

                self.labelValidationRatioCount.setStyleSheet("Color : black")
                self.labelValidationRatioDir.setStyleSheet("Color : black")
                self.labelValidationRatioTitle.setStyleSheet("Color : black")

                self.labelValidationRatioDir.setText(str(int(initFirstModal.fileSetdata['val_per'] * 100)) + '%')
                self.labelValidationRatioCount.setText(initFirstModal.fileSetdata['validationTotalCount'])
            else:
                self.labelValidationOkCount.setStyleSheet("Color : black")
                self.labelValidationOkDir.setStyleSheet("Color : black")
                self.labelValidationOkTitle.setStyleSheet("Color : black")
                self.labelValidationDefCount.setStyleSheet("Color : black")
                self.labelValidationDefDir.setStyleSheet("Color : black")
                self.labelValidationDefTitle.setStyleSheet("Color : black")

                self.labelValidationRatioCount.setStyleSheet("Color : gray")
                self.labelValidationRatioDir.setStyleSheet("Color : gray")
                self.labelValidationRatioTitle.setStyleSheet("Color : gray")

                self.labelValidationOkDir.setText(initFirstModal.fileSetdata['val_path'][0])
                self.labelValidationDefDir.setText(initFirstModal.fileSetdata['val_path'][1])
                self.labelValidationOkCount.setText(initFirstModal.fileSetdata['validationOkCount'])
                self.labelValidationDefCount.setText(initFirstModal.fileSetdata['validationDefCount'])

            # Save Directiory   
            self.labelSaveDir.setText(initFirstModal.fileSetdata['save_path'])

    # 이벤트 연결
    def initData(self):
        # 어그멘테이션
        self.checkBoxAugmentation.stateChanged.connect(self.switchAugmentation)
        self.checkBoxFlip.stateChanged.connect(self.switchFlip)
        self.checkBoxSpin.stateChanged.connect(self.switchSpin)
        self.checkBoxSwift.stateChanged.connect(self.switchSwift)
        self.checkBoxMixup.stateChanged.connect(self.switchMixup)

        # 하이퍼파라미터
        self.spinBoxEpoch.valueChanged.connect(self.changeEpoch)
        self.comboBoxBatchSize.currentTextChanged.connect(self.changeBatchSize)
        self.horizontalSliderLearningRate.valueChanged.connect(self.changeLearningRate)
        self.comboBoxDecayStep.currentTextChanged.connect(self.changeDecayStep)

        self.lineEditBatchSize.textChanged.connect(self.customBatchSize)
        self.lineEditDecayStep.textChanged.connect(self.customDecayStep)

        self.comboBoxBatchSize.setCurrentText("16")
        self.comboBoxDecayStep.setCurrentText("1000")
        self.labelLearningRate.setText(str(self.setLearningRate))

        self.pushButtonControlStart.clicked.connect(self.trainingStart)
        self.pushButtonControlStop.clicked.connect(self.trainingStop)

        # 프로그래스바는 0부터 시작
        self.progressBar.setValue(0)

    # epoch
    def changeEpoch(self):

        epoch = self.spinBoxEpoch.value()
        if epoch % 5 != 0:  # 5의 배수 아니면 절삭
            epoch = epoch - epoch % 5
            self.spinBoxEpoch.setValue(epoch)
        self.setEpoch = epoch

    # batch size
    def changeBatchSize(self):
        if self.comboBoxBatchSize.currentText() == "사용자 지정":
            self.lineEditBatchSize.setEnabled(True)
            self.lineEditBatchSize.setText(str(self.setBatchSize))
            self.setBatchSize = self.lineEditBatchSize.text()
        else:
            self.lineEditBatchSize.setEnabled(False)
            self.lineEditBatchSize.setText("")
            self.setBatchSize = self.comboBoxBatchSize.currentText()

    def customBatchSize(self):
        self.setBatchSize = self.lineEditBatchSize.text()

    # learning rate
    def changeLearningRate(self):
        self.setLearningRate = self.horizontalSliderLearningRate.value() / 10000
        self.labelLearningRate.setText(str(self.setLearningRate))

    # decay step
    def changeDecayStep(self):
        if self.comboBoxDecayStep.currentText() == "사용자 지정":
            self.lineEditDecayStep.setEnabled(True)
            self.lineEditDecayStep.setText(str(self.setDecayStep))
            self.setDecayStep = self.lineEditDecayStep.text()
        else:
            self.lineEditDecayStep.setEnabled(False)
            self.lineEditDecayStep.setText("")
            self.setDecayStep = self.comboBoxDecayStep.currentText()

    def customDecayStep(self):
        self.setDecayStep = self.lineEditDecayStep.text()

    # 하이퍼파라미터 - 초기값 설정
    def initHyperParameter(self):
        # 어그멘테이션 초기 - 전부 선택
        self.checkBoxAugmentation.setCheckState(2)
        self.checkBoxFlip.setCheckState(2)
        self.checkBoxSpin.setCheckState(2)
        self.checkBoxSwift.setCheckState(2)
        self.checkBoxMixup.setCheckState(2)

        self.switchAugmentation()

    # 어그멘테이션 전체 on/off 활성화 비활성화
    def switchAugmentation(self):
        self.setAugmentation = self.checkBoxAugmentation.isChecked()
        isAugmentation = self.setAugmentation

        if isAugmentation:
            self.checkBoxFlip.setEnabled(True)
            self.checkBoxSpin.setEnabled(True)
            self.checkBoxSwift.setEnabled(True)
            self.checkBoxMixup.setEnabled(True)

            self.setAugmentation = True
            self.setFlip = self.checkBoxFlip.isChecked()
            self.setSpin = self.checkBoxSpin.isChecked()
            self.setSwift = self.checkBoxSwift.isChecked()
            self.setMixup = self.checkBoxMixup.isChecked()

        else:
            self.checkBoxFlip.setEnabled(False)
            self.checkBoxSpin.setEnabled(False)
            self.checkBoxSwift.setEnabled(False)
            self.checkBoxMixup.setEnabled(False)

            self.setAugmentation = False
            self.setFlip = False
            self.setSpin = False
            self.setSwift = False
            self.setMixup = False

    # 어그멘테이션 개별 on/off
    def switchFlip(self):
        self.setFlip = self.checkBoxFlip.isChecked()

    def switchSpin(self):
        self.setSpin = self.checkBoxSpin.isChecked()

    def switchSwift(self):
        self.setSwift = self.checkBoxSwift.isChecked()

    def switchMixup(self):
        self.setMixup = self.checkBoxMixup.isChecked()

    def changeProgressbar(self, progress):
        self.progressBar.setValue(progress)

    # 학습 시작
    @pyqtSlot()
    def trainingStart(self):
        # 어그멘테이션 설정
        if self.setAugmentation:
            self.config.flip = self.checkBoxFlip.isChecked()
            self.config.spin = self.checkBoxSpin.isChecked()
            self.config.shift = self.checkBoxSwift.isChecked()
            self.config.mixup = self.checkBoxMixup.isChecked()
        else:
            self.config.flip = False
            self.config.spin = False
            self.config.shift = False
            self.config.mixup = False

        # 하이퍼 파라미터 설정
        self.config.epoch = int(self.spinBoxEpoch.text())
        self.config.lr = float(self.labelLearningRate.text())

        if self.comboBoxBatchSize.currentText() == "사용자 지정":
            self.config.batch_size = int(self.lineEditBatchSize.text())
        else:
            self.config.batch_size = int(self.comboBoxBatchSize.currentText())

        if self.comboBoxDecayStep.currentText() == "사용자 지정":
            self.config.decay = int(self.lineEditDecayStep.text())
        else:
            self.config.decay = int(self.comboBoxDecayStep.currentText())
        
        self.graphLoss.setEpoch(self.config.epoch)
        self.graphAcc.setEpoch(self.config.epoch)
        self.graphRecall.setEpoch(self.config.epoch)
        
        if self.isSetFile:
            try:
                # Augmentation, hyper parameter unable
                # Augmentation
                self.checkBoxAugmentation.setEnabled(False)
                self.checkBoxFlip.setEnabled(False)
                self.checkBoxMixup.setEnabled(False)
                self.checkBoxSpin.setEnabled(False)
                self.checkBoxSwift.setEnabled(False)

                # hyper parameter
                self.spinBoxEpoch.setEnabled(False)
                self.horizontalSliderLearningRate.setEnabled(False)
                self.labelLearningRate.setEnabled(False)
                self.comboBoxBatchSize.setEnabled(False)
                self.lineEditBatchSize.setEnabled(False)
                self.comboBoxDecayStep.setEnabled(False)
                self.lineEditDecayStep.setEnabled(False)

                # start button
                self.pushButtonControlStart.setEnabled(False)

                # QProcess 시작
                save_path = self.config.process()
                utils.make_folder(save_path)

                # .json 파일 만들기
                json_file = os.path.join(save_path, 'config.json')
                with open(json_file, 'w') as f:
                    json.dump(self.config.__dict__, f)
                    print("dumped", json_file)

                # qProcess
                self.start_process(json_file)
            except Exception as e:
                # 오류 메시지 출력하기
                print(e)

    def message(self, s):
        self.textBrowser.append(s)
        s = s.rstrip()
        if s[-1] == '}':

            tmp = s.split('-')
            isTrain = tmp[3].rstrip().lstrip()
            result_dict = tmp[5].rstrip().lstrip()

            if isTrain == 'train':
                result_dict = eval(result_dict)
                log_data1.append(result_dict['loss'])
                log_data2.append(result_dict['accuracy'])
                log_data3.append(result_dict['recall'])

                self.graphLoss.update(epoch=int(result_dict['epoch'].split('/')[0]), data=float(result_dict['loss']),
                                      name=isTrain)
                self.graphAcc.update(epoch=int(result_dict['epoch'].split('/')[0]), data=float(result_dict['accuracy']),
                                     name=isTrain)
                self.graphRecall.update(epoch=int(result_dict['epoch'].split('/')[0]),
                                        data=float(result_dict['recall']), name=isTrain)
                self.updateGrpah()

            elif isTrain == 'val':
                result_dict = eval(result_dict)
                log_data5.append(result_dict['loss'])
                log_data6.append(result_dict['accuracy'])
                log_data7.append(result_dict['recall'])

                self.graphLoss.update(epoch=int(result_dict['epoch'].split('/')[0]), data=float(result_dict['loss']),
                                      name=isTrain)
                self.graphAcc.update(epoch=int(result_dict['epoch'].split('/')[0]), data=float(result_dict['accuracy']),
                                     name=isTrain)
                self.graphRecall.update(epoch=int(result_dict['epoch'].split('/')[0]),
                                        data=float(result_dict['recall']), name=isTrain)

                if result_dict['batch'].split('/')[0] == result_dict['batch'].split('/')[1]:
                    epoch = int(result_dict['epoch'].split('/')[0])
                    Mepoch = int(self.spinBoxEpoch.text())
                    cal = epoch * 100 // Mepoch
                    self.changeProgressbar(cal)
        return

    def start_process(self, json_file):
        self.message("Executing process")
        self.p = QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
        self.p.readyReadStandardOutput.connect(self.handle_stdout)
        self.p.readyReadStandardError.connect(self.handle_stderr)
        self.p.stateChanged.connect(self.handle_state)
        self.p.finished.connect(self.process_finished)  # Clean up once complete.
        self.message(self.p.start("python", ['train.py', '--json', json_file]))

    def handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        # Extract progress if it is in the data.
        self.message(stderr)

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        print(data)
        stdout = bytes(data).decode("utf8")
        print(type(stdout), len(stdout), str(stdout))
        if stdout[0] == '{' and stdout[-1] == '}':
            print(TrainConfig)
            data = json.loads(stdout)
            print('=============== data:')
            print(data)
        self.message(stdout)

    def handle_state(self, state):
        states = {
            QProcess.NotRunning: 'Not running',
            QProcess.Starting: 'Starting',
            QProcess.Running: 'Running',
        }
        state_name = states[state]
        self.message(f"State changed: {state_name}")

    def process_finished(self):
        self.message("Process finished.")
        self.p = None

    # 학습 정지
    def trainingStop(self):
        if self.p != None:
            self.p.kill()
            self.p = None

            # Augmentation
            self.checkBoxAugmentation.setEnabled(True)
            self.checkBoxFlip.setEnabled(True)
            self.checkBoxMixup.setEnabled(True)
            self.checkBoxSpin.setEnabled(True)
            self.checkBoxSwift.setEnabled(True)

            # hyper parameter
            self.spinBoxEpoch.setEnabled(True)
            self.horizontalSliderLearningRate.setEnabled(True)
            self.labelLearningRate.setEnabled(True)
            self.comboBoxBatchSize.setEnabled(True)
            self.comboBoxDecayStep.setEnabled(True)
            if self.comboBoxBatchSize.currentText() == '사용자 지정':
                self.lineEditBatchSize.setEnabled(True)
            if self.comboBoxDecayStep.currentText() == '사용자 지정':
                self.lineEditDecayStep.setEnabled(True)

            # start button
            self.pushButtonControlStart.setEnabled(True)

    # 그래프 플로팅
    def updateGrpah(self):
        return


# 그래프용 Class 선언
class Graph_Widget:
    def __init__(self, Xaxis, Yaxis, trainName, valName, title):

        self.graph = pg.PlotWidget(background='w')
        self.x1 = []
        self.y1 = []
        self.trainName = trainName
        self.startEpoch = 1

        self.x2 = []
        self.y2 = []
        self.valName = valName
        self.valStartEpoch = 1
        # style
        self.graph.setBackground('w')
        # self.graph.setTitle("Title")
        self.graph.setLabel("left", Yaxis)
        self.graph.setLabel("bottom", Xaxis)
        self.graph.setTitle(title)
        self.graph.addLegend(size=(80, 10), offset=(355, 1))
        self.graph.showGrid(x=True, y=True)
        self.graph.setGeometry(300, 100, 550, 650)
        self.graph.setXRange(0, 50)
        self.graph.setYRange(0, 1)
        # plot 
        self.graph.plot(x=self.x1, y=self.y1, pen=pg.mkPen(width=2, color='r'), name=trainName, symbol='o',
                        symbolSize=8, symbolBrush=('r'))
        self.graph.plot(x=self.x2, y=self.y2, pen=pg.mkPen(width=2, color='b'), name=valName, symbol='o', symbolSize=8,
                        symbolBrush=('b'))

    def setEpoch(self, epoch):
        self.graph.setXRange(0, epoch)
        return

    def update(self, epoch, data, name):
        if name == 'train':
            if epoch == self.startEpoch:
                self.x1.append(epoch)
                self.y1.append(data)
                self.startEpoch += 1
            else:
                self.y1[epoch - 1] = data
            self.graph.clear()
            self.graph.plot(x=self.x1, y=self.y1, pen=pg.mkPen(width=2, color='r'), name=self.trainName, symbol='o',
                            symbolSize=8, symbolBrush=('r'))
            self.graph.plot(x=self.x2, y=self.y2, pen=pg.mkPen(width=2, color='b'), name=self.valName, symbol='o',
                            symbolSize=8, symbolBrush=('b'))
        else:
            if epoch == self.valStartEpoch:
                self.x2.append(epoch)
                self.y2.append(data)
                self.valStartEpoch += 1
            else:
                self.y2[epoch - 1] = data
            self.graph.clear()
            self.graph.plot(x=self.x1, y=self.y1, pen=pg.mkPen(width=2, color='r'), name=self.trainName, symbol='o',
                            symbolSize=8, symbolBrush=('r'))
            self.graph.plot(x=self.x2, y=self.y2, pen=pg.mkPen(width=2, color='b'), name=self.valName, symbol='o',
                            symbolSize=8, symbolBrush=('b'))

        return


# 그래프 끝

def main():
    app = QApplication(sys.argv)
    myWindow = trainingWindowClass()
    myWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

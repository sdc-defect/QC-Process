import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import os
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtChart import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtCore import *
from PyQt5.QtCore import pyqtSlot
import pandas as pd
import time
from pandas import Series
<<<<<<< HEAD
# import matplotlib.pyplot as plt
=======
import matplotlib.pyplot as plt
>>>>>>> 10538915bbd3926c4546b86fb8201fcfd27c4a93



class Worker(QThread):
    
    time = pyqtSignal(str)
    result = pyqtSignal(int)
<<<<<<< HEAD
    cur_result = 1
=======
    cur_result = 0
>>>>>>> 10538915bbd3926c4546b86fb8201fcfd27c4a93
    def __init__(self):
        super().__init__()

    def run(self):
        infResult = { "timestamp": "2022-11-07 10:57:36",
            "prob": [
                0.05927957221865654,
                0.9407203793525696
            ],
            "label" : 1
        }

        infResult2 = { "timestamp": "2022-11-07 11:57:36",
            "prob": [
                0.05927957221865654,
                0.9407203793525696
            ],
            "label" : 2
        }
        while True:
            self.cur_result += 1
            self.result.emit(self.cur_result)
<<<<<<< HEAD
            time.sleep(10)
=======
            time.sleep(1)
>>>>>>> 10538915bbd3926c4546b86fb8201fcfd27c4a93
            
        for i in range(1, 10):
            cur_result += 1
            self.result.emit(cur_result)
            time.sleep(1)
            

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
    # thread
        self.worker = Worker()
        self.worker.result.connect(self.get_result)
        self.worker.start()
        
        self.ticks = Series(dtype='int')
        
    # window size
        self.setMinimumSize(800, 400)
        self.series = QBarSeries()
        
<<<<<<< HEAD
        
=======
>>>>>>> 10538915bbd3926c4546b86fb8201fcfd27c4a93
    # chart object
        chart = QChart()
        # chart.legend().hide()
        chart.addSeries(self.series)

        self.resize(800, 600)

        chart.setTitle('수율')
<<<<<<< HEAD
        chart.setAnimationOptions(QChart.SeriesAnimations)

        dt = QDateTime.currentDateTime()
        self.statusBar().showMessage(dt.toString('mm'))
        self.ts = dt.toString('mm')
=======
        # chart.setAnimationOptions(QChart.SeriesAnimations)

        dt = QDateTime.currentDateTime()
        self.statusBar().showMessage(dt.toString('M'))
        self.ts = dt.toString('M')
>>>>>>> 10538915bbd3926c4546b86fb8201fcfd27c4a93

        months = (self.ts)

        axisX = QBarCategoryAxis()
        axisX.append(months)

        axisY = QValueAxis()
<<<<<<< HEAD
        axisY.setRange(0, 500)

        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)
        self.series.attachAxis(axisX)
        self.series.attachAxis(axisY)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        self.chartView = QChartView(chart)
        self.setCentralWidget(self.chartView)
=======
        # axisY.setRange(0, 15)

        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)

        chart.legend().setVisible(False)
        chart.legend().setAlignment(Qt.AlignBottom)

        chartView = QChartView(chart)
        self.setCentralWidget(chartView)
>>>>>>> 10538915bbd3926c4546b86fb8201fcfd27c4a93

        # 코드 복붙 끝

        # ts = dt.toString('M')
        # axisX = QBarCategoryAxis()
        # axisX.append(ts)
        
        # axisY = QValueAxis()
        # axisY.setRange(0, 15)
    
        # chart.addAxis(axisX, Qt.AlignBottom)
        # chart.addAxis(axisY, Qt.AlignLeft)
        
        # chart.legend().setVisible(True)
        # chart.legend().setAlignment(Qt.AlignBottom)
        # chartView = QChartView(chart)
        # self.setCentralWidget(chartView)
        
    
    @pyqtSlot(int)
    def get_result(self, cur_result):
        
        
        # append current result
        dt = QDateTime.currentDateTime()
<<<<<<< HEAD
        self.statusBar().showMessage(dt.toString('mm'))
=======
        self.statusBar().showMessage(dt.toString('M'))
>>>>>>> 10538915bbd3926c4546b86fb8201fcfd27c4a93
        self.ticks[dt] = cur_result

        # # check whether minute changed
        # #if dt.time().minute() != self.minute_cur.time().minute():


<<<<<<< HEAD
        ts = dt.toString('mm')
        print(ts, cur_result, type(cur_result))
        
        a=0
        if len(self.series.barSets())>0:
            a=self.series.barSets()[-1]
            print(self.series.take(a))
        if a!=0:
            cur_result=cur_result+int(a[0])
        new_set = QBarSet(f'{ts}')
        new_set << cur_result
        if a!=0 and new_set.label()!=a.label():
            self.series.append(a)
        self.series.append(new_set)
        self.chartView.update()
        print('sum=',new_set[0])
        print('count=',self.series.count())
=======
        ts = dt.toString('M')
        print(ts, cur_result, type(cur_result))
        
        new_set = QBarSet(f'{ts}')
        # new_set.append(cur_result)
        new_set << cur_result
        self.series.append(new_set)
        # print(new_set)
>>>>>>> 10538915bbd3926c4546b86fb8201fcfd27c4a93


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    app.exec_()
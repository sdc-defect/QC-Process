import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import os

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("training_ratio.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    train_cnt = 900
    test_cnt = 100
    val_cnt = 0
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Title")
        
        self.pushButtonCalculateImg:QPushButton
        self.pushButtonSetRatio:QPushButton
        self.spinBoxTest:QSpinBox
        self.spinBoxVal:QSpinBox
        self.lcdNumberTrain:QLCDNumber
        self.lcdNumberVal:QLCDNumber
        self.lcdNumberTest:QLCDNumber
        self.labelTrainCnt:QLabel
        self.labelValCnt:QLabel
        self.labelTestCnt:QLabel
        
        if self.test_cnt > 0:
            self.spinBoxTest.setValue(self.test_cnt/(self.train_cnt + self.test_cnt) * 100)
            self.spinBoxTest.valueChanged.connect(self.do)
            self.spinBoxTest.setReadOnly(True)
        self.pushButtonCalculateImg.clicked.connect(self.btn_cal)
        
        self.pushButtonSetRatio.clicked.connect(self.btn_done)
    
    # test 비율값 변경 함수
    # 비율값이랑 장수 print, 
    def sb_test(self):
        print("spin box test")
        
    # validation 비율값 변경 함수
    def sb_val(self):
        print("spin box val")
    
    def do(self):
    # setting text to the label
        self.spinBoxTest.setText("변경 불가")
    
    # 장수계산 버튼 함수
    def btn_cal(self):
        if not self.test_cnt:
            self.test_cnt = round(self.train_cnt/ 100 * int(self.spinBoxTest.text()))
        self.val_cnt = round((self.train_cnt + self.test_cnt)/ 100 * int(self.spinBoxVal.text()))
        train_cnt = self.train_cnt - self.val_cnt
        self.labelTrainCnt.setText(str(train_cnt)+"장")
        self.labelValCnt.setText(str(self.val_cnt)+"장")
        self.labelTestCnt.setText(str(self.test_cnt)+"장")
        
        # return self.train_cnt, self.test_cnt, self.val_cnt
    
    # 완료 버튼 함수
    def btn_done(self):
        print("bnt 클릭")


if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
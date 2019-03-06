from PyQt5.QtWidgets import QApplication,QLabel
from PyQt5.QtWidgets import QWidget,QFileDialog,QMainWindow
from PyQt5 import QtWidgets,QtCore
import os,time,cv2
import numpy as np
from PyQt5.QtGui import *

class Img2Bin(QtCore.QThread):
    def __init__(self,img=None):
        super().__init__()

    def run(self,path="/media/zhaomingxin/winF/PythonProject/VPGUI/projects/examples"):
        imgList = os.listdir(path)
        img = cv2.imread(os.path.join(path,imgList[0]),cv2.COLOR_BGR2RGB)
        img.tofile("/media/zhaomingxin/winE/Github/a.bin")
        print("Convert Completed")

    def __del__(self):
        print("Thread Destroyed.")

class Params2Bin(QtCore.QThread):
    def __init__(self):
        super().__init__()


class RefreshResult(QtCore.QThread):
    def __init__(self,ResultArea):
        super().__init__()
        self.Signal = QtCore.pyqtSignal()
        self.RA = ResultArea

    def run(self,TYPE="origin",GAP=0.2,path="/media/zhaomingxin/winF/PythonProject/VPGUI/projects/examples"):
        imgList = os.listdir(path)
        # img = cv2.imread(os.path.join(path,imgList[0]))
        # img = cv2.resize(img, (300, 200))
        # qImg = QImage(img.data, 300, 200, 3 * 300, QImage.Format_RGB888)
        # self.RA.Tested.setPixmap(QPixmap(qImg))
        # self.sleep(GAP*50)
        for item in imgList:
            img = cv2.imread(os.path.join(path,item))
            img = cv2.resize(img, (300, 200))
            qImg = QImage(img.data, 300, 200, 3 * 300, QImage.Format_RGB888)
            self.RA.Tested.setPixmap(QPixmap(qImg))
            print(item)
            self.sleep(GAP*10)

            print("Setted")

    def __del__(self):
        print("Thread Destroyed")

class LogWriter(QtCore.QRunnable):
    def __init__(self):
        super().__init__()
        self.index = 0
        print(self.index)
    def run(self):
        while True:
            time.sleep(1)
            self.index+=1
            print(self.index)

    def __del__(self):
        print("Deleted")

class BackendThread(QtCore.QThread):
    def __int__(self):
        super().__init__()

    def run(self,window):
        a = SignalMonitor(window)
        # b = LogWriter()
        DeamonThread = QtCore.QThreadPool()
        DeamonThread.setMaxThreadCount(3)
        DeamonThread.start(a)
        # DeamonThread.start(b)

        a.run()
        # b.run()


class SignalMonitor(QtCore.QRunnable):
    def __init__(self,sender):
        super().__init__()
        self.ConnectCriticalSignals(sender)

    def ConnectCriticalSignals(self,sender):
        sender.RunCtrl.StartTestButton.clicked.connect(lambda: sender.LogArea.LogTab.append("nihao"))

    def run(self):
        print("1")





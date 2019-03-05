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
    def __init__(self):
        super().__init__()
    def run(self,ResultArea,TYPE="origin",GAP=0.2,path="/media/zhaomingxin/winF/PythonProject/VPGUI/projects/examples"):
        imgList = os.listdir(path)
        for item in imgList:
            img = cv2.imread(os.path.join(path,item))
            img = cv2.resize(img, (300, 200))
            qImg = QImage(img.data, 300, 200, 3 * 300, QImage.Format_RGB888)
            print(item)
            self.sleep(GAP*10)
            ResultArea.Tested.setPixmap(QPixmap(qImg))
            print("Setted")

    def __del__(self):
        print("Thread Destroyed")



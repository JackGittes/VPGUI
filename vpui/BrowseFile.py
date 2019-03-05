from PyQt5.QtWidgets import QApplication,QLabel
from PyQt5.QtWidgets import QWidget,QFileDialog,QMainWindow
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtGui import *
import os

class FileDialog(QtWidgets.QFileDialog):
    def __init__(self,path=None):
        super().__init__()
        if path is None:
            path = os.getcwd()
        self.setFixedSize(400,300)
        filename = self.getOpenFileName(QtWidgets.QMainWindow(),"选择文件", path)
        print(filename[0])

    def __del__(self):
        print("FileDialog Destroyed")
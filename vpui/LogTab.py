from PyQt5.QtWidgets import QApplication,QLabel
from PyQt5.QtWidgets import QWidget,QFileDialog,QMainWindow
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtGui import *

class LogTab(QWidget):
    def __init__(self):
        super().__init__()
        hLayout = QtWidgets.QHBoxLayout()

        self.Log = QtWidgets.QTabWidget()
        self.RealTimeLog = QtWidgets.QTextBrowser()
        self.Log.addTab(self.RealTimeLog,"实时日志")
        self.Log.addTab(QtWidgets.QTextBrowser(),"错误信息")
        self.Log.addTab(QtWidgets.QTextBrowser(),"状态")
        hLayout.addWidget(self.Log)

        self.setLayout(hLayout)
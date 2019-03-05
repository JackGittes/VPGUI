from PyQt5.QtWidgets import QWidget
from PyQt5 import QtWidgets
from PyQt5.QtGui import *

class RunButton(QWidget):
    def __init__(self):
        super().__init__()
        self.SetupButton()

    def SetupButton(self):
        vLayout = QtWidgets.QVBoxLayout()
        self.ExitButton = QtWidgets.QPushButton("结束并关闭")
        self.ExitButton.setIcon(QIcon("./icons/png/close.png"))

        self.LoadFileButton = QtWidgets.QPushButton("加载数据")
        self.LoadFileButton.setIcon(QIcon("./icons/png/openfile.png"))

        self.DownloadParamsButton = QtWidgets.QPushButton("下载数据")
        self.DownloadParamsButton.setIcon(QIcon("./icons/png/down.png"))

        self.StartTestButton = QtWidgets.QPushButton("开始测试")
        self.StartTestButton.setIcon(QIcon("./icons/png/start.png"))

        vLayout.addWidget(self.LoadFileButton)
        vLayout.addWidget(self.DownloadParamsButton)
        vLayout.addWidget(self.StartTestButton)
        vLayout.addWidget(self.ExitButton)
        self.setLayout(vLayout)

    def __del__(self):
        print("Run Button Destroyed.")
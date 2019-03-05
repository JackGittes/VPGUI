from PyQt5.QtWidgets import QApplication,QLabel
from PyQt5.QtWidgets import QWidget,QFileDialog,QMainWindow
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtGui import *

class DownloadWindow(QtWidgets.QMessageBox):
    def __init__(self,Window=None):
        super().__init__()
        initialGeometry = QtCore.QRect(500, 400, 200, 100)
        if Window is not None:
            initialGeometry.moveCenter(Window.geometry().center())

        self.setGeometry(initialGeometry)
        self.setWindowTitle("选择下载类型")
        self.setText("请选择参数下载类型：")
        imgButton =self.addButton("图像数据",QtWidgets.QMessageBox.YesRole)
        mpuButton =self.addButton("MPU指令", QtWidgets.QMessageBox.YesRole)
        vpButton =self.addButton("VP指令", QtWidgets.QMessageBox.YesRole)
        self.exec_()

    def __del__(self):
        print("Download Box Destroyed")
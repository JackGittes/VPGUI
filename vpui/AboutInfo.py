from PyQt5.QtWidgets import QApplication,QLabel
from PyQt5.QtWidgets import QWidget,QFileDialog,QMainWindow
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtGui import *

class AboutWindow(QtWidgets.QMessageBox):
    def __init__(self,Window=None):
        super().__init__()
        initialGeometry = QtCore.QRect(0, 0, 150, 60)
        if Window is not None:
            initialGeometry.moveCenter(Window.geometry().center())
        self.setGeometry(initialGeometry)

        IconMap = QPixmap("./icons/png/info.png").scaled(60,60,QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation)
        self.setIconPixmap(IconMap)

        self.setWindowTitle("关于")
        self.setText("视觉芯片测试软件平台")
        self.setInformativeText("作者：Vision Chip")

        yesButton = self.addButton("确定", QtWidgets.QMessageBox.YesRole)

        self.exec_()
        if self.clickedButton() == yesButton:
            self.close()
    def __del__(self):
        print("Exit Message Box Destroyed.")
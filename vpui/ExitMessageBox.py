from PyQt5.QtWidgets import QApplication,QLabel
from PyQt5.QtWidgets import QWidget,QFileDialog,QMainWindow
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtGui import *

class ExitMessage(QtWidgets.QMessageBox):
    def __init__(self,Window):
        super().__init__()
        initialGeometry = QtCore.QRect(0, 0, 100, 40)
        initialGeometry.moveCenter(Window.geometry().center())
        self.setGeometry(initialGeometry)
        IconMap = QPixmap("./icons/png/unlink.png").scaled(60,60,QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation)
        self.setIconPixmap(IconMap)
        self.setText("确认要退出？")
        self.setInformativeText("未保存的信息将丢失")
        self.setWindowTitle("提示")
        yesButton = self.addButton("确定", QtWidgets.QMessageBox.YesRole)
        self.addButton("取消", QtWidgets.QMessageBox.NoRole)
        self.exec_()
        if self.clickedButton() == yesButton:
            Window.close()
    def __del__(self):
        print("Exit Message Box Destroyed.")
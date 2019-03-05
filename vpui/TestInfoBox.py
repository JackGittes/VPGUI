from PyQt5.QtWidgets import QWidget
from PyQt5 import QtWidgets

class TestInfoBox(QWidget):
    def __init__(self):
        super().__init__()
        widget = QtWidgets.QWidget()

        self.TotalInfo = QtWidgets.QLabel(widget)
        self.TotalNumber = QtWidgets.QLCDNumber(widget)
        self.TestInfo = QtWidgets.QLabel(widget)
        self.FPS = QtWidgets.QLCDNumber(widget)

        self.TotalInfo.setText("总测试数量(张)")
        self.TestInfo.setText("当前帧率(FPS)")
        vLayout = QtWidgets.QVBoxLayout()
        vLayout.addWidget(self.TotalInfo)
        vLayout.addWidget(self.TotalNumber)
        vLayout.addWidget(self.TestInfo)
        vLayout.addWidget(self.FPS)
        self.setLayout(vLayout)
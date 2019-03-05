from PyQt5.QtWidgets import QApplication,QLabel
from PyQt5.QtWidgets import QWidget,QFileDialog,QMainWindow
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import QThread

class ResultArea(QWidget):
    def __init__(self):
        super().__init__()
        h1widget = QtWidgets.QWidget()
        h2widget = QtWidgets.QWidget()

        gLayout = QtWidgets.QVBoxLayout()
        h1Layout = QtWidgets.QHBoxLayout()
        h2Layout = QtWidgets.QHBoxLayout()

        """Two Images to Display"""
        self.Origin = QLabel(h1widget)
        self.Tested = QLabel(h1widget)

        self.WindowSize = [self.width(),self.height()]

        """A display tool used to control image display mode"""
        h1Layout.setStretch(0,1)
        h1Layout.setStretch(1,1)

        self.Origin.setPixmap(QPixmap("./imgs/gakki.png"))
        self.Tested.setPixmap(QPixmap("./imgs/tested.png"))

        h1Layout.addWidget(self.Origin)
        h1Layout.addWidget(self.Tested)

        self.PreviousButton = QtWidgets.QPushButton(h2widget)
        self.PlayPauseButton = QtWidgets.QPushButton(h2widget)
        self.NextButton = QtWidgets.QPushButton(h2widget)
        self.FileSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal,h2widget)

        self.Progress = QtWidgets.QProgressBar(h2widget)
        self.Progress.setMinimum(1)
        self.Progress.setMaximum(1000)

        self.SetButtonNames()

        h2Layout.addWidget(self.PreviousButton)
        h2Layout.addWidget(self.PlayPauseButton)
        h2Layout.addWidget(self.NextButton)
        h2Layout.addWidget(self.FileSlider)
        h2Layout.addWidget(self.Progress)

        h2Layout.setStretch(0, 1)
        h2Layout.setStretch(1, 1)
        h2Layout.setStretch(2, 1)
        h2Layout.setStretch(3, 6)
        h2Layout.setStretch(4, 10)

        h1widget.setLayout(h1Layout)
        h2widget.setLayout(h2Layout)

        gLayout.addWidget(h1widget)
        gLayout.addWidget(h2widget)

        self.setLayout(gLayout)
        self.adjustSize()

    def SetButtonNames(self):
        self.PreviousButton.setText("上一张")
        self.PlayPauseButton.setText("暂停/播放")
        self.NextButton.setText("下一张")

        self.PreviousButton.setIcon(QIcon("./icons/png/previous_one.png"))
        self.PlayPauseButton.setIcon(QIcon("./icons/png/play.png"))
        self.NextButton.setIcon(QIcon("./icons/png/next_one.png"))

    #TODO: use Qthread to update images to
    # avoid garbage-collection crash caused by image refreshing

    def UpdateImg(self,pic=None,type="Origin"):

        if pic is None:
            qImg = "./imgs/origin.png"
        else:
            qImg = QImage(pic.data, self.Origin.width(), self.Origin.height(), 3 * self.Origin.width(), QImage.Format_RGB888)
        if type=="Origin":
            self.Origin.setPixmap(QPixmap(qImg))
        elif type=="Tested":
            self.Tested.setPixmap(QPixmap(qImg))
        else:
            pass



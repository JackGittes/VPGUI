from PyQt5.QtWidgets import QApplication,QLabel
from PyQt5.QtWidgets import QWidget,QFileDialog,QMainWindow
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtGui import *

import cv2
import sys,os
import numpy as np

class VPGUI(QMainWindow):
    def __init__(self,parent=None):
        """Here we initialize VPGUI and set some default params"""
        super(VPGUI, self).__init__(parent)
        self.Name = "视觉芯片测试平台"
        self.Width = 1100
        self.Height = 800
        self.Version = "r1.0"
        self.StartTime = 0

        self.BWidth = 150
        self.BHeight = 40
        self.StandardGap = 40

        """A variable to record current test mode
            0: No test mode choose
            1~5: Self-defined test mode
        """
        self.Status = 0

    """Setup VPGUI and connect signals with slots"""
    def SetupUI(self):
        width = self.Width
        height = self.Height
        BW = self.BWidth
        BH = self.BHeight
        BGAP = self.StandardGap

        self.resize(width, height)
        self.setFixedSize(width, height)

        self.ExitButton = QtWidgets.QPushButton("结束并关闭",self)
        self.ExitButton.setGeometry(QtCore.QRect(width-BW-2*BGAP, height-BH-BGAP, BW, BH))
        self.ExitButton.clicked.connect(self.ExitMessageBox)

        self.LoadFileButton = QtWidgets.QPushButton("加载数据",self)
        self.LoadFileButton.setGeometry(QtCore.QRect(width-BW-2*BGAP, height-BH-5.5*BGAP, BW, BH))
        self.LoadFileButton.clicked.connect(self.BrowseFile)

        self.DownloadParamsButton = QtWidgets.QPushButton("下载数据",self)
        self.DownloadParamsButton.setGeometry(QtCore.QRect(width-BW-2*BGAP, height-BH-4*BGAP,  BW, BH))

        self.StartTestButton = QtWidgets.QPushButton("开始测试",self)
        self.StartTestButton.setGeometry(QtCore.QRect(width-BW-2*BGAP, height-BH-2.5*BGAP, BW, BH))

        # self.MessageOutput = QtWidgets.QTextBrowser(self)
        # self.MessageOutput.setGeometry(QtCore.QRect(width - BW - 2 * BGAP, height - BH - 2.5 * BGAP, BW, BH))

        self.CreateImgWindow()
        self.NameInitial()
        self.ExitTest()
        self.ToolBarTop()
        self.ShowTestResult()
        self.TopMenuBar()

    def NameInitial(self):
        self.setWindowTitle(self.Name+" "+self.Version)

    def ExitTest(self):
        self.ExitButton.clicked.connect(self.close)

    def CreateImgWindow(self, scale=0.55, margin=150, pos_y=50):
        window_w = int((self.Width - margin)/2)
        window_h = int(self.Height*scale)
        gap = int(margin/3)
        pos_x = gap

        self.DisplayOrigin = QLabel(self)
        self.DisplayOrigin.setGeometry(QtCore.QRect(pos_x,pos_y,window_w,window_h))

        self.DisplayTested = QLabel(self)
        self.DisplayTested.setGeometry(QtCore.QRect(pos_x+window_w+gap,pos_y,window_w,window_h))

        imgs1 = cv2.imread("./imgs/gakki.png")
        imgs2 = cv2.imread("./imgs/tested.png")
        imgs1 = cv2.cvtColor(imgs1,cv2.COLOR_BGR2RGB)
        imgs2 = cv2.cvtColor(imgs2, cv2.COLOR_BGR2RGB)

        imgs1 = cv2.resize(imgs1,(window_w,window_h))
        imgs2 = cv2.resize(imgs2, (window_w, window_h))
        h, w, ch = imgs1.shape
        qImg1 = QImage(imgs1.data, w, h, 3*w, QImage.Format_RGB888)
        qImg2 = QImage(imgs2.data, w, h, 3 * w, QImage.Format_RGB888)

        self.DisplayOrigin.setPixmap(QPixmap(qImg1))
        self.DisplayTested.setPixmap(QPixmap(qImg2))

    def BrowseFile(self):
        filename = QFileDialog.getOpenFileName(self, "选择文件", os.getcwd())
        print(filename[0])
        return filename

    def ToolBarTop(self):
        TestModeButton = QtWidgets.QPushButton("测试模式")
        SettingsButton = QtWidgets.QPushButton("设置")
        ExitTestButton = QtWidgets.QPushButton("退出测试")

        exitAct = QtWidgets.QAction('退出', self)

        toolbar = self.addToolBar("退出")

        toolbar.addWidget(TestModeButton)
        toolbar.addWidget(SettingsButton)
        toolbar.addWidget(ExitTestButton)
        toolbar.addAction(exitAct)

        TestMode = QtWidgets.QMenu()
        TestMode.addAction("舰船检测：分辨率32")
        TestMode.addAction("舰船检测：分辨率64")
        TestMode.addAction("舰船检测：分辨率128")
        TestMode.addAction("MobileNet：1000类")
        TestMode.addAction("MobileNet：20类")
        TestModeButton.setMenu(TestMode)
        TestMode.triggered.connect(lambda action: print(action.text()))

        Settings = QtWidgets.QMenu()
        SettingsButton.setMenu(Settings)

        ExitTestButton.clicked.connect(self.ExitMessageBox)

    def ExitMessageBox(self):
        Msg = QtWidgets.QMessageBox()
        Msg.setGeometry(QtCore.QRect(0,0, 100, 40))
        Msg.setIcon(QtWidgets.QMessageBox.Information)
        Msg.setText("确认要退出？")
        Msg.setInformativeText("未保存的信息将丢失")
        Msg.setWindowTitle("提示")
        Msg.setDetailedText("详细信息:"+str(self.Status))

        OKButton = QtWidgets.QMessageBox.Ok
        CancelButton = QtWidgets.QMessageBox.Cancel
        Msg.setStandardButtons( OKButton | CancelButton )

        """Set Messsage Window to Desktop Center"""
        qtRectangle = Msg.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        Msg.move(qtRectangle.topLeft())

        return Msg.exec_()

    def TopMenuBar(self):
        FileMenu = self.menuBar().addMenu("文件")
        EditMenu = self.menuBar().addMenu("编辑")
        SettingMenu = self.menuBar().addMenu("设置")
        RunMenu = self.menuBar().addMenu("运行")
        HelpMenu = self.menuBar().addMenu("帮助")

        PathAct = FileMenu.addAction('工作路径')
        PreferenceAct = FileMenu.addAction("偏好")
        ExitAct = FileMenu.addAction("退出")

        HelpMenu.addAction("查看日志")
        HelpMenu.addAction("帮助")
        HelpMenu.addAction("关于")

        WriteLogAct = EditMenu.addAction("日志")

    """Here is vision chip test platform help document."""
    def HelpManual(self):
        return True

    """Here is About info in top toolbar."""
    def AboutInfo(self):
        return True

    def ShowTestResult(self):
        print("I'm Ready")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = VPGUI()
    form.SetupUI()
    form.show()
    sys.exit(app.exec_())
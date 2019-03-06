from PyQt5.QtWidgets import QApplication,QLabel
from PyQt5.QtWidgets import QWidget,QFileDialog,QMainWindow
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtGui import *

import sys,os

from vpui import *
import function
import cv2

""" VPGUI Mainwindow used for vision chip test platform"""

class VPGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMaximumSize(1920,1080)
        self.setMinimumSize(800,600)

        icon = QIcon(QPixmap("./icons/png/main.png").scaled(60,65,QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.setWindowIcon(icon)

        self.Version = 1.0
        self.Name = "视觉芯片软件测试平台"
        self.setWindowTitle(self.Name+str(self.Version))

        self.Index = 0

        self.SetupGUI()
        self.BuildConnect()

        self.thread = ThreadEngine.BackendThread()
        self.thread

    def BuildConnect(self):
        self.RunCtrl.ExitButton.clicked.connect(lambda: ExitMessageBox.ExitMessage(self))
        self.RunCtrl.LoadFileButton.clicked.connect(lambda: BrowseFile.FileDialog())
        self.RunCtrl.DownloadParamsButton.clicked.connect(lambda: DownloadParamsWindow.DownloadWindow(self))
        self.RunCtrl.StartTestButton.clicked.connect(lambda: self.LogArea.RealTimeLog.append("nihao"))

        self.ResultImg.PreviousButton.clicked.connect(lambda: self.LogArea.RealTimeLog.append("前一首"))
        self.ResultImg.PlayPauseButton.clicked.connect(lambda: self.LogArea.RealTimeLog.append("播放"))
        # self.RunCtrl.StartTestButton.clicked.connect()

        # self.ResultImg.PreviousButton.clicked.connect()
        # self.ResultImg.PlayPauseButton.clicked.connect()
        # self.ResultImg.NextButton.clicked.connect()

    def SetupGUI(self):
        self.SetupMenuBar()
        self.SetupToolBar()
        self.SetupStatusBar()
        self.SetupMainWidget()

    def SetupMainWidget(self):
        self.gwidget = QtWidgets.QWidget()

        self.ResultImg = ResultArea.ResultArea()
        self.LogArea = LogTab.LogTab()
        self.TestArea = TestInfoBox.TestInfoBox()
        self.RunCtrl = RunButton.RunButton()

        bottomWidget = QtWidgets.QWidget()

        hLayout = QtWidgets.QHBoxLayout()
        hLayout.addWidget(self.LogArea)
        hLayout.addWidget(self.TestArea)
        hLayout.addWidget(self.RunCtrl)
        bottomWidget.setLayout(hLayout)

        vLayout = QtWidgets.QVBoxLayout()
        vLayout.addWidget(self.ResultImg)
        vLayout.addWidget(bottomWidget)

        self.gwidget.setLayout(vLayout)
        self.setCentralWidget(self.gwidget)

    def SetupMenuBar(self):
        FileMenu = self.menuBar().addMenu("文件")
        EditMenu = self.menuBar().addMenu("编辑")
        SettingMenu = self.menuBar().addMenu("设置")
        HelpMenu = self.menuBar().addMenu("帮助")

        """File Menu Settings Begin"""

        OpenFileAction = QtWidgets.QAction("打开",self)
        OpenFileAction.setIcon(QIcon("./icons/png/openfile.png"))

        SetPathAction = QtWidgets.QAction("路径",self)
        SetPathAction.setIcon(QIcon("./icons/png/path.png"))

        PreferenceAction = QtWidgets.QAction("偏好",self)
        PreferenceAction.setIcon(QIcon("./icons/png/settings.png"))

        ExitAction = QtWidgets.QAction("退出",self)
        ExitAction.setIcon(QIcon("./icons/png/exit.png"))

        FileMenu.addAction(OpenFileAction)
        FileMenu.addAction(SetPathAction)
        FileMenu.addAction(PreferenceAction)
        FileMenu.addAction(ExitAction)

        ExitAction.triggered.connect(lambda: ExitMessageBox.ExitMessage(self))

        """Edit Menu Settings Begin"""
        ConfigAction = QtWidgets.QAction("测试配置",self)
        ConfigAction.setIcon(QIcon("./icons/png/logs.png"))

        OutlookAction = QtWidgets.QAction("外观",self)
        OutlookAction.setIcon(QIcon("./icons/png/outlook.png"))

        EditMenu.addAction(ConfigAction)
        EditMenu.addAction(OutlookAction)

        """ Settings Menu Begin"""

        """Help Menu Settings Begin"""
        LookLogAction = QtWidgets.QAction("查看日志",self)
        LookLogAction.setIcon(QIcon("./icons/png/docs.png"))

        AboutAction = QtWidgets.QAction("关于",self)
        AboutAction.setIcon(QIcon("./icons/png/logs.png"))

        HelpAction = QtWidgets.QAction("帮助",self)
        HelpAction.setIcon(QIcon("./icons/png/what.png"))
        HelpAction.triggered.connect(lambda: os.system("xdg-open "+"./doc/document.pdf"))

        HelpMenu.addAction(LookLogAction)
        HelpMenu.addAction(HelpAction)
        HelpMenu.addAction(AboutAction)

        AboutAction.triggered.connect(lambda: AboutInfo.AboutWindow(self))

    def SetupToolBar(self):
        TestModeButton = QtWidgets.QPushButton("测试模式")
        PrepareButton = QtWidgets.QPushButton("初始化")
        PreprocessButton = QtWidgets.QPushButton("预处理")
        UploadButton = QtWidgets.QPushButton("返回结果")
        ResetButton = QtWidgets.QPushButton("复位状态")
        ChangeIOModeButton = QtWidgets.QPushButton("IO模式")

        TestModeButton.setIcon(QIcon("./icons/png/settings.png"))
        PrepareButton.setIcon(QIcon("./icons/png/connect.png"))
        PreprocessButton.setIcon(QIcon("./icons/png/process.png"))
        ResetButton.setIcon(QIcon("./icons/png/reset_hint.png"))
        UploadButton.setIcon(QIcon("./icons/png/upload.png"))


        self.toolbar = self.addToolBar("快捷设置")

        self.toolbar.addWidget(TestModeButton)
        self.toolbar.addWidget(PrepareButton)
        self.toolbar.addWidget(PreprocessButton)
        self.toolbar.addWidget(UploadButton)
        self.toolbar.addWidget(ResetButton)
        self.toolbar.addWidget(ChangeIOModeButton)

        ChangeIOMode = QtWidgets.QMenu()
        ChangeIOMode.addAction("模式1")
        ChangeIOMode.addAction("模式2")
        ChangeIOMode.addAction("模式3")
        ChangeIOModeButton.setMenu(ChangeIOMode)
        #
        # ChangeIOModeButton
        ChangeIOMode.triggered.connect(lambda action: ChangeIODispatcher(action.text()))

        TestMode = QtWidgets.QMenu()
        TestMode.addAction("舰船检测：分辨率32")
        TestMode.addAction("舰船检测：分辨率64")
        TestMode.addAction("舰船检测：分辨率128")
        TestMode.addAction("MobileNet：1000类")
        TestMode.addAction("MobileNet：20类")
        TestModeButton.setMenu(TestMode)
        TestMode.triggered.connect(lambda action: print(action.text()))

    def SetupStatusBar(self):
        self.status = QLabel("工作模式")
        statusBar = QtWidgets.QStatusBar()
        self.setStatusBar(statusBar)
        self.statusBar().addWidget(self.status)


def ChangeIODispatcher(mode):
    if mode == "模式1":
        mode = 1
    elif mode == "模式2":
        mode = 2
    elif mode == "模式3":
        mode = 3
    return function.change_io_mode(mode)

if __name__=="__main__":
    app = QApplication(sys.argv)
    button = VPGUI()
    button.show()
    # button.thread.run(button)
    sys.exit(app.exec_())
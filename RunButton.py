from PyQt5.QtWidgets import QApplication,QLabel
from PyQt5.QtWidgets import QWidget,QFileDialog,QMainWindow
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtGui import *
import sys,os
import warnings
from vpui import *
import cv2

""" VPGUI Mainwindow used for vision chip test platform"""

class VPGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMaximumSize(1920,1080)
        self.setMinimumSize(800,600)
        self.setWindowIcon(QIcon("./icons/png/main.png"))

        self.Version = 1.0
        self.Name = "视觉芯片软件测试平台"
        self.setWindowTitle(self.Name+str(self.Version))

        self.Index = 0

        self.SetupGUI()
        self.BuildConnect()

    def BuildConnect(self):
        self.RunCtrl.ExitButton.clicked.connect(lambda: ExitMessageBox.ExitMessage(self))
        self.RunCtrl.LoadFileButton.clicked.connect(lambda: BrowseFile.FileDialog())
        self.RunCtrl.StartTestButton.clicked.connect(lambda: self.UpdateResult())
        self.RunCtrl.DownloadParamsButton.clicked.connect(lambda: DownloadParamsWindow.DownloadWindow(self))

        self.RunCtrl.StartTestButton.clicked.connect(lambda: print(self.geometry().center()))
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
        RunMenu = self.menuBar().addMenu("运行")
        HelpMenu = self.menuBar().addMenu("帮助")

        OpenFile = FileMenu.addAction("打开")
        PathAct = FileMenu.addAction("路径")
        PreferenceAct = FileMenu.addAction("偏好")
        ExitAct = FileMenu.addAction("退出")

        AboutButton = QtWidgets.QAction("关于")
        AboutButton.setIcon(QIcon("./icons/png/logs.png"))

        HelpButton = QtWidgets.QAction("帮助")
        HelpButton.setIcon(QIcon("./icons/png/what.png"))

        HelpMenu.addAction("查看日志")
        HelpMenu.addAction("帮助")
        HelpMenu.addAction("关于")
        WriteLogAct = EditMenu.addAction("日志")

    def SetupToolBar(self):
        TestModeButton = QtWidgets.QPushButton("测试模式")
        PrepareButton = QtWidgets.QPushButton("初始化")
        PreprocessButton = QtWidgets.QPushButton("预处理")
        UploadButton = QtWidgets.QPushButton("返回结果")
        ResetButton = QtWidgets.QPushButton("复位状态")
        ExitTestButton = QtWidgets.QPushButton("退出测试")
        TestModeButton.setIcon(QIcon("./icons/png/settings.png"))
        ExitTestButton.setIcon(QIcon("./icons/png/stop.png"))
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
        self.toolbar.addWidget(ExitTestButton)

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

    def UpdateResult(self,path='./imgs/tested.png',type="Tested"):
        Img = cv2.imread(path,cv2.COLOR_BGR2RGB)
        self.ResultImg.UpdateImg(Img,type)

if __name__=="__main__":
    app = QApplication(sys.argv)
    button = VPGUI()
    button.show()
    sys.exit(app.exec_())
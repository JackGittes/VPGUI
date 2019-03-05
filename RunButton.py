from PyQt5.QtWidgets import QApplication,QLabel
from PyQt5.QtWidgets import QWidget,QFileDialog,QMainWindow
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtGui import *
import sys,os
import utils
import warnings

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

class LogTab(QWidget):
    def __init__(self):
        super().__init__()
        hLayout = QtWidgets.QHBoxLayout()

        self.Log = QtWidgets.QTabWidget()
        self.Log.addTab(QtWidgets.QTextBrowser(),"实时日志")
        self.Log.addTab(QtWidgets.QTextBrowser(),"错误信息")
        self.Log.addTab(QtWidgets.QTextBrowser(),"状态")
        hLayout.addWidget(self.Log)

        self.setLayout(hLayout)

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

        """A display tool used to control image display mode"""
        self.Origin.setPixmap(QPixmap("./imgs/origin.png"))
        self.Tested.setPixmap(QPixmap("./imgs/tested.png"))

        h1Layout.addWidget(self.Origin)
        h1Layout.addWidget(self.Tested)

        self.PreviousButton = QtWidgets.QPushButton(h2widget)
        self.PlayPauseButton = QtWidgets.QPushButton(h2widget)
        self.NextButton = QtWidgets.QPushButton(h2widget)
        self.Progress = QtWidgets.QProgressBar(h2widget)
        self.Progress.setMinimum(1)
        self.Progress.setMaximum(1000)

        self.SetButtonNames()

        h2Layout.addWidget(self.PreviousButton)
        h2Layout.addWidget(self.PlayPauseButton)
        h2Layout.addWidget(self.NextButton)
        h2Layout.addWidget(self.Progress)

        h1widget.setLayout(h1Layout)
        h2widget.setLayout(h2Layout)

        gLayout.addWidget(h1widget)
        gLayout.addWidget(h2widget)

        self.setLayout(gLayout)

    def SetButtonNames(self):
        self.PreviousButton.setText("上一张")
        self.PlayPauseButton.setText("暂停/播放")
        self.NextButton.setText("下一张")

        self.PreviousButton.setIcon(QIcon("./icons/png/previous_one.png"))
        self.PlayPauseButton.setIcon(QIcon("./icons/png/play.png"))
        self.NextButton.setIcon(QIcon("./icons/png/next_one.png"))

class StatusBottom(QWidget):
    def __init__(self):
        super().__init__()

""" VPGUI Mainwindow used for vision chip test platform"""

class VPGUI(QMainWindow):
    def __init__(self,width=1500,height=900):
        super().__init__()
        if width<800 or height<600:
            width_warn = "Window width shouldn't be less than 800\n"
            height_warn = "Window height shouldn't be less than 600\n"
            warnings.warn(width_warn+height_warn)
            width = 800
            height = 600

        self.Width = width
        self.Height = height

        self.Version = 1.0
        self.Name = "视觉芯片软件测试平台"
        self.setWindowTitle(self.Name+str(self.Version))

        self.SetupGUI()
        self.BuildConnect()

    def BuildConnect(self):
        self.RunCtrl.ExitButton.clicked.connect(lambda: ExitMessageBox(self))
        self.RunCtrl.LoadFileButton.clicked.connect(lambda: self.BrowseFile())
        # self.RunCtrl.DownloadParamsButton.click.connect()
        # self.RunCtrl.StartTestButton.clicked.connect()
        #
        # self.ResultImg.PreviousButton.clicked.connect()
        # self.ResultImg.PlayPauseButton.clicked.connect()
        # self.ResultImg.NextButton.clicked.connect()

    def SetupGUI(self):
        width = self.Width
        height = self.Height

        self.resize(width, height)
        self.setFixedSize(width, height)

        self.SetupMenuBar()
        self.SetupToolBar()

        self.gwidget = QtWidgets.QWidget()

        self.ResultImg = ResultArea()
        self.LogArea = LogTab()
        self.TestArea = TestInfoBox()
        self.RunCtrl = RunButton()

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
        return True

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

    def BrowseFile(self, path=None):
        if path == None:
            path = os.getcwd()
        filename = QFileDialog.getOpenFileName(self, "选择文件", path)
        print(filename[0])
        return filename

    def DownloadParams(self):
        ChooseLoadType = QtWidgets.QMessageBox()
        ChooseLoadType.setWindowTitle("选择下载位置")
        ChooseLoadType.setGeometry(QtCore.QRect(self.Width/2-100,self.Height/2-50,200,100))
        ChooseLoadType.setText("请选择参数下载位置：")

        mpuButton = ChooseLoadType.addButton("MPU",QtWidgets.QMessageBox.YesRole)
        vpButton = ChooseLoadType.addButton("VP",QtWidgets.QMessageBox.YesRole)
        ChooseLoadType.exec_()

        if ChooseLoadType.clickedButton()==mpuButton:
            ChooseLoadType.sender()
        elif ChooseLoadType.clickedButton()==vpButton:
            self.RunStatusMessage.append("正在写入VP")
        else:
            ChooseLoadType.destroy()

def ExitMessageBox(self):
    Msg = QtWidgets.QMessageBox()
    Msg.setGeometry(QtCore.QRect(0, 0, 100, 40))
    IconMap = QPixmap("./icons/png/unlink.png")
    IconMap = IconMap.scaled(60, 60)
    Msg.setIconPixmap(IconMap)
    Msg.setText("确认要退出？")
    Msg.setInformativeText("未保存的信息将丢失")
    Msg.setWindowTitle("提示")
    yesButton = Msg.addButton("确定", QtWidgets.QMessageBox.YesRole)
    Msg.addButton("取消", QtWidgets.QMessageBox.NoRole)
    """Set Messsage Window to Desktop Center"""
    qtRectangle = Msg.frameGeometry()
    centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
    qtRectangle.moveCenter(centerPoint)
    Msg.move(qtRectangle.topLeft())
    Msg.exec_()
    if Msg.clickedButton() == yesButton:
        self.close()

if __name__=="__main__":
    app = QApplication(sys.argv)
    button = VPGUI()
    button.show()
    sys.exit(app.exec_())
from PyQt5.QtWidgets import QApplication,QLabel
from PyQt5.QtWidgets import QWidget,QFileDialog,QMainWindow
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtGui import *
import sys

class RunButton(QWidget):
    def __init__(self):
        super().__init__()
        vLayout = QtWidgets.QVBoxLayout()

        self.ExitButton = QtWidgets.QPushButton("结束并关闭")
        self.ExitButton.setIcon(QIcon("./icons/png/close.png"))

        self.LoadFileButton = QtWidgets.QPushButton("加载数据")
        self.LoadFileButton.setIcon(QIcon("./icons/png/openfile.png"))

        self.DownloadParamsButton = QtWidgets.QPushButton("下载数据",self)
        self.DownloadParamsButton.setIcon(QIcon("./icons/png/down.png"))

        self.StartTestButton = QtWidgets.QPushButton("开始测试",self)
        self.StartTestButton.setIcon(QIcon("./icons/png/start.png"))

        vLayout.addWidget(self.LoadFileButton)
        vLayout.addWidget(self.DownloadParamsButton)
        vLayout.addWidget(self.StartTestButton)
        vLayout.addWidget(self.ExitButton)
        self.setLayout(vLayout)

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

class ResultArea(QWidget):
    def __init__(self):
        super().__init__()
        widget = QtWidgets.QWidget()

        hwidget = QtWidgets.QWidget()
        vwidget = QtWidgets.QWidget()

        hLayout = QtWidgets.QHBoxLayout()
        vLayout = QtWidgets.QVBoxLayout()

        """Two Images to Display"""
        self.Origin = QLabel(widget)
        self.Tested = QLabel(widget)

        """A display tool used to control image display mode"""

        self.Origin.setPixmap(QPixmap("./imgs/origin.png"))
        self.Tested.setPixmap(QPixmap("./imgs/tested.png"))

        hLayout.addWidget(self.Origin)
        hLayout.addWidget(self.Tested)

        self.PreviousButton = QtWidgets.QToolButton(widget)
        self.PlayPauseButton = QtWidgets.QToolButton(widget)
        self.NextButton = QtWidgets.QToolButton(widget)
        self.SetButtonNames()

        vLayout.addWidget(self.PreviousButton)
        vLayout.addWidget(self.PlayPauseButton)
        vLayout.addWidget(self.NextButton)

        self.setLayout(hLayout)

    def SetButtonNames(self):
        self.PreviousButton.setText("上一张")
        self.PlayPauseButton.setText("暂停/播放")
        self.NextButton.setText("下一张")

class StatusBottom(QWidget):
    def __init__(self):
        super().__init__()

""" VPGUI Mainwindow used for vision chip test platform"""

class VPGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.Width = 1200
        self.Height = 800

    def SetupGUI(self):
        width = self.Width
        height = self.Height

        self.resize(width, height)
        self.setFixedSize(width, height)

        self.SetupMenuBar()
        self.SetupToolBar()

        central_widget = QtWidgets.QWidget()

        bottomWidget = QtWidgets.QWidget()

        hLayout = QtWidgets.QHBoxLayout()
        hLayout.addWidget(LogTab())
        hLayout.addWidget(RunButton())
        bottomWidget.setLayout(hLayout)

        vLayout = QtWidgets.QVBoxLayout()
        vLayout.addWidget(ResultArea())
        vLayout.addWidget(bottomWidget)

        central_widget.setLayout(vLayout)

        self.setCentralWidget(central_widget)

        return True

    def SetupMenuBar(self):
        FileMenu = self.menuBar().addMenu("文件")
        EditMenu = self.menuBar().addMenu("编辑")
        SettingMenu = self.menuBar().addMenu("设置")
        RunMenu = self.menuBar().addMenu("运行")
        HelpMenu = self.menuBar().addMenu("帮助")

        PathAct = FileMenu.addAction('工作路径')
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
        ExitTestButton = QtWidgets.QPushButton("退出测试")
        UploadButton = QtWidgets.QPushButton("返回结果")
        TestModeButton.setIcon(QIcon("./icons/png/settings.png"))
        ExitTestButton.setIcon(QIcon("./icons/png/stop.png"))
        PrepareButton.setIcon(QIcon("./icons/png/connect.png"))
        PreprocessButton.setIcon(QIcon("./icons/png/process.png"))
        UploadButton.setIcon(QIcon("./icons/png/upload.png"))

        self.toolbar = self.addToolBar("快捷设置")

        self.toolbar.addWidget(TestModeButton)
        self.toolbar.addWidget(PrepareButton)
        self.toolbar.addWidget(PreprocessButton)
        self.toolbar.addWidget(UploadButton)
        self.toolbar.addWidget(ExitTestButton)

        TestMode = QtWidgets.QMenu()
        TestMode.addAction("舰船检测：分辨率32")
        TestMode.addAction("舰船检测：分辨率64")
        TestMode.addAction("舰船检测：分辨率128")
        TestMode.addAction("MobileNet：1000类")
        TestMode.addAction("MobileNet：20类")
        TestModeButton.setMenu(TestMode)
        TestMode.triggered.connect(lambda action: print(action.text()))


if __name__=="__main__":
    app = QApplication(sys.argv)
    button = VPGUI()
    button.SetupGUI()
    button.show()
    sys.exit(app.exec_())
from PyQt5.QtWidgets import QApplication,QLabel
from PyQt5.QtWidgets import QWidget,QFileDialog,QMainWindow
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtGui import *

import cv2
import sys,os,time
import numpy as np

class EmbTerminal(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(EmbTerminal, self).__init__(parent)
        self.process = QtCore.QProcess(self)
        self.terminal = QtWidgets.QWidget(self)
        self.process.start('xterm',['-into', str(int(self.winId()))])

class VPGUI(QMainWindow):
    def __init__(self,parent=None):
        """Here we initialize VPGUI and set some default params"""
        super(VPGUI, self).__init__(parent)
        self.Name = "视觉芯片测试软件平台"
        self.Width = 1200
        self.Height = 800
        self.Version = "r1.0"
        self.StartTime = 0
        self.Date = time.strftime('%Y_%m_%d_%H%M%S',time.localtime(time.time()))
        self.LogFilePath = "./logs/"

        self.BWidth = 150
        self.BHeight = 40
        self.StandardGap = 40

        """A variable to record current test mode
            0: No test mode choose
            1~5: Self-defined test mode
        """
        self.Status = 0
        self.LogID = open(self.LogFilePath + self.Date + ".log",'w')

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
        self.ExitButton.setIcon(QIcon("./icons/png/close.png"))
        self.ExitButton.setGeometry(QtCore.QRect(width-BW-2*BGAP, height-BH-BGAP, BW, BH))
        self.ExitButton.clicked.connect(self.ExitMessageBox)

        self.LoadFileButton = QtWidgets.QPushButton("加载数据",self)
        self.LoadFileButton.setIcon(QIcon("./icons/png/openfile.png"))
        self.LoadFileButton.setGeometry(QtCore.QRect(width-BW-2*BGAP, height-BH-5.5*BGAP, BW, BH))
        self.LoadFileButton.clicked.connect(self.BrowseFile)

        self.DownloadParamsButton = QtWidgets.QPushButton("下载数据",self)
        self.DownloadParamsButton.setIcon(QIcon("./icons/png/down.png"))
        self.DownloadParamsButton.setGeometry(QtCore.QRect(width-BW-2*BGAP, height-BH-4*BGAP,  BW, BH))
        self.DownloadParamsButton.clicked.connect(self.DownloadParams)

        self.StartTestButton = QtWidgets.QPushButton("开始测试",self)
        self.StartTestButton.setIcon(QIcon("./icons/png/start.png"))
        self.StartTestButton.setGeometry(QtCore.QRect(width-BW-2*BGAP, height-BH-2.5*BGAP, BW, BH))

        # self.RunStatusMessage = QtWidgets.QTextBrowser(self)
        # self.RunStatusMessage.setGeometry(QtCore.QRect(50,height-height/4-BGAP,width/3,height/4))
        # self.RunStatusMessage.verticalScrollBar()
        # self.RunStatusMessage.lineWrapMode()
        self.LogOutput()
        self.CreateImgWindow()
        self.NameInitial()
        self.ToolBarTop()
        self.ShowTestResult()
        self.TopMenuBar()


    def NameInitial(self):
        self.setWindowTitle(self.Name+" "+self.Version)

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
        self.RunStatusMessage.append(filename[0])
        self.LogID.write(filename[0])
        print(filename[0])
        return filename

    def ToolBarTop(self):
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

        toolbar = self.addToolBar("快速设置")

        toolbar.addWidget(TestModeButton)
        toolbar.addWidget(PrepareButton)
        toolbar.addWidget(PreprocessButton)
        toolbar.addWidget(UploadButton)
        toolbar.addWidget(ExitTestButton)

        TestMode = QtWidgets.QMenu()
        TestMode.addAction("舰船检测：分辨率32")
        TestMode.addAction("舰船检测：分辨率64")
        TestMode.addAction("舰船检测：分辨率128")
        TestMode.addAction("MobileNet：1000类")
        TestMode.addAction("MobileNet：20类")
        TestModeButton.setMenu(TestMode)
        TestMode.triggered.connect(lambda action: print(action.text()))

        ExitTestButton.clicked.connect(self.ExitMessageBox)
        PrepareButton.clicked.connect(self.InitDevice)
        # PrepareButton.clicked.connect(self.Preprocess)

    def ExitMessageBox(self):
        Msg = QtWidgets.QMessageBox()
        Msg.setGeometry(QtCore.QRect(0,0, 100, 40))
        IconMap = QPixmap("./icons/png/protect.png")
        IconMap = IconMap.scaled(50,50,QtCore.Qt.SmoothTransformation)
        Msg.setIconPixmap(IconMap)
        Msg.setText("确认要退出？")
        Msg.setInformativeText("未保存的信息将丢失")
        Msg.setWindowTitle("提示")

        yesButton = Msg.addButton("确定",QtWidgets.QMessageBox.YesRole)
        noButton = Msg.addButton("取消", QtWidgets.QMessageBox.NoRole)

        """Set Messsage Window to Desktop Center"""
        qtRectangle = Msg.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        Msg.move(qtRectangle.topLeft())
        Msg.exec_()
        if Msg.clickedButton() == yesButton:
            self.close()

    def TopMenuBar(self):
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

        AboutButton.triggered.connect(self.AboutInfo)

        WriteLogAct = EditMenu.addAction("日志")

    """Here is vision chip test platform help document."""
    def HelpManual(self):
        return True

    """Here is About info in top toolbar."""
    def AboutInfo(self):
        AboutMsg = QtWidgets.QMessageBox()
        AboutMsg.setGeometry(QtCore.QRect(0, 0, 120, 50))
        AboutMsg.setText("视觉芯片测试软件平台\n PyQT5 Copyright©2019 \n 作者：赵明心 \n 版本号:Release 1.0")

        AboutMsg.setWindowTitle("关于")

        OKButton = QtWidgets.QMessageBox.Ok
        AboutMsg.setStandardButtons(OKButton)

        """Set Messsage Window to Desktop Center"""
        qtRectangle = AboutMsg.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        AboutMsg.move(qtRectangle.topLeft())

        return AboutMsg.exec_()

    def ShowTestResult(self):
        print("I'm Ready")

    def InitDevice(self):
        data = function.setup_pcie_driver()
        print(data)
        self.RunStatusMessage.append(data)
        return data

    def CreateStatusBar(self):
        self.statusbar = QtWidgets.QStatusBar()
        barLabel = QLabel("工作模式")
        self.statusbar.addPermanentWidget(barLabel)
        self.setGeometry(self.Width-5,self.Height-10,5,10)

    def DownloadParams(self):
        ChooseLoadType = QtWidgets.QMessageBox()
        ChooseLoadType.setWindowTitle("选择下载位置")
        ChooseLoadType.setGeometry(QtCore.QRect(self.Width/2-100,self.Height/2-50,200,100))
        ChooseLoadType.setText("请选择参数下载位置：")

        mpuButton = ChooseLoadType.addButton("MPU",QtWidgets.QMessageBox.YesRole)
        vpButton = ChooseLoadType.addButton("VP",QtWidgets.QMessageBox.YesRole)
        ChooseLoadType.exec_()

        if ChooseLoadType.clickedButton()==mpuButton:
            self.RunStatusMessage.append("正在写入MPU")
        elif ChooseLoadType.clickedButton()==vpButton:
            self.RunStatusMessage.append("正在写入VP")
        else:
            ChooseLoadType.destroy()

    def LogOutput(self):
        tab_widget = QtWidgets.QTabWidget()
        tab_widget.addTab(QtWidgets.QTextBrowser(), "事件日志")
        tab_widget.addTab(EmbTerminal(), "终端")
        self.LogOut = tab_widget
        self.setGeometry(50,600,300,150)

    def __del__(self):
        self.LogID.close()
        print("VPGUI Closing")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = VPGUI()
    form.SetupUI()
    form.show()
    sys.exit(app.exec_())
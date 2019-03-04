# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'VP_test.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_VisionChip(object):
    def setupUi(self, VisionChip):
        VisionChip.setObjectName("VisionChip")
        VisionChip.resize(627, 636)
        self.LogName = QtWidgets.QLineEdit(VisionChip)
        self.LogName.setGeometry(QtCore.QRect(140, 560, 113, 25))
        self.LogName.setObjectName("LogName")
        self.label_2 = QtWidgets.QLabel(VisionChip)
        self.label_2.setGeometry(QtCore.QRect(80, 560, 41, 17))
        self.label_2.setObjectName("label_2")
        self.TestProgress = QtWidgets.QProgressBar(VisionChip)
        self.TestProgress.setGeometry(QtCore.QRect(140, 360, 118, 23))
        self.TestProgress.setProperty("value", 24)
        self.TestProgress.setObjectName("TestProgress")
        self.StartTest = QtWidgets.QPushButton(VisionChip)
        self.StartTest.setGeometry(QtCore.QRect(140, 400, 89, 25))
        self.StartTest.setObjectName("StartTest")
        self.LoadImgButton = QtWidgets.QPushButton(VisionChip)
        self.LoadImgButton.setGeometry(QtCore.QRect(420, 250, 89, 25))
        self.LoadImgButton.setObjectName("LoadImgButton")
        self.LoadParamsButton = QtWidgets.QPushButton(VisionChip)
        self.LoadParamsButton.setGeometry(QtCore.QRect(420, 290, 141, 25))
        self.LoadParamsButton.setObjectName("LoadParamsButton")
        self.ResetButton = QtWidgets.QPushButton(VisionChip)
        self.ResetButton.setGeometry(QtCore.QRect(420, 330, 141, 25))
        self.ResetButton.setObjectName("ResetButton")
        self.label_3 = QtWidgets.QLabel(VisionChip)
        self.label_3.setGeometry(QtCore.QRect(60, 360, 71, 17))
        self.label_3.setObjectName("label_3")
        self.checkBox = QtWidgets.QCheckBox(VisionChip)
        self.checkBox.setGeometry(QtCore.QRect(140, 530, 92, 23))
        self.checkBox.setObjectName("checkBox")
        self.ExitButton = QtWidgets.QPushButton(VisionChip)
        self.ExitButton.setGeometry(QtCore.QRect(420, 550, 101, 41))
        self.ExitButton.setObjectName("ExitButton")
        self.TestMode = QtWidgets.QTabWidget(VisionChip)
        self.TestMode.setGeometry(QtCore.QRect(60, 50, 311, 291))
        self.TestMode.setObjectName("TestMode")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.TestMode.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.TestMode.addTab(self.tab_2, "")

        self.retranslateUi(VisionChip)
        self.TestMode.setCurrentIndex(0)
        self.StartTest.clicked.connect(self.TestProgress.update)
        self.ExitButton.clicked.connect(VisionChip.close)
        QtCore.QMetaObject.connectSlotsByName(VisionChip)

    def retranslateUi(self, VisionChip):
        _translate = QtCore.QCoreApplication.translate
        VisionChip.setWindowTitle(_translate("VisionChip", "Vision Chip Test"))
        self.label_2.setText(_translate("VisionChip", "名称"))
        self.StartTest.setText(_translate("VisionChip", "开始测试"))
        self.LoadImgButton.setText(_translate("VisionChip", "加载图像"))
        self.LoadParamsButton.setText(_translate("VisionChip", "加载参数文件"))
        self.ResetButton.setText(_translate("VisionChip", "复位所有状态"))
        self.label_3.setText(_translate("VisionChip", "当前进度"))
        self.checkBox.setText(_translate("VisionChip", "写入日志"))
        self.ExitButton.setText(_translate("VisionChip", "结束并退出"))
        self.TestMode.setTabText(self.TestMode.indexOf(self.tab), _translate("VisionChip", "Tab 1"))
        self.TestMode.setTabText(self.TestMode.indexOf(self.tab_2), _translate("VisionChip", "Tab 2"))


if __name__=="__main__":
    import sys
    from PyQt5.QtGui import QIcon
    app=QtWidgets.QApplication(sys.argv)
    widget=QtWidgets.QWidget()
    ui=Ui_VisionChip()
    ui.setupUi(widget)
    widget.setWindowIcon(QIcon('web.png'))
    widget.show()
    sys.exit(app.exec_())


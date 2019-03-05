# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_VP_test(object):
    def setupUi(self, VP_test):
        VP_test.setObjectName("VP_test")
        VP_test.resize(772, 666)
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        VP_test.setFont(font)
        self.VPTitleHint = QtWidgets.QPlainTextEdit(VP_test)
        self.VPTitleHint.setGeometry(QtCore.QRect(100, 50, 251, 41))
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.VPTitleHint.setFont(font)
        self.VPTitleHint.setReadOnly(True)
        self.VPTitleHint.setBackgroundVisible(False)
        self.VPTitleHint.setObjectName("VPTitleHint")
        self.ChooseFolder = QtWidgets.QToolButton(VP_test)
        self.ChooseFolder.setGeometry(QtCore.QRect(460, 260, 201, 51))
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.ChooseFolder.setFont(font)
        self.ChooseFolder.setObjectName("ChooseFolder")
        self.TestInfo = QtWidgets.QListView(VP_test)
        self.TestInfo.setGeometry(QtCore.QRect(100, 180, 256, 192))
        self.TestInfo.setObjectName("TestInfo")
        self.QuitAndClose = QtWidgets.QPushButton(VP_test)
        self.QuitAndClose.setGeometry(QtCore.QRect(450, 550, 261, 41))
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.QuitAndClose.setFont(font)
        self.QuitAndClose.setStyleSheet("font: 75 15pt \"Courier\"\n"
"rgb(239, 41, 41)")
        self.QuitAndClose.setObjectName("QuitAndClose")
        self.TestProgress = QtWidgets.QProgressBar(VP_test)
        self.TestProgress.setGeometry(QtCore.QRect(110, 450, 251, 23))
        self.TestProgress.setProperty("value", 0)
        self.TestProgress.setObjectName("TestProgress")

        self.retranslateUi(VP_test)
        self.QuitAndClose.clicked.connect(VP_test.deleteLater)
        QtCore.QMetaObject.connectSlotsByName(VP_test)

    def retranslateUi(self, VP_test):
        _translate = QtCore.QCoreApplication.translate
        VP_test.setWindowTitle(_translate("VP_test", "Vision Chip Test"))
        self.VPTitleHint.setPlainText(_translate("VP_test", "Vision Chip Test"))
        self.ChooseFolder.setText(_translate("VP_test", "Choose Folder"))
        self.QuitAndClose.setText(_translate("VP_test", "Quit Test and Exit"))


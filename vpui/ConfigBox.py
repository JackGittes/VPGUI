from PyQt5.QtWidgets import QApplication,QLabel
from PyQt5.QtWidgets import QWidget,QFileDialog,QMainWindow
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtGui import *
import sys

t=QtCore.QThreadPool()

t.setMaxThreadCount(3)

class MyThread(QtCore.QRunnable):
    def __init__(self):
        super().__init__()
        # self.autoDelete()
        print("Created.")

    def run(self):
        tt = QtWidgets.QMessageBox()
        tt.setText("你好")
        tt.show()
        tt.exec_()

    def __del__(self):
        print("Deleted")

a = MyThread()
b = MyThread()
c = MyThread()
d = MyThread()

t.tryStart(a)
t.tryStart(b)
print(t.tryStart(c))
print(t.tryStart(d))

print(t.globalInstance())

app = QtWidgets.QApplication(sys.argv)
a.run()
sys.exit(app.exec_())

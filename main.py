import sys
import os
import json

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class AddressBar(QLineEdit):
    def __init__(self):
        super().__init__()
    

class App(QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Web Browser")

        self.StartApp()
        self.setBaseSize(1080,720)


    def StartApp(self):
        self.layout=QVBoxLayout()
        self.tabar=QTabBar(movable=True,tabsClosable=True)
        self.tabar.tabCloseRequested.connect(self.CloseTab)
        self.tabar.addTab("Tab 1")
        self.tabar.addTab("Tab 2")
        self.tabar.setCurrentIndex(0)
        self.layout.addWidget(self.tabar)
        self.setLayout(self.layout)
        self.show()

    def CloseTab(self,i):
        self.tabar.removeTab(i)

if __name__=="__main__":
    app=QApplication(sys.argv)
    window=App()
    sys.exit(app.exec_())




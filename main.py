import sys
import os
import json

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *

class AddressBar(QLineEdit):
    def __init__(self):
        super().__init__()

    def mousePressEvent(self, QMouseEvent):
        self.selectAll()



class App(QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Web Browser")

        self.StartApp()
        self.setBaseSize(1080,720)


    def StartApp(self):
        self.layout=QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)

        self.tabar=QTabBar(movable=True,tabsClosable=True)
        self.tabar.tabCloseRequested.connect(self.CloseTab)

        self.tabar.setCurrentIndex(0)
        self.layout.addWidget(self.tabar)

        self.tabCount=0
        self.tabs=[]

        self.ToolBar=QWidget()
        self.ToolBarLayout=QHBoxLayout()
        self.addressbar=AddressBar()

        self.ToolBar.setLayout(self.ToolBarLayout)
        self.ToolBarLayout.addWidget(self.addressbar)
        self.layout.addWidget(self.ToolBar)

        self.container=QWidget()
        self.container.layout=QStackedLayout()
        self.container.setLayout(self.container.layout)
        self.AddTabButton=QPushButton("+")
        self.ToolBarLayout.addWidget(self.AddTabButton)

        self.AddTabButton.clicked.connect(self.AddTab)

        self.layout.addWidget(self.container)
        self.AddTab()

        self.setLayout(self.layout)
        self.show()

    def CloseTab(self,i):
        self.tabar.removeTab(i)

    def AddTab(self):
        i=self.tabCount
        self.tabs.append(QWidget())
        self.tabs[i].layout=QVBoxLayout()
        self.tabs[i].setObjectName("Tab"+str(i))
        self.tabs[i].content=QWebEngineView()
        self.tabs[i].content.load(QUrl.fromUserInput("http://www.google.com"))
        self.tabs[i].layout.addWidget(self.tabs[i].content)
        self.tabs[i].setLayout(self.tabs[i].layout)
        self.container.layout.addWidget(self.tabs[i])
        self.container.layout.setCurrentWidget(self.tabs[i])
        self.tabar.addTab("New Tab")
        self.tabar.setTabData(i,"tab"+str(i))
        self.tabar.setCurrentIndex(i)


        pass

if __name__=="__main__":
    app=QApplication(sys.argv)
    window=App()
    sys.exit(app.exec_())




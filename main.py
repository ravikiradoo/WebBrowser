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
        self.setWindowTitle("Qt Web Browser")

        self.StartApp()
        self.setBaseSize(1080,720)
        self.setWindowIcon(QIcon("logo.png"))


    def StartApp(self):
        self.layout=QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)

        self.tabar=QTabBar(movable=True,tabsClosable=True)
        self.tabar.tabCloseRequested.connect(self.CloseTab)
        self.tabar.tabBarClicked.connect(self.SwitchTab)

        self.tabar.setCurrentIndex(0)
        self.tabar.setDrawBase(False)
        self.layout.addWidget(self.tabar)





        self.tabCount=0
        self.tabs=[]

        self.ToolBar=QWidget()
        self.ToolBar.setObjectName("Toolbar")
        self.ToolBarLayout=QHBoxLayout()
        self.BackButton = QPushButton("<-")
        self.BackButton.clicked.connect(self.GoBack)
        self.ForwardButton = QPushButton("->")
        self.ForwardButton.clicked.connect(self.GoForward)
        self.ReloadButton=QPushButton("↺")
        self.ReloadButton.clicked.connect(self.Reload)
        self.ToolBarLayout.addWidget(self.BackButton)
        self.ToolBarLayout.addWidget(self.ForwardButton)
        self.ToolBarLayout.addWidget(self.ReloadButton)


        self.addressbar=AddressBar()

        self.ToolBar.setLayout(self.ToolBarLayout)
        self.ToolBarLayout.addWidget(self.addressbar)
        self.addressbar.returnPressed.connect(self.BrowseTo)

        self.layout.addWidget(self.ToolBar)

        self.container=QWidget()
        self.container.layout=QStackedLayout()
        self.container.setLayout(self.container.layout)
        self.AddTabButton=QPushButton("+")
        self.ToolBarLayout.addWidget(self.AddTabButton)

        self.AddTabButton.clicked.connect(self.AddTab)

        self.layout.addWidget(self.container)
        self.AddTab()

        self.newTabShortCut=QShortcut(QKeySequence("Ctrl+N"),self)
        self.newTabShortCut.activated.connect(self.AddTab)

        self.ReloadShortCut=QShortcut(QKeySequence("Ctrl+R"),self)
        self.ReloadShortCut.activated.connect(self.Reload)

        self.BackShortCut=QShortcut(QKeySequence("Ctrl+B"),self)
        self.BackShortCut.activated.connect(self.GoBack)

        self.ForwardShortCut = QShortcut(QKeySequence("Ctrl+F"), self)
        self.ForwardShortCut.activated.connect(self.GoForward)

        index=self.tabar.currentIndex()

        self.ClosedTabShortCut=QShortcut(QKeySequence("Alt+C"),self)
        self.ClosedTabShortCut.activated.connect(lambda :self.CloseTab(index))



        self.setLayout(self.layout)
        self.show()

    def CloseTab(self,i):
        self.tabar.removeTab(i)

    def AddTab(self):
        i=self.tabCount
        self.tabs.append(QWidget())
        self.tabs[i].layout=QVBoxLayout()
        self.tabs[i].layout.setContentsMargins(0,0,0,0)
        self.tabs[i].setObjectName("Tab"+str(i))
        self.tabs[i].content=QWebEngineView()
        self.tabs[i].content.load(QUrl.fromUserInput("http://www.google.com"))
        self.tabs[i].content.titleChanged.connect(lambda : self.setTabContent(i,"title"))
        self.tabs[i].content.iconChanged.connect(lambda: self.setTabContent(i,"icon"))
        self.tabs[i].content.urlChanged.connect(lambda: self.setTabContent(i, "url"))

        self.tabs[i].layout.addWidget(self.tabs[i].content)
        self.tabs[i].setLayout(self.tabs[i].layout)
        self.container.layout.addWidget(self.tabs[i])
        self.container.layout.setCurrentWidget(self.tabs[i])
        self.tabar.addTab("Tab"+str(i))
        self.tabar.setTabData(i,{"Object":"Tab"+str(i),"initial":i})
        self.tabar.setCurrentIndex(i)
        self.tabCount+=1


        pass

    def SwitchTab(self,i):
        tab_data=self.tabar.tabData(i)
        print(tab_data["Object"])
        tab_content=self.findChild(QWidget,tab_data["Object"])
        url=tab_content.content.url().toString()
        self.addressbar.setText(url)
        self.container.layout.setCurrentWidget(tab_content)

    def BrowseTo(self):
        text=self.addressbar.text()
        i=self.tabar.currentIndex()
        tab=self.tabar.tabData(i)
        wv=self.findChild(QWidget,tab["Object"]).content


        if "http" not in text:
            if "." not in text:
                url="https://www.google.co.in/search?q="+text
            else:
                url="http;//"+text
        else:
            url=text


        wv.load(QUrl.fromUserInput(url))

    def setTabContent(self,i,type):
        tab_name=self.tabs[i].objectName()

        count=0
        if type=="url":
            url=self.findChild(QWidget,tab_name).content.url().toString()
            self.addressbar.setText(url)
            return

        while count<=self.tabCount:
            if tab_name==self.tabs[count].objectName():
                if type=="title":
                    title=self.findChild(QWidget,tab_name).content.title()
                    self.tabar.setTabText(count,title)
                    break
                if type=="icon":
                    icon=self.findChild(QWidget,tab_name).content.icon()
                    self.tabar.setTabIcon(count, icon)
                    break

            else:
                count+=1

    def GoBack(self):
        index=self.tabar.currentIndex()
        tab=self.tabar.tabData(index)["Object"]
        wv=self.findChild(QWidget,tab).content
        wv.back()

    def GoForward(self):
        index=self.tabar.currentIndex()
        tab=self.tabar.tabData(index)["Object"]
        wv=self.findChild(QWidget,tab).content
        wv.forward()

    def Reload(self):
        index = self.tabar.currentIndex()
        tab = self.tabar.tabData(index)["Object"]
        wv = self.findChild(QWidget, tab).content
        wv.reload()





if __name__=="__main__":
    app=QApplication(sys.argv)
    os.environ["QTWEBENGINE_REMOTE_DEBUGGING"]="667"
    window=App()

    with open("main.css","r") as style:
        app.setStyleSheet(style.read())

    sys.exit(app.exec_())




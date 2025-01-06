# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 11:46:12 2024

@author: biol0117
"""

import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMainWindow, QStyle, QAction, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import webbrowser
import winwidget
import advwin

basefile = Path(__file__)
basedir = basefile.parents[0]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        title = 'GDSiMS GUI: Gene Drive Simulator of Mosquito Spread' # window title
        left = 300
        top = 150
        width = 1100
        height = 800
        self.setWindowTitle(title)
        self.setGeometry(left, top, width, height) # sets position and size of window
        self.setWindowIcon(QIcon("web.png")) # window icon on corner of window
        
        self.advWindow = advwin.AdvancedWindow(self)
        self.advWindow.hide()
        
        self.centralWidget = winwidget.WindowWidget(self.advWindow)
        self.setCentralWidget(self.centralWidget)

        menu = self.menuBar()
        pixmapi = QStyle.SP_MessageBoxQuestion
        icon = self.style().standardIcon(pixmapi)
        helpMenu = menu.addMenu(icon, "&Help")
        docsAction = QAction("&Documentation site", self)
        docsAction.triggered.connect(self.openDocs)
        docsAction.setStatusTip("Open the project documentation website")
        helpMenu.addAction(docsAction)
        menu.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
    def closeEvent(self, event):
        """Displays a question when the user tries to close the window to ask for confirmation on closing the window."""
        simRunning = self.centralWidget.simRunSpace.isSimRunning()
        if simRunning: # gives specific warning message if sim is running
            reply = QMessageBox.question(self, "Warning", 
                "The simulation is still running.\nAre you sure you want to abort the run and quit?", QMessageBox.Yes | 
                QMessageBox.No, QMessageBox.No)
        else: 
            reply = QMessageBox.question(self, "Message", # creates a message box with a question that the user needs to answer, first string appears in titlebar, second string is message displayed by the dialog
                "Are you sure you want to quit?", QMessageBox.Yes |   # give message in the box and what combination of buttons appear in the dialog, and what the default button is
                QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes: # if user says yes, the widget will close
            event.accept()
            if self.advWindow != None:
                self.advWindow.close()
                self.advWindow = None
            if simRunning:
                self.centralWidget.simRunSpace.abortSim()
            exit()
        else: # otherwise widget won't close
            event.ignore()  
            
    def openDocs(self):
        webbrowser.open("https://acernorth.github.io/GeneralMetapop/")
        
    def getMaxT(self):
        return self.centralWidget.paramSpace.maxTSB.value()
    
    def getNumPat(self):
        return self.centralWidget.paramSpace.numPatSB.value()
        
if __name__ == "__main__":
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv) # creates an application object
    win = MainWindow() # uses class where the main application window is
    win.show()
    sys.exit(app.exec())
    
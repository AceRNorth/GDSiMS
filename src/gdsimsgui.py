# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 11:46:12 2024

@author: biol0117
"""

import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMainWindow, QStyle, QAction, QMessageBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QTimer
import webbrowser
import winwidget
import advwin

# global filepaths
basefile = Path(__file__)
basedir = basefile.parents[0]
appname = Path(basedir / "model" / "gdsimsapp_win.exe")

class ErrorCatcher:
    """Redirects stderr to capture error messages and display in a message box."""
    
    def __init__(self):
        self.oldStderr = sys.stderr  
        sys.stderr = self  # redirect stderr to this class
        self.errorBuffer = ""
        self.timer = QTimer()
        self.timer.setSingleShot(True)  
        self.timer.timeout.connect(self.displayErrorPopUp) # show latest error when timer expires

    def write(self, msg):
        """
        Intercepts stderr messages and shows only the most recent one in a pop-up.

        Parameters
        ----------
        msg : str
            stderr message.

        """
        
        if not msg.isspace():
            self.errorBuffer = msg  
            self.timer.start(500) # wait for more messages before displaying pop-up

    def flush(self):
        """ Required for stderr compatibility. """
        self.oldStderr.flush()
        
    def displayErrorPopUp(self):
        """Displays the most recent error message in a pop-up with an expandable details section."""
        if self.errorBuffer and not self.errorBuffer.isspace():
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("An error occurred")
        
            # Short preview in main message and full message in details section
            shortMsg = self.errorBuffer[:300] + ("..." if len(self.errorBuffer) > 300 else "")
            msgBox.setInformativeText(shortMsg)
            msgBox.setDetailedText(self.errorBuffer)
        
            msgBox.setWindowTitle("Error")
            msgBox.exec_()
            self.errorBuffer = "" # clear buffer

class MainWindow(QMainWindow):
    """ GUI main window frame. """
    
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
        #self.setFont(QFont("Arial", 9))
        
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
        
        # Activate the error catcher at the start of your application
        self.errorCatcher = ErrorCatcher()
        
    def closeEvent(self, event):
        """
        Asks for confirmation to close the window. Aborts the simulation if running. 

        Parameters
        ----------
        event : QCloseEvent

        """
        
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
            if self.advWindow != None:
                self.advWindow.close()
                self.advWindow = None
            if simRunning:
                self.centralWidget.simRunSpace.abortSim()
            event.accept()
        else: # otherwise widget won't close
            event.ignore()  
            
    def openDocs(self):
        """ Opens the documentation site link. """
        webbrowser.open("https://acernorth.github.io/GeneralMetapop/")
        
    def getMaxT(self):
        """ Returns the max_t parameter of the current simulation. """
        return self.centralWidget.paramSpace.maxTSB.value()
    
    def getNumPat(self):
        """ Returns the num_pat parameter of the current simulation. """
        return self.centralWidget.paramSpace.numPatSB.value()
        
if __name__ == "__main__":
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv) # creates an application object
    win = MainWindow() # uses class where the main application window is
    win.show()
    sys.exit(app.exec())
    

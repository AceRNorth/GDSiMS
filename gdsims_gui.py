# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 11:46:12 2024

@author: biol0117
"""

import sys
import os
import logging
from pathlib import Path
import re
import subprocess
import webbrowser
import numpy as np
from PyQt5.QtWidgets import (
    QWidget,
    QMainWindow,
    QAction,
    QStyle,
    QLineEdit,
    QVBoxLayout,
    QSizePolicy,
    QGroupBox,
    QGridLayout,
    QCheckBox,
    QMessageBox,
    QApplication,
    QPushButton,
    QLabel,
    QSpinBox,
    QDoubleSpinBox,
    QFrame,
    QProgressBar, 
    QComboBox,
    QFileDialog,
    QTabWidget,
    QDialog,
    QDialogButtonBox
    )
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, QTimer
from datetime import datetime
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavBar
from matplotlib.figure import Figure
        
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
        
        self.advWindow = AdvancedWindow(self)
        self.advWindow.hide()
        
        self.centralWidget = WindowWidget(self.advWindow)
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

class WindowWidget(QWidget):
    
    def __init__(self, advWindow): 
        super().__init__()
        self.createGridLayout(advWindow) # creates layout to place widgets in window
        
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.mainBox)
        self.setLayout(windowLayout)
        self.show()
        
    def createGridLayout(self, advWindow):
        # widgets
        """Contains all widgets and sets the layout for the main window."""
        
        self.paramSpace = WidgetParams(advWindow)
        self.simRunSpace = WidgetRun(self)
        plotTabs = QTabWidget(self)
        self.plotSpace = WidgetPlot()
        plotTabs.addTab(self.plotSpace, "Totals")
        
        # layout structure
        self.mainBox = QGroupBox()
        layout = QGridLayout()
        
        # 'parameters' box
        parametersBox = QGroupBox()
        layout1 = QGridLayout()
        layout1.addWidget(self.paramSpace, 0, 0, 20, 2)
        #layout1.setContentsMargins(5, 5, 5, 5)
        parametersBox.setLayout(layout1)
        
        # 'running simulation' box
        runSimBox = QGroupBox()
        layout2 = QGridLayout()
        layout2.addWidget(self.simRunSpace, 0, 0, 18, 2)
        #layout2.setContentsMargins(5, 5, 5, 5)
        runSimBox.setLayout(layout2)
        
        # 'plotspace' box
        plotSpaceBox = QGroupBox()
        layout3 = QGridLayout()
        layout3.addWidget(plotTabs, 2, 0, 18, 5)
        #layout3.setContentsMargins(5, 5, 5, 5)
        plotSpaceBox.setLayout(layout3)
        
        layout.addWidget(parametersBox, 0, 0, 3, 1) 
        layout.addWidget(runSimBox, 0, 3, 1, 5)
        layout.addWidget(plotSpaceBox, 1, 3, 5, 5)
        self.mainBox.setLayout(layout)
        
    def createParamsFile(self, outputDir):
        customSet = self.paramSpace.createParamsFile(outputDir)
        return customSet
    
    def runStarted(self):
        self.plotSpace.runStarted()
    
    def runFinished(self, outputDir):
        self.plotSpace.runFinished(outputDir)
        
    def isSimRunning(self):
        self.simRunSpace.isSimRunning()
      
class WidgetParams(QWidget):
    def __init__(self, advWindow):
        super().__init__()
        self.advWindow = advWindow
        self.advWindow.hide()
        
        self.setLayout(QGridLayout())
        self.initUI()
        
        self.initParamSets()
        
    def initUI(self): 
        setsLabel = QLabel("Load a parameter set or choose your own parameters:")
        setsCB = QComboBox()
        setsCB.addItems([
            "Set 1 - default",
            "Set 2 - low fitness cost",
            "Set 3 - high fitness cost",
            "Set 4 - high number of\nrelease sites",
            "Set 5 - low dispersal rate",
            "Set 6 - high dispersal rate"
        ])
        setsCB.resize(setsCB.sizeHint())
        setsCB.setFixedWidth(160)
        setsBtn = QPushButton("Load")
        setsBtn.setToolTip("Load selected parameter set")
        setsBtn.resize(setsBtn.sizeHint())
        setsBtn.clicked.connect(lambda: self.loadSet(setsCB.currentIndex()))
        
        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        pal = line1.palette()
        pal.setColor(QPalette.WindowText, QColor("lightGray"))
        line1.setPalette(pal)
        
        progTitle = QLabel("Progression and model area")
        numRunsLabel = QLabel("num_runs \U0001F6C8")
        numRunsLabel.setToolTip("Number of simulation replicates to run.")
        self.numRunsSB = QSpinBox()
        self.numRunsSB.setMinimum(1)
        self.numRunsSB.setMaximum(10000)
        self.numRunsSB.setValue(1)
        self.numRunsSB.resize(self.numRunsSB.sizeHint())
        maxTLabel = QLabel("max_t")
        maxTLabel.setToolTip("Maximum simulated time (in days).")
        self.maxTSB = QSpinBox()
        self.maxTSB.setMinimum(1)
        self.maxTSB.setMaximum(10000)
        self.maxTSB.setValue(1000)
        self.maxTSB.setSingleStep(100)
        self.maxTSB.resize(self.maxTSB.sizeHint())
        numPatLabel = QLabel("num_pat")
        numPatLabel.setToolTip("Number of population sites chosen for the simulation.")
        self.numPatSB = QSpinBox()
        self.numPatSB.setMinimum(1)
        self.numPatSB.setMaximum(100000)
        self.numPatSB.setValue(100)
        self.numPatSB.setSingleStep(10)
        self.numPatSB.resize(self.numPatSB.sizeHint())
        
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setPalette(pal)
        
        inherTitle = QLabel("Gene drive inheritance")
        xiLabel = QLabel("xi")
        xiLabel.setToolTip("Somatic Cas9 expression fitness cost.")
        self.xiSB = QDoubleSpinBox()
        self.xiSB.setMinimum(0.0)
        self.xiSB.setMaximum(1.0)
        self.xiSB.setValue(0.5)
        self.xiSB.setSingleStep(0.05)
        self.xiSB.resize(self.xiSB.sizeHint())
        eLabel = QLabel("e")
        eLabel.setToolTip("Homing rate in females.")
        self.eSB = QDoubleSpinBox()
        self.eSB.setMinimum(0.0)
        self.eSB.setMaximum(1.0)
        self.eSB.setValue(0.95)
        self.eSB.setSingleStep(0.01)
        self.eSB.resize(self.eSB.sizeHint())
        
        line3 = QFrame()
        line3.setFrameShape(QFrame.HLine)
        line3.setPalette(pal)
        
        releaseTitle = QLabel("Gene drive release")
        driverStartLabel = QLabel("driver_start")
        driverStartLabel.setToolTip("Time to start releasing drive alleles into the mosquito population.")
        self.driverStartSB = QSpinBox()
        self.driverStartSB.setMinimum(1)
        self.driverStartSB.setMaximum(10000)
        self.driverStartSB.setValue(200)
        self.driverStartSB.setSingleStep(100)
        self.driverStartSB.resize(self.driverStartSB.sizeHint())
        
        numDriverMLabel = QLabel("num_driver_M")
        numDriverMLabel.setToolTip("Number of drive heterozygous (WD) male mosquitoes per release.")
        self.numDriverMSB = QSpinBox()
        self.numDriverMSB.setMinimum(0)
        self.numDriverMSB.setMaximum(100000)
        self.numDriverMSB.setValue(1000)
        self.numDriverMSB.setSingleStep(100)
        self.numDriverMSB.resize(self.numDriverMSB.sizeHint())
        numDriverSitesLabel = QLabel("num_driver_sites")
        numDriverSitesLabel.setToolTip("Number of gene drive release sites per year.")
        self.numDriverSitesSB = QSpinBox()
        self.numDriverSitesSB.setMinimum(0)
        self.numDriverSitesSB.setMaximum(100000)
        self.numDriverSitesSB.setValue(1)
        self.numDriverSitesSB.resize(self.numDriverSitesSB.sizeHint())
        
        line4 = QFrame()
        line4.setFrameShape(QFrame.HLine)
        line4.setPalette(pal)

        advancedBtn = QPushButton("Advanced")
        advancedBtn.setToolTip("Advanced parameters")
        advancedBtn.clicked.connect(self.openAdvanced)
        
        self.layout().addWidget(setsLabel, 1, 0, 1, 2)
        self.layout().addWidget(setsCB, 2, 0)
        self.layout().addWidget(setsBtn, 2, 1)
        self.layout().addWidget(line1, 3, 0, 1, 2)
        self.layout().addWidget(progTitle, 4, 0, 1, 2)
        self.layout().addWidget(numRunsLabel, 5, 0)
        self.layout().addWidget(self.numRunsSB, 5, 1)
        self.layout().addWidget(maxTLabel, 6, 0)
        self.layout().addWidget(self.maxTSB, 6, 1)
        self.layout().addWidget(numPatLabel, 7, 0)
        self.layout().addWidget(self.numPatSB, 7, 1)
        self.layout().addWidget(line2, 8, 0, 1, 2)
        self.layout().addWidget(inherTitle, 9, 0, 1, 2)
        self.layout().addWidget(xiLabel, 10, 0)
        self.layout().addWidget(self.xiSB, 10, 1)
        self.layout().addWidget(eLabel, 11, 0)
        self.layout().addWidget(self.eSB, 11, 1)
        self.layout().addWidget(line3, 12, 0, 1, 2)
        self.layout().addWidget(releaseTitle, 13, 0, 1, 2)
        self.layout().addWidget(driverStartLabel, 14, 0)
        self.layout().addWidget(self.driverStartSB, 14, 1)
        self.layout().addWidget(numDriverMLabel, 15, 0)
        self.layout().addWidget(self.numDriverMSB, 15, 1)
        self.layout().addWidget(numDriverSitesLabel, 16, 0)
        self.layout().addWidget(self.numDriverSitesSB, 16, 1)
        self.layout().addWidget(line4, 18, 0, 1, 2)
        self.layout().addWidget(advancedBtn, 19, 0)
      
    def initParamSets(self):
        set1 = InputParams(
                numRuns = 1, 
                maxT = 1000,
                numPat = 100,
                muJ = 0.05,
                muA = 0.125,
                beta = 100.0,
                theta = 9.0,
                compPower = 0.066666667,
                minDev = 10,
                gamma = 0.025,
                xi = 0.5,
                e = 0.95,
                driverStart = 200,
                numDriverM = 1000,
                numDriverSites = 1,
                dispRate = 0.01,
                maxDisp = 0.2,
                psi = 0.0,
                muAes = 0.0,
                tHide1 = 0,
                tHide2 = 0,
                tWake1 = 0,
                tWake2 = 0,
                alpha0Mean = 100000.0,
                alpha0Variance = 0.0,
                alpha1 = 0.0,
                amp = 0.0,
                resp = 0.0,
                recStart = 0,
                recEnd = 1000,
                recIntervalGlobal = 1,
                recIntervalLocal = 200,
                recSitesFreq = 1,
                setLabel = 1,
                dispType = "Radial",
                boundaryType = "Toroid",
                rainfallFile = None,
                coordsFile = None,
                relTimesFile = None
                )
        
        set2 = InputParams(
                numRuns = 1, 
                maxT = 1000,
                numPat = 100,
                muJ = 0.05,
                muA = 0.125,
                beta = 100.0,
                theta = 9.0,
                compPower = 0.066666667,
                minDev = 10,
                gamma = 0.025,
                xi = 0.3,
                e = 0.95,
                driverStart = 200,
                numDriverM = 1000,
                numDriverSites = 1,
                dispRate = 0.01,
                maxDisp = 0.2,
                psi = 0.0,
                muAes = 0.0,
                tHide1 = 0,
                tHide2 = 0,
                tWake1 = 0,
                tWake2 = 0,
                alpha0Mean = 100000.0,
                alpha0Variance = 0.0,
                alpha1 = 0.0,
                amp = 0.0,
                resp = 0.0,
                recStart = 0,
                recEnd = 1000,
                recIntervalGlobal = 1,
                recIntervalLocal = 200,
                recSitesFreq = 1,
                setLabel = 2,
                dispType = "Radial",
                boundaryType = "Toroid",
                rainfallFile = None,
                coordsFile = None,
                relTimesFile = None
                )
        
        set3 = InputParams(
                numRuns = 1, 
                maxT = 1000,
                numPat = 100,
                muJ = 0.05,
                muA = 0.125,
                beta = 100.0,
                theta = 9.0,
                compPower = 0.066666667,
                minDev = 10,
                gamma = 0.025,
                xi = 0.7,
                e = 0.95,
                driverStart = 200,
                numDriverM = 1000,
                numDriverSites = 1,
                dispRate = 0.01,
                maxDisp = 0.2,
                psi = 0.0,
                muAes = 0.0,
                tHide1 = 0,
                tHide2 = 0,
                tWake1 = 0,
                tWake2 = 0,
                alpha0Mean = 100000.0,
                alpha0Variance = 0.0,
                alpha1 = 0.0,
                amp = 0.0,
                resp = 0.0,
                recStart = 0,
                recEnd = 1000,
                recIntervalGlobal = 1,
                recIntervalLocal = 200,
                recSitesFreq = 1,
                setLabel = 3,
                dispType = "Radial",
                boundaryType = "Toroid",
                rainfallFile = None,
                coordsFile = None,
                relTimesFile = None
                )
        
        set4 = InputParams(
                numRuns = 1, 
                maxT = 1000,
                numPat = 100,
                muJ = 0.05,
                muA = 0.125,
                beta = 100.0,
                theta = 9.0,
                compPower = 0.066666667,
                minDev = 10,
                gamma = 0.025,
                xi = 0.5,
                e = 0.95,
                driverStart = 200,
                numDriverM = 1000,
                numDriverSites = 10,
                dispRate = 0.01,
                maxDisp = 0.2,
                psi = 0.0,
                muAes = 0.0,
                tHide1 = 0,
                tHide2 = 0,
                tWake1 = 0,
                tWake2 = 0,
                alpha0Mean = 100000.0,
                alpha0Variance = 0.0,
                alpha1 = 0.0,
                amp = 0.0,
                resp = 0.0,
                recStart = 0,
                recEnd = 1000,
                recIntervalGlobal = 1,
                recIntervalLocal = 200,
                recSitesFreq = 1,
                setLabel = 4,
                dispType = "Radial",
                boundaryType = "Toroid",
                rainfallFile = None,
                coordsFile = None,
                relTimesFile = None
                )
        
        set5 = InputParams(
                numRuns = 1, 
                maxT = 1000,
                numPat = 100,
                muJ = 0.05,
                muA = 0.125,
                beta = 100.0,
                theta = 9.0,
                compPower = 0.066666667,
                minDev = 10,
                gamma = 0.025,
                xi = 0.5,
                e = 0.95,
                driverStart = 200,
                numDriverM = 1000,
                numDriverSites = 1,
                dispRate = 0.002,
                maxDisp = 0.2,
                psi = 0.0,
                muAes = 0.0,
                tHide1 = 0,
                tHide2 = 0,
                tWake1 = 0,
                tWake2 = 0,
                alpha0Mean = 100000.0,
                alpha0Variance = 0.0,
                alpha1 = 0.0,
                amp = 0.0,
                resp = 0.0,
                recStart = 0,
                recEnd = 1000,
                recIntervalGlobal = 1,
                recIntervalLocal = 200,
                recSitesFreq = 1,
                setLabel = 5,
                dispType = "Radial",
                boundaryType = "Toroid",
                rainfallFile = None,
                coordsFile = None,
                relTimesFile = None
                )
        
        set6 = InputParams(
                numRuns = 1, 
                maxT = 1000,
                numPat = 100,
                muJ = 0.05,
                muA = 0.125,
                beta = 100.0,
                theta = 9.0,
                compPower = 0.066666667,
                minDev = 10,
                gamma = 0.025,
                xi = 0.5,
                e = 0.95,
                driverStart = 200,
                numDriverM = 1000,
                numDriverSites = 1,
                dispRate = 0.05,
                maxDisp = 0.2,
                psi = 0.0,
                muAes = 0.0,
                tHide1 = 0,
                tHide2 = 0,
                tWake1 = 0,
                tWake2 = 0,
                alpha0Mean = 100000.0,
                alpha0Variance = 0.0,
                alpha1 = 0.0,
                amp = 0.0,
                resp = 0.0,
                recStart = 0,
                recEnd = 1000,
                recIntervalGlobal = 1,
                recIntervalLocal = 200,
                recSitesFreq = 1,
                setLabel = 6,
                dispType = "Radial",
                boundaryType = "Toroid",
                rainfallFile = None,
                coordsFile = None,
                relTimesFile = None
                )
         
        self.sets = [set1, set2, set3, set4, set5, set6] 
        
    def loadSet(self, setIndex):
        # clear previous box options
        self.advWindow.aesCheckbox.setChecked(False)
        self.advWindow.rainfallFileCheckbox.setChecked(False)
        self.advWindow.coordsFileCheckbox.setChecked(False)
        self.advWindow.relTimesFileCheckbox.setChecked(False)
        self.advWindow.dispTypeCB.setCurrentText("Radial")
        self.advWindow.boundaryTypeCB.setCurrentText("Toroid")
        self.advWindow.rainfallFilenameEdit.setText("")
        self.advWindow.coordsFilenameEdit.setText("")
        self.advWindow.relTimesFilenameEdit.setText("")
            
        if self.sets[setIndex].psi != 0:
            self.advWindow.aesCheckbox.setChecked(True)
        if self.sets[setIndex].rainfallFile != None:
            self.advWindow.rainfallFileCheckbox.setChecked(True)
        if self.sets[setIndex].coordsFile != None:
            self.advWindow.coordsFileCheckbox.setChecked(True)
        if self.sets[setIndex].relTimesFile != None:
            self.advWindow.relTimesFileCheckbox.setChecked(True)
        
        self.numRunsSB.setValue(self.sets[setIndex].numRuns)
        self.maxTSB.setValue(self.sets[setIndex].maxT)
        self.numPatSB.setValue(self.sets[setIndex].numPat)
        self.xiSB.setValue(self.sets[setIndex].xi)
        self.eSB.setValue(self.sets[setIndex].e)
        self.driverStartSB.setValue(self.sets[setIndex].driverStart)
        self.numDriverMSB.setValue(self.sets[setIndex].numDriverM)
        self.numDriverSitesSB.setValue(self.sets[setIndex].numDriverSites)
        self.advWindow.setLabelSB.setValue(self.sets[setIndex].setLabel)
        self.advWindow.recIntervalGlobalSB.setValue(self.sets[setIndex].recIntervalGlobal)
        self.advWindow.recStartSB.setValue(self.sets[setIndex].recStart)
        self.advWindow.recEndSB.setValue(self.sets[setIndex].recEnd)
        self.advWindow.recIntervalLocalSB.setValue(self.sets[setIndex].recIntervalLocal)
        self.advWindow.recSitesFreqSB.setValue(self.sets[setIndex].recSitesFreq)
        self.advWindow.muJSB.setValue(self.sets[setIndex].muJ)
        self.advWindow.muASB.setValue(self.sets[setIndex].muA)
        self.advWindow.betaSB.setValue(self.sets[setIndex].beta)
        self.advWindow.thetaSB.setValue(self.sets[setIndex].theta)
        self.advWindow.compPowerSB.setValue(self.sets[setIndex].compPower)
        self.advWindow.minDevSB.setValue(self.sets[setIndex].minDev)
        self.advWindow.dispRateSB.setValue(self.sets[setIndex].dispRate)
        self.advWindow.maxDispSB.setValue(self.sets[setIndex].maxDisp)
        self.advWindow.dispTypeCB.setCurrentText(self.sets[setIndex].dispType)
        self.advWindow.psiSB.setValue(self.sets[setIndex].psi)
        self.advWindow.muAesSB.setValue(self.sets[setIndex].muAes)
        self.advWindow.tHide1SB.setValue(self.sets[setIndex].tHide1)
        self.advWindow.tHide2SB.setValue(self.sets[setIndex].tHide2)
        self.advWindow.tWake1SB.setValue(self.sets[setIndex].tWake1)
        self.advWindow.tWake2SB.setValue(self.sets[setIndex].tWake2)
        self.advWindow.alpha0MeanSB.setValue(self.sets[setIndex].alpha0Mean)
        self.advWindow.alpha0VarSB.setValue(self.sets[setIndex].alpha0Variance)
        self.advWindow.alpha1SB.setValue(self.sets[setIndex].alpha1)
        self.advWindow.ampSB.setValue(self.sets[setIndex].amp)
        self.advWindow.respSB.setValue(self.sets[setIndex].resp)
        self.advWindow.boundaryTypeCB.setCurrentText(self.sets[setIndex].boundaryType)
        self.advWindow.gammaSB.setValue(self.sets[setIndex].gamma)
        self.advWindow.rainfallFilenameEdit.setText(self.sets[setIndex].rainfallFile)
        self.advWindow.coordsFilenameEdit.setText(self.sets[setIndex].coordsFile)
        self.advWindow.relTimesFilenameEdit.setText(self.sets[setIndex].relTimesFile)
        
        self.advWindow.saveValues()
        
    def openAdvanced(self):
        """ Opens a new window for advanced parameters."""
        self.advWindow.openWin()
        
    def checkBounds(self):
        self.advWindow.checkBounds()
        
    def createParamsFile(self, outputDirPath):
        advParams = self.advWindow.getParams()
        self.customSet = InputParams(
                            numRuns = self.numRunsSB.value(), 
                            maxT = self.maxTSB.value(),
                            numPat = self.numPatSB.value(),
                            muJ = advParams.muJ,
                            muA = advParams.muA,
                            beta = advParams.beta,
                            theta = advParams.theta,
                            compPower = advParams.compPower,
                            minDev = advParams.minDev,
                            gamma = advParams.gamma,
                            xi = self.xiSB.value(),
                            e = self.eSB.value(),
                            driverStart = self.driverStartSB.value(),
                            numDriverM = self.numDriverMSB.value(),
                            numDriverSites = self.numDriverSitesSB.value(),
                            dispRate = advParams.dispRate,
                            maxDisp = advParams.maxDisp,
                            psi = advParams.psi,
                            muAes = advParams.muAes,
                            tHide1 = advParams.tHide1,
                            tHide2 = advParams.tHide2,
                            tWake1 = advParams.tWake1,
                            tWake2 = advParams.tWake2,
                            alpha0Mean = advParams.alpha0Mean,
                            alpha0Variance = advParams.alpha0Var,
                            alpha1 = advParams.alpha1,
                            amp = advParams.amp,
                            resp = advParams.resp,
                            recStart = advParams.recStart,
                            recEnd = advParams.recEnd,
                            recIntervalGlobal = advParams.recIntervalGlobal,
                            recIntervalLocal = advParams.recIntervalLocal,
                            recSitesFreq = advParams.recSitesFreq,
                            setLabel = advParams.setLabel,
                            dispType = self.advWindow.dispType,
                            boundaryType = self.advWindow.boundaryType,
                            rainfallFile = None if advParams.rainfallFile == False else self.advWindow.rainfallFile,
                            coordsFile = None if advParams.patchCoordsFile == False else self.advWindow.coordsFile,
                            relTimesFile = None if advParams.relTimesFile == False else self.advWindow.relTimesFile
                        )
    
        
        # turn class data into "params.txt" file in selected outputDir path
        filePath = outputDirPath / "params.txt"
        with open(filePath, "w") as file:
            file.write(str(self.customSet.numRuns) + "\n")
            file.write(str(self.customSet.maxT) + "\n")
            file.write(str(self.customSet.numPat) + "\n")
            file.write(str(self.customSet.muJ) + "\n")
            file.write(str(self.customSet.muA) + "\n")
            file.write(str(self.customSet.beta) + "\n")
            file.write(str(self.customSet.theta) + "\n")
            file.write(str(self.customSet.compPower) + "\n")
            file.write(str(self.customSet.minDev) + "\n")
            file.write(str(self.customSet.gamma) + "\n")
            file.write(str(self.customSet.xi) + "\n")
            file.write(str(self.customSet.e) + "\n")
            file.write(str(self.customSet.driverStart) + "\n")
            file.write(str(self.customSet.numDriverM) + "\n")
            file.write(str(self.customSet.numDriverSites) + "\n")
            file.write(str(self.customSet.dispRate) + "\n")
            file.write(str(self.customSet.maxDisp) + "\n")
            file.write(str(self.customSet.psi) + "\n")
            file.write(str(self.customSet.muAes) + "\n")
            file.write(str(self.customSet.tHide1) + "\n")
            file.write(str(self.customSet.tHide2) + "\n")
            file.write(str(self.customSet.tWake1) + "\n")
            file.write(str(self.customSet.tWake2) + "\n")
            file.write(str(self.customSet.alpha0Mean) + "\n")
            file.write(str(self.customSet.alpha0Variance) + "\n")
            file.write(str(self.customSet.alpha1) + "\n")
            file.write(str(self.customSet.amp) + "\n")
            file.write(str(self.customSet.resp) + "\n")
            file.write(str(self.customSet.recStart) + "\n")
            file.write(str(self.customSet.recEnd) + "\n")
            file.write(str(self.customSet.recIntervalGlobal) + "\n")
            file.write(str(self.customSet.recIntervalLocal) + "\n")
            file.write(str(self.customSet.recSitesFreq) + "\n")
            file.write(str(self.customSet.setLabel) + "\n")
            
        return self.customSet
      
class InputParams():
    def __init__(self, numRuns, maxT, numPat, muJ, muA, beta, theta, compPower, minDev, gamma, xi, e, driverStart, numDriverM,
                 numDriverSites, dispRate, maxDisp, psi, muAes, tHide1, tHide2, tWake1, tWake2, alpha0Mean, alpha0Variance, alpha1,
                 amp, resp, recStart, recEnd, recIntervalGlobal, recIntervalLocal, recSitesFreq, setLabel, dispType, boundaryType,
                 rainfallFile, coordsFile, relTimesFile):
        self.numRuns = numRuns
       	self.maxT = maxT
       	self.numPat = numPat
       	self.muJ = muJ
       	self.muA = muA
       	self.beta = beta
       	self.theta = theta
       	self.compPower = compPower
       	self.minDev = minDev
        self.gamma = gamma
       	self.xi = xi
       	self.e = e
        self.driverStart = driverStart
       	self.numDriverM = numDriverM
       	self.numDriverSites = numDriverSites
        self.dispRate = dispRate
       	self.maxDisp = maxDisp
       	self.psi = psi
       	self.muAes = muAes
       	self.tHide1 = tHide1
       	self.tHide2 = tHide2
       	self.tWake1 = tWake1
       	self.tWake2 = tWake2
        self.alpha0Mean = alpha0Mean
        self.alpha0Variance = alpha0Variance
        self.alpha1 = alpha1
        self.amp = amp
        self.resp = resp
       	self.recStart = recStart
       	self.recEnd = recEnd
        self.recIntervalGlobal = recIntervalGlobal
       	self.recIntervalLocal = recIntervalLocal
       	self.recSitesFreq = recSitesFreq
       	self.setLabel = setLabel
        self.dispType = dispType
        self.boundaryType = boundaryType
        self.rainfallFile = rainfallFile
        self.coordsFile = coordsFile
        self.relTimesFile = relTimesFile
      
class AdvancedWindow(QDialog):
    
    def __init__(self, parentWin):
        super().__init__()
        self.title = 'Advanced parameters' 
        self.left = 600
        self.top = 150
        self.width = 900
        self.height = 700
        self.setWindowIcon(QIcon('web.png')) 
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint) # removes window help button
        self.parentWindow = parentWin
        
        self.lastVals = AdvParams()
        self.rainfallFile = None
        self.coordsFile = None
        self.relTimesFile = None
    
        self.initUI()    
        
    def initUI(self):    
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height) # sets position and size of window
    
        self.createGridLayout() # creates layout to place widgets in window
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
        self.openWin()
        
    def openWin(self):
        #self.applyBtn.setEnabled(False) # ?
        self.show()
        self.activateWindow() # moves the window to the top
        self.saveValues() # save starting values in case need to reset when close window without saving
        self.okBtn.setDefault(True)
        self.okBtn.setAutoDefault(True)
        
    def closeEvent(self, event):
        self.hide()
    
        # reset all values to their defaults
        self.setLabelSB.setValue(self.lastVals.setLabel)
        self.recIntervalGlobalSB.setValue(self.lastVals.recIntervalGlobal)
        self.recStartSB.setValue(self.lastVals.recStart)
        self.recEndSB.setValue(self.lastVals.recEnd)
        self.recIntervalLocalSB.setValue(self.lastVals.recIntervalLocal)
        self.recSitesFreqSB.setValue(self.lastVals.recSitesFreq)
        self.muJSB.setValue(self.lastVals.muJ)
        self.muASB.setValue(self.lastVals.muA)
        self.betaSB.setValue(self.lastVals.beta)
        self.thetaSB.setValue(self.lastVals.theta)
        self.compPowerSB.setValue(self.lastVals.compPower)
        self.minDevSB.setValue(self.lastVals.minDev)
        self.dispRateSB.setValue(self.lastVals.dispRate)
        self.maxDispSB.setValue(self.lastVals.maxDisp)
        self.dispTypeCB.setCurrentText(self.lastVals.dispType)
        self.aesCheckbox.setChecked(self.lastVals.aestivation)
        self.psiSB.setValue(self.lastVals.psi)
        self.muAesSB.setValue(self.lastVals.muAes)
        self.tHide1SB.setValue(self.lastVals.tHide1)
        self.tHide2SB.setValue(self.lastVals.tHide2)
        self.tWake1SB.setValue(self.lastVals.tWake1)
        self.tWake2SB.setValue(self.lastVals.tWake2)
        self.alpha0MeanSB.setValue(self.lastVals.alpha0Mean)
        self.alpha0VarSB.setValue(self.lastVals.alpha0Var)
        self.alpha1SB.setValue(self.lastVals.alpha1)
        self.ampSB.setValue(self.lastVals.amp)
        self.rainfallFileCheckbox.setChecked(self.lastVals.rainfallFile)
        self.rainfallFilenameEdit.setText(self.lastVals.rainfallFilename)
        self.boundaryTypeCB.setCurrentText(self.lastVals.boundaryType)
        self.coordsFileCheckbox.setChecked(self.lastVals.patchCoordsFile)
        self.coordsFilenameEdit.setText(self.lastVals.patchCoordsFilename)
        self.gammaSB.setValue(self.lastVals.gamma)
        self.relTimesFileCheckbox.setChecked(self.lastVals.relTimesFile)
        self.relTimesFilenameEdit.setText(self.lastVals.relTimesFilename)
        
        self.applyBtn.setEnabled(False) # closing resets changes so don't need this enabled anymore
        
        event.ignore()
        
    def saveValues(self):
        """ Save last applied changes to values for update of UI components and parameter values on run. """
        self.lastVals.setLabel = self.setLabelSB.value()
        self.lastVals.recIntervalGlobal = self.recIntervalGlobalSB.value()
        self.lastVals.recStart = self.recStartSB.value()
        self.lastVals.recEnd = self.recEndSB.value()
        self.lastVals.recIntervalLocal = self.recIntervalLocalSB.value()
        self.lastVals.recSitesFreq = self.recSitesFreqSB.value()
        self.lastVals.muJ = self.muJSB.value()
        self.lastVals.muA = self.muASB.value()
        self.lastVals.beta = self.betaSB.value()
        self.lastVals.theta = self.thetaSB.value()
        self.lastVals.compPower = self.compPowerSB.value()
        self.lastVals.minDev = self.minDevSB.value()
        self.lastVals.dispRate = self.dispRateSB.value()
        self.lastVals.maxDisp = self.maxDispSB.value()
        self.lastVals.dispType = self.dispTypeCB.currentText()
        self.lastVals.aestivation = self.aesCheckbox.isChecked()
        self.lastVals.psi = self.psiSB.value()
        self.lastVals.muAes = self.muAesSB.value()
        self.lastVals.tHide1 = self.tHide1SB.value()
        self.lastVals.tHide2 = self.tHide2SB.value()
        self.lastVals.tWake1 = self.tWake1SB.value()
        self.lastVals.tWake2 = self.tWake2SB.value()
        self.lastVals.alpha0Mean = self.alpha0MeanSB.value()
        self.lastVals.alpha0Var = self.alpha0VarSB.value()
        self.lastVals.alpha1 = self.alpha1SB.value()
        self.lastVals.amp = self.ampSB.value()
        self.lastVals.rainfallFile = self.rainfallFileCheckbox.isChecked()
        self.lastVals.rainfallFilename = self.rainfallFilenameEdit.text()
        self.lastVals.resp = self.respSB.value()
        self.lastVals.boundaryType = self.boundaryTypeCB.currentText()
        self.lastVals.patchCoordsFile = self.coordsFileCheckbox.isChecked()
        self.lastVals.patchCoordsFilename = self.coordsFilenameEdit.text()
        self.lastVals.gamma = self.gammaSB.value()
        self.lastVals.relTimesFile = self.relTimesFileCheckbox.isChecked()
        self.lastVals.relTimesFilename = self.relTimesFilenameEdit.text()
        
        self.boundaryType = self.lastVals.boundaryType
        self.dispType = self.lastVals.dispType
        self.rainfallFile = self.lastVals.rainfallFilename
        self.coordsFile = self.lastVals.patchCoordsFilename
        self.relTimesFile = self.lastVals.relTimesFilename
    
    def getParams(self):
        return self.lastVals
    
    def createGridLayout(self):
        # widgets
        """Contains all widgets and sets the layout for the advanced parameters window."""
        self.horizontalGroupBox = QGroupBox()
        self.layout = QGridLayout()
        
        recTitle = QLabel("Recording")
        setLabelLabel = QLabel("set_label")
        setLabelLabel.setToolTip("'Set of repetitions' index label for output files.")
        self.setLabelSB = QSpinBox()
        self.setLabelSB.setMaximum(10000000)
        self.setLabelSB.setValue(1)
        self.setLabelSB.resize(self.setLabelSB.sizeHint())
        self.setLabelSB.valueChanged.connect(self.enableApply)
        recIntervalGlobalLabel = QLabel("rec_interval_global")
        recIntervalGlobalLabel.setToolTip("Time interval for global data recording/output.")
        self.recIntervalGlobalSB = QSpinBox()
        self.recIntervalGlobalSB.setMinimum(1)
        self.recIntervalGlobalSB.setMaximum(100000)
        self.recIntervalGlobalSB.setValue(1)
        self.recIntervalGlobalSB.setSingleStep(100)
        self.recIntervalGlobalSB.resize(self.recIntervalGlobalSB.sizeHint())
        self.recIntervalGlobalSB.valueChanged.connect(self.enableApply)
        recStartLabel = QLabel("rec_start")
        recStartLabel.setToolTip("Start time for the data recording window (inclusive).")
        self.recStartSB = QSpinBox()
        self.recStartSB.setMinimum(0)
        self.recStartSB.setMaximum(100000)
        self.recStartSB.setValue(0)
        self.recStartSB.setSingleStep(100)
        self.recStartSB.resize(self.recStartSB.sizeHint())
        self.recStartSB.valueChanged.connect(self.enableApply)
        recEndLabel = QLabel("rec_end")
        recEndLabel.setToolTip("End time for the data recording window (inclusive).")
        self.recEndSB = QSpinBox()
        self.recEndSB.setMinimum(0) # should be rec_start
        self.recEndSB.setMaximum(100000)
        self.recEndSB.setValue(1000)
        self.recEndSB.setSingleStep(100)
        self.recEndSB.resize(self.recEndSB.sizeHint())
        self.recEndSB.valueChanged.connect(self.enableApply)
        recIntervalLocalLabel = QLabel("rec_interval_local")
        recIntervalLocalLabel.setToolTip("Time interval at which to collect/record local data (in days).")
        self.recIntervalLocalSB = QSpinBox()
        self.recIntervalLocalSB.setMinimum(1)
        self.recIntervalLocalSB.setMaximum(100000)
        self.recIntervalLocalSB.setValue(200)
        self.recIntervalLocalSB.setSingleStep(100)
        self.recIntervalLocalSB.resize(self.recIntervalLocalSB.sizeHint())
        self.recIntervalLocalSB.valueChanged.connect(self.enableApply)
        recSitesFreqLabel = QLabel("rec_sites_freq")
        recSitesFreqLabel.setToolTip("Fraction of sites to collect local data for (1 is all sites, 10 is 1 in 10 etc).")
        self.recSitesFreqSB = QSpinBox()
        self.recSitesFreqSB.setValue(1)
        self.recSitesFreqSB.setMinimum(1)
        self.recSitesFreqSB.setMaximum(100000)
        self.recSitesFreqSB.setSingleStep(5)
        self.recSitesFreqSB.resize(self.recSitesFreqSB.sizeHint())
        self.recSitesFreqSB.valueChanged.connect(self.enableApply)
        
        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        pal = line1.palette()
        pal.setColor(QPalette.WindowText, QColor("lightGray"))
        line1.setPalette(pal)
        
        lifeTitle = QLabel("Mosquito life processes")
        muJLabel = QLabel("mu_j")
        muJLabel.setToolTip("Juvenile density independent mortality rate per day.")
        self.muJSB = QDoubleSpinBox()
        self.muJSB.setMinimum(0)
        self.muJSB.setMaximum(0.99) # should not include 1
        self.muJSB.setValue(0.05)
        self.muJSB.setSingleStep(0.05)
        self.muJSB.resize(self.muJSB.sizeHint())
        self.muJSB.valueChanged.connect(self.enableApply)
        muALabel = QLabel("mu_a")
        muALabel.setToolTip("Adult mortality rate per day.")
        self.muASB = QDoubleSpinBox()
        self.muASB.setDecimals(3)
        self.muASB.setMinimum(0.001) # should not include 0
        self.muASB.setMaximum(0.999) # should not include 1
        self.muASB.setValue(0.125)
        self.muASB.setSingleStep(0.005)
        self.muASB.resize(self.muASB.sizeHint())
        self.muASB.valueChanged.connect(self.enableApply)
        betaLabel = QLabel("beta")
        betaLabel.setToolTip("Parameter that controls mating rate.")
        self.betaSB = QDoubleSpinBox()
        self.betaSB.setMinimum(0.01) # should not include 0
        self.betaSB.setMaximum(10000) # ?
        self.betaSB.setValue(100)
        self.betaSB.setSingleStep(10)
        self.betaSB.resize(self.betaSB.sizeHint())
        self.betaSB.valueChanged.connect(self.enableApply)
        thetaLabel = QLabel("theta")
        thetaLabel.setToolTip("Average egg laying rate of wildtype females (eggs per day).")
        self.thetaSB = QDoubleSpinBox()
        self.thetaSB.setMinimum(0.01) # should not include 0
        self.thetaSB.setMaximum(10000)
        self.thetaSB.setValue(9)
        self.thetaSB.resize(self.thetaSB.sizeHint())
        self.thetaSB.valueChanged.connect(self.enableApply)
        compPowerLabel = QLabel("comp_power")
        compPowerLabel.setToolTip("Parameter that controls the juvenile survival probability.")
        self.compPowerSB = QDoubleSpinBox()
        self.compPowerSB.setMinimum(0.000000001) # should not include 0
        self.compPowerSB.setMaximum(10000)
        self.compPowerSB.setDecimals(9)
        self.compPowerSB.setValue(0.066666667)
        self.compPowerSB.setSingleStep(0.1)
        self.compPowerSB.resize(self.compPowerSB.sizeHint())
        self.compPowerSB.valueChanged.connect(self.enableApply)
        minDevLabel = QLabel("min_dev")
        minDevLabel.setToolTip("Minimum development time for a juvenile (in days).")
        self.minDevSB = QSpinBox()
        self.minDevSB.setMinimum(1) # should not include 0
        self.minDevSB.setMaximum(10000)
        self.minDevSB.setValue(10)
        self.minDevSB.resize(self.minDevSB.sizeHint())
        self.minDevSB.valueChanged.connect(self.enableApply)
    
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setPalette(pal)    
    
        dispTitle = QLabel("Dispersal")
        dispRateLabel = QLabel("disp_rate")
        dispRateLabel.setToolTip("Adult dispersal rate.")
        self.dispRateSB = QDoubleSpinBox()
        self.dispRateSB.setDecimals(3)
        self.dispRateSB.setMinimum(0)
        self.dispRateSB.setMaximum(1)
        self.dispRateSB.setValue(0.01)
        self.dispRateSB.setSingleStep(0.005)
        self.dispRateSB.resize(self.dispRateSB.sizeHint())
        self.dispRateSB.valueChanged.connect(self.enableApply)
        maxDispLabel = QLabel("max_disp")
        maxDispLabel.setToolTip("Maximum dispersal distance at which two sites are connected.")
        self.maxDispSB = QDoubleSpinBox()
        self.maxDispSB.setMinimum(0.01) # should not include 0
        self.maxDispSB.setMaximum(10000) # should be side
        self.maxDispSB.setValue(0.2)
        self.maxDispSB.resize(self.maxDispSB.sizeHint())
        self.maxDispSB.valueChanged.connect(self.enableApply)
        dispTypeLabel = QLabel("dispersal type")
        self.dispTypeCB = QComboBox()
        self.dispTypeCB.addItems(["Radial", "Distance kernel"])
        self.dispTypeCB.currentTextChanged.connect(self.enableApply)
        
        line3 = QFrame()
        line3.setFrameShape(QFrame.HLine)
        line3.setPalette(pal)
        
        aesTitle = QLabel("Aestivation")
        self.aesCheckbox = QCheckBox()
        self.aesCheckbox.stateChanged.connect(lambda: self.checkboxState(self.aesCheckbox,
            showLabelElements=[psiLabel, muAesLabel, tHide1Label, tHide2Label, tWake1Label, tWake2Label],
            showNumElements=[self.psiSB, self.muAesSB, self.tHide1SB, self.tHide2SB, self.tWake1SB, self.tWake2SB])
        )
        self.aesCheckbox.stateChanged.connect(self.enableApply)
        psiLabel = QLabel("psi")
        psiLabel.setToolTip("Aestivation rate.")
        self.psiSB = QDoubleSpinBox()
        self.psiSB.setMinimum(0)
        self.psiSB.setMaximum(1)
        self.psiSB.setValue(0)
        self.psiSB.setSingleStep(0.05)
        self.psiSB.resize(self.psiSB.sizeHint())
        self.psiSB.valueChanged.connect(self.enableApply)
        muAesLabel = QLabel("mu_aes")
        muAesLabel.setToolTip("Aestivation mortality rate.")
        self.muAesSB = QDoubleSpinBox()
        self.muAesSB.setMinimum(0)
        self.muAesSB.setMaximum(1)
        self.muAesSB.setValue(0)
        self.muAesSB.setSingleStep(0.05)
        self.muAesSB.resize(self.muAesSB.sizeHint())
        self.muAesSB.valueChanged.connect(self.enableApply)
        tHide1Label = QLabel("t_hide1")
        tHide1Label.setToolTip("Start day of aestivation-hiding period (exclusive).")
        self.tHide1SB = QSpinBox()
        self.tHide1SB.setMinimum(0)
        self.tHide1SB.setMaximum(365)
        self.tHide1SB.setValue(0)
        self.tHide1SB.resize(self.tHide1SB.sizeHint())
        self.tHide1SB.valueChanged.connect(self.enableApply)
        tHide2Label = QLabel("t_hide2")
        tHide2Label.setToolTip("End day of aestivation-hiding period (inclusive)..")
        self.tHide2SB = QSpinBox()
        self.tHide2SB.setMinimum(0) # should be t_hide1
        self.tHide2SB.setMaximum(365)
        self.tHide2SB.setValue(0)
        self.tHide2SB.resize(self.tHide2SB.sizeHint())
        self.tHide2SB.valueChanged.connect(self.enableApply)
        tWake1Label = QLabel("t_wake1")
        tWake1Label.setToolTip("Start day of aestivation-waking period (exclusive).")
        self.tWake1SB = QSpinBox()
        self.tWake1SB.setMinimum(0)
        self.tWake1SB.setMaximum(365)
        self.tWake1SB.setValue(0)
        self.tWake1SB.resize(self.tWake1SB.sizeHint())
        self.tWake1SB.valueChanged.connect(self.enableApply)
        tWake2Label = QLabel("t_wake2")
        tWake2Label.setToolTip("End day of aestivation-waking period (inclusive).")
        self.tWake2SB = QSpinBox()
        self.tWake2SB.setMinimum(0) # should be t_wake1
        self.tWake2SB.setMaximum(365)
        self.tWake2SB.setValue(0)
        self.tWake2SB.resize(self.tWake2SB.sizeHint())
        self.tWake2SB.valueChanged.connect(self.enableApply)
        psiLabel.hide()
        self.psiSB.hide()
        muAesLabel.hide()
        self.muAesSB.hide()
        tHide1Label.hide()
        self.tHide1SB.hide()
        tHide2Label.hide()
        self.tHide2SB.hide()
        tWake1Label.hide()
        self.tWake1SB.hide()
        tWake2Label.hide()
        self.tWake2SB.hide()
        
        line4 = QFrame()
        line4.setFrameShape(QFrame.HLine)
        line4.setPalette(pal)
        
        seasonalityTitle = QLabel("Seasonality")
        alpha0MeanLabel = QLabel("alpha0_mean")
        alpha0MeanLabel.setToolTip("Mean of the baseline contribution to the carrying capacity.")
        self.alpha0MeanSB = QDoubleSpinBox()
        self.alpha0MeanSB.setMinimum(0.01) # should not include 0
        self.alpha0MeanSB.setMaximum(100000000)
        self.alpha0MeanSB.setValue(100000)
        self.alpha0MeanSB.setSingleStep(10000)
        self.alpha0MeanSB.resize(self.alpha0MeanSB.sizeHint())
        self.alpha0MeanSB.valueChanged.connect(self.enableApply)
        alpha0VarLabel = QLabel("alpha0_variance")
        alpha0VarLabel.setToolTip("Variance of the baseline contribution to the carrying capacity.")
        self.alpha0VarSB = QDoubleSpinBox()
        self.alpha0VarSB.setMinimum(0)
        self.alpha0VarSB.setMaximum(100000000)
        self.alpha0VarSB.setValue(0)
        self.alpha0VarSB.setSingleStep(1000)
        self.alpha0VarSB.resize(self.alpha0VarSB.sizeHint())
        self.alpha0VarSB.valueChanged.connect(self.enableApply)
        alpha1Label = QLabel("alpha1")
        alpha1Label.setToolTip("Rainfall contribution factor to carrying capacity.")
        self.alpha1SB = QDoubleSpinBox()
        self.alpha1SB.setMinimum(0)
        self.alpha1SB.setMaximum(100000000)
        self.alpha1SB.setValue(0)
        self.alpha1SB.setSingleStep(100)
        self.alpha1SB.resize(self.alpha1SB.sizeHint())
        self.alpha1SB.valueChanged.connect(self.enableApply)
        ampLabel = QLabel("amp")
        ampLabel.setToolTip("Amplitude of rainfall fluctuations.")
        self.ampSB = QDoubleSpinBox()
        self.ampSB.setMinimum(0)
        self.ampSB.setMaximum(1)
        self.ampSB.setValue(0)
        self.ampSB.setSingleStep(0.1)
        self.ampSB.resize(self.ampSB.sizeHint())
        self.ampSB.valueChanged.connect(self.enableApply)
        rainfallFileLabel = QLabel("rainfall file")
        rainfallFileLabel.setToolTip("Rainfall data file")
        self.rainfallFileCheckbox = QCheckBox()
        self.rainfallFileCheckbox.stateChanged.connect(lambda: self.checkboxState(self.rainfallFileCheckbox,
            showLabelElements=[rainfallFileDialogBtn, respLabel], 
            showNumElements=[self.respSB],
            showTextElements=[self.rainfallFilenameEdit],
            hideLabelElements=[ampLabel],
            hideNumElements=[self.ampSB])
        )
        self.rainfallFileCheckbox.stateChanged.connect(self.enableApply)
        
        self.rainfallFilenameEdit = QLineEdit("")
        self.rainfallFilenameEdit.setReadOnly(True)
        self.rainfallFilenameEdit.textChanged.connect(self.enableApply)
        rainfallFileDialogBtn = QPushButton("Select")
        rainfallFileDialogBtn.clicked.connect(lambda: self.openFileDialog(self.rainfallFile, self.rainfallFilenameEdit))
        respLabel = QLabel("resp")
        respLabel.setToolTip("Carrying capacity's responsiveness to rainfall contribution.")
        self.respSB = QDoubleSpinBox()
        self.respSB.setMinimum(0)
        self.respSB.setMaximum(10000)
        self.respSB.setValue(0)
        self.respSB.resize(self.respSB.sizeHint())
        self.respSB.valueChanged.connect(self.enableApply)
        self.rainfallFilenameEdit.hide()
        rainfallFileDialogBtn.hide()
        respLabel.hide()
        self.respSB.hide()
        
        line5 = QFrame()
        line5.setFrameShape(QFrame.HLine)
        line5.setPalette(pal)
        
        modelAreaTitle = QLabel("Model area")
        boundaryTypeLabel = QLabel("boundary type")
        self.boundaryTypeCB = QComboBox()
        self.boundaryTypeCB.addItems(["Toroid", "Edge"])
        self.boundaryTypeCB.currentTextChanged.connect(self.boundaryTypeState)
        self.boundaryTypeCB.currentTextChanged.connect(self.enableApply)
        self.coordsFileLabel = QLabel("patch coordinates file")
        self.coordsFileCheckbox = QCheckBox()
        self.coordsFileCheckbox.stateChanged.connect(lambda: self.checkboxState(self.coordsFileCheckbox,
            showLabelElements=[coordsFileDialogBtn],
            showTextElements=[self.coordsFilenameEdit]
            )
        )
        self.coordsFileCheckbox.stateChanged.connect(self.enableApply)
        self.coordsFileLabel.hide()
        self.coordsFileCheckbox.hide()
        self.coordsFilenameEdit = QLineEdit("")
        self.coordsFilenameEdit.setReadOnly(True)
        self.coordsFilenameEdit.textChanged.connect(self.enableApply)
        coordsFileDialogBtn = QPushButton("Select")
        coordsFileDialogBtn.clicked.connect(lambda: self.openFileDialog(self.coordsFile, self.coordsFilenameEdit))
        self.coordsFilenameEdit.hide()
        coordsFileDialogBtn.hide()
        
        line6 = QFrame()
        line6.setFrameShape(QFrame.HLine)
        line6.setPalette(pal)
        
        inherTitle = QLabel("Gene drive resistance")
        gammaLabel = QLabel("gamma")
        gammaLabel.setToolTip("Rate of r2 allele formation from W/D meiosis.")
        self.gammaSB = QDoubleSpinBox()
        self.gammaSB.setDecimals(3)
        self.gammaSB.setMinimum(0)
        self.gammaSB.setMaximum(1)
        self.gammaSB.setValue(0.025)
        self.gammaSB.setSingleStep(0.01)
        self.gammaSB.resize(self.gammaSB.sizeHint())
        self.gammaSB.valueChanged.connect(self.enableApply)
        
        line7 = QFrame()
        line7.setFrameShape(QFrame.HLine)
        line7.setPalette(pal)
        
        releaseTitle = QLabel("Gene drive release")
        relTimesFileLabel = QLabel("release times file")
        self.relTimesFileCheckbox = QCheckBox()
        self.relTimesFileCheckbox.stateChanged.connect(lambda: self.checkboxState(self.relTimesFileCheckbox,
            showLabelElements=[relTimesFileDialogBtn],
            showTextElements=[self.relTimesFilenameEdit]
            )
        )
        self.relTimesFileCheckbox.stateChanged.connect(self.enableApply)
        
        self.relTimesFilenameEdit = QLineEdit("")
        self.relTimesFilenameEdit.setReadOnly(True)
        self.relTimesFilenameEdit.textChanged.connect(self.enableApply)
        relTimesFileDialogBtn = QPushButton("Select")
        relTimesFileDialogBtn.clicked.connect(lambda: self.openFileDialog(self.relTimesFile, self.relTimesFilenameEdit))
        self.relTimesFilenameEdit.hide()
        relTimesFileDialogBtn.hide()
        
        line8 = QFrame()
        line8.setFrameShape(QFrame.HLine)
        line8.setPalette(pal)
        
        self.okBtn = QPushButton("Ok")
        self.okBtn.setToolTip("Accept changes and close dialog.")
        self.okBtn.setAutoDefault(True)
        self.okBtn.setDefault(True)
        self.okBtn.clicked.connect(lambda: self.applyChanges("ok"))
        self.applyBtn = QPushButton("Apply")
        self.applyBtn.setToolTip("Apply changes.")
        self.applyBtn.setEnabled(False)
        self.applyBtn.clicked.connect(lambda: self.applyChanges("apply"))
    
        self.layout.addWidget(recTitle, 0, 0)
        self.layout.addWidget(setLabelLabel, 1, 0)
        self.layout.addWidget(self.setLabelSB, 1, 1)
        self.layout.addWidget(recIntervalGlobalLabel, 1, 2)
        self.layout.addWidget(self.recIntervalGlobalSB, 1, 3)
        self.layout.addWidget(recStartLabel, 2, 0)
        self.layout.addWidget(self.recStartSB, 2, 1)
        self.layout.addWidget(recEndLabel, 2, 2)
        self.layout.addWidget(self.recEndSB, 2, 3)
        self.layout.addWidget(recIntervalLocalLabel, 2, 4)
        self.layout.addWidget(self.recIntervalLocalSB, 2, 5)
        self.layout.addWidget(recSitesFreqLabel, 2, 6)
        self.layout.addWidget(self.recSitesFreqSB, 2, 7)
        self.layout.addWidget(line1, 4, 0, 1, 8)
        self.layout.addWidget(lifeTitle, 5, 0)
        self.layout.addWidget(muJLabel, 6, 0)
        self.layout.addWidget(self.muJSB, 6, 1)
        self.layout.addWidget(muALabel, 6, 2)
        self.layout.addWidget(self.muASB, 6, 3)
        self.layout.addWidget(betaLabel, 6, 4)
        self.layout.addWidget(self.betaSB, 6, 5)
        self.layout.addWidget(thetaLabel, 6, 6)
        self.layout.addWidget(self.thetaSB, 6, 7)
        self.layout.addWidget(compPowerLabel, 7, 0)
        self.layout.addWidget(self.compPowerSB, 7, 1)
        self.layout.addWidget(minDevLabel, 7, 2)
        self.layout.addWidget(self.minDevSB, 7, 3)
        self.layout.addWidget(line2, 8, 0, 1, 8)
        self.layout.addWidget(dispTitle, 9, 0)
        self.layout.addWidget(dispRateLabel, 10, 0)
        self.layout.addWidget(self.dispRateSB, 10, 1)
        self.layout.addWidget(maxDispLabel, 10, 2)
        self.layout.addWidget(self.maxDispSB, 10, 3)
        self.layout.addWidget(dispTypeLabel, 11, 0)
        self.layout.addWidget(self.dispTypeCB, 11, 1, 1, 2)
        self.layout.addWidget(line3, 12, 0, 1, 8)
        self.layout.addWidget(aesTitle, 13, 0)
        self.layout.addWidget(self.aesCheckbox, 13, 1)
        self.layout.addWidget(psiLabel, 14, 0)
        self.layout.addWidget(self.psiSB, 14, 1)
        self.layout.addWidget(muAesLabel, 14, 2)
        self.layout.addWidget(self.muAesSB, 14, 3)
        self.layout.addWidget(tHide1Label, 15, 0)
        self.layout.addWidget(self.tHide1SB, 15, 1)
        self.layout.addWidget(tHide2Label, 15, 2)
        self.layout.addWidget(self.tHide2SB, 15, 3)
        self.layout.addWidget(tWake1Label, 15, 4)
        self.layout.addWidget(self.tWake1SB, 15, 5)
        self.layout.addWidget(tWake2Label, 15, 6)
        self.layout.addWidget(self.tWake2SB, 15, 7)
        self.layout.addWidget(line4, 16, 0, 1, 8)
        self.layout.addWidget(seasonalityTitle, 17, 0)
        self.layout.addWidget(alpha0MeanLabel, 18, 0)
        self.layout.addWidget(self.alpha0MeanSB, 18, 1)
        self.layout.addWidget(alpha0VarLabel, 18, 2)
        self.layout.addWidget(self.alpha0VarSB, 18, 3)
        self.layout.addWidget(alpha1Label, 18, 4)
        self.layout.addWidget(self.alpha1SB, 18, 5)
        self.layout.addWidget(ampLabel, 18, 6)
        self.layout.addWidget(self.ampSB, 18, 7)
        self.layout.addWidget(rainfallFileLabel, 19, 0)
        self.layout.addWidget(self.rainfallFileCheckbox, 19, 1)
        self.layout.addWidget(self.rainfallFilenameEdit, 20, 0, 1, 5)
        self.layout.addWidget(rainfallFileDialogBtn, 20, 5)
        self.layout.addWidget(respLabel, 21, 0)
        self.layout.addWidget(self.respSB, 21, 1)
        self.layout.addWidget(line5, 22, 0, 1, 8)
        self.layout.addWidget(modelAreaTitle, 23, 0)
        self.layout.addWidget(boundaryTypeLabel, 24, 0)
        self.layout.addWidget(self.boundaryTypeCB, 24, 1, 1, 2)
        self.layout.addWidget(self.coordsFileLabel, 25, 0)
        self.layout.addWidget(self.coordsFileCheckbox, 25, 1)
        self.layout.addWidget(self.coordsFilenameEdit, 26, 0, 1, 5)
        self.layout.addWidget(coordsFileDialogBtn, 26, 5)
        self.layout.addWidget(line6, 27, 0, 1, 8)
        self.layout.addWidget(inherTitle, 28, 0)
        self.layout.addWidget(gammaLabel, 29, 0)
        self.layout.addWidget(self.gammaSB, 29, 1)
        self.layout.addWidget(line7, 30, 0, 1, 8)
        self.layout.addWidget(releaseTitle, 31, 0)
        self.layout.addWidget(relTimesFileLabel, 32, 0)
        self.layout.addWidget(self.relTimesFileCheckbox, 32, 1)
        self.layout.addWidget(self.relTimesFilenameEdit, 33, 0, 1, 5)
        self.layout.addWidget(relTimesFileDialogBtn, 33, 5)
        self.layout.addWidget(line8, 34, 0, 1, 8)
        self.layout.addWidget(self.okBtn, 35, 6, 1, 1)
        self.layout.addWidget(self.applyBtn, 35, 7, 1, 1)
        
        self.horizontalGroupBox.setLayout(self.layout)
        
    def boundaryTypeState(self):
        self.coordsFileCheckbox.setChecked(False)
        if self.boundaryTypeCB.currentText() == "Toroid":
            self.coordsFileLabel.hide()
            self.coordsFileCheckbox.hide()
            
        if self.boundaryTypeCB.currentText() == "Edge":
            self.coordsFileLabel.show()
            self.coordsFileCheckbox.show()
        
    def checkboxState(self, checkBox, showLabelElements, showNumElements=[], showTextElements=[], hideLabelElements=[], hideNumElements=[]):
        if checkBox.isChecked():
            for l in showLabelElements:
                l.show()
            for l in showNumElements:
                l.show()
            for l in showTextElements:
                l.show()
            for l in hideLabelElements:
                l.hide()
            for l in hideNumElements:
                l.hide()
                l.setValue(0)
            
        else:
            for l in showLabelElements:
                l.hide()
            for l in showNumElements:
                l.hide()
                l.setValue(0)
            for l in showTextElements:
                l.hide()
                l.clear()
            for l in hideLabelElements:
                l.show()
            for l in hideNumElements:
                l.show()
        
    def openFileDialog(self, filename, filenameEdit):
        """ Opens a file dialog box to select a file, saves the filename and updates the Edit box text with the filename. """
        fname, ok = QFileDialog.getOpenFileName(self, "Select a file", ".", "Text files (*.txt)")
        if fname:
            filename = Path(fname)
            filenameEdit.setText(str(filename))
            
    def validParams(self):
        errs = 0 
        errMsgs = []
        maxT = self.parentWindow.getMaxT()
        numPat = self.parentWindow.getNumPat()
        if self.recEndSB.value() < self.recStartSB.value():
            errs += 1
            errMsgs.append("rec_end must be equal to or larger than rec_start.")
        if self.aesCheckbox.isChecked():
            if self.tHide2SB.value() < self.tHide1SB.value():
                errs += 1
                errMsgs.append("t_hide2 must be equal to or larger than t_hide1.")
            if self.tWake2SB.value() < self.tWake1SB.value():
                errs += 1
                errMsgs.append("t_wake2 must be equal to or larger than t_wake1.")
        
        # read files and check values        
        if self.rainfallFileCheckbox.isChecked():
            if self.rainfallFilenameEdit.text() == "":
                errs += 1
                errMsgs.append("No rainfall file selected.")
            else:
                try:
                    rfData = np.loadtxt(self.rainfallFilenameEdit.text(), dtype=np.float64)
                    if len(rfData) == 365 or len(rfData) == maxT:
                        for i in range(0, len(rfData)):
                            dp = rfData[i]
                            if dp < 0:
                                errs += 1
                                errMsgs.append("Rainfall value r for day {} is out of bounds r ≥ 0.".format(i+1))
                    else:
                        errs += 1
                        errMsgs.append("The number of daily rainfall values in the file is not 365 or max_t.")
                except Exception as e:
                    errs += 1
                    errMsgs.append("An error occured with the rainfall file: {}".format(e))
                
        if self.coordsFileCheckbox.isChecked():
            if self.coordsFilenameEdit.text() == "":
                errs += 1
                errMsgs.append("No patch coordinates file selected.")
            else:
                # use this method to check the different data types 
                with open(self.coordsFilenameEdit.text(), 'r') as file: 
                    lines = file.readlines()
                    if len(lines) != numPat:
                        errs += 1
                        errMsgs.append("The number of patch coordinates in the file does not match num_pat.")
                    else:
                        for i in range(0, len(lines)):
                            line = lines[i].strip() # strip surrounding whitespace
                            x, y, isRelSite = line.split() # split into column values
                            try:
                                x = float(x)
                            except Exception as e:
                                errs += 1
                                errMsgs.append("An error occured for patch coordinate x{}: {}".format(i+1, e))
                            try:
                                y = float(y)
                            except Exception as e:
                                errs += 1
                                errMsgs.append("An error occured for patch coordinate y{}: {}".format(i+1, e))
                            if re.match(r"^y|n$", isRelSite) == None:
                                errs += 1
                                errMsgs.append("Patch coordinate {} has an invalid release site choice.".format(i+1))   
        
        if self.relTimesFileCheckbox.isChecked():
            if self.relTimesFilenameEdit.text() == "":
                errs += 1
                errMsgs.append("No release times file selected.")
            else:
                # use this method to check for floats (cannot convert floats to ints)
                with open(self.relTimesFilenameEdit.text(), 'r') as file: 
                    lines = file.readlines()
                    for i in range(0, len(lines)):
                        dp = lines[i].strip()
                        if re.match(r"^[-+]?[0-9]+$", dp):
                            dp = int(dp)
                            if dp < 0 or dp > maxT:
                                errs += 1
                                errMsgs.append("Release time t{} is out of bounds 0 ≤ t ≤ max_t.".format(i+1))
                        else:
                            errMsgs.append("Release time t{} is not an integer.".format(i+1))
                
        # give warnings but still allow the values - no errors thrown
        if self.aesCheckbox.isChecked():
            if (self.t_hide1SB.value() > maxT) or (self.t_hide2SB.value() > maxT) or (self.tWake1SB.value() > maxT) or (self.tWake2SB.value() > maxT):
                errMsgs.append("The aestivation interval times are larger than max_t.\nThe simulation will only run partly through the aestivation period.")
        if self.recStartSB.value() > maxT:
            errMsgs.append("rec_start > max_t. This simulation will not include local recording.")
        if (maxT - self.recIntervalLocalSB.value() - self.recStartSB.value()) < 0:
            errMsgs.append("The interval between rec_start and max_t is larger than rec_interval_local.\nThe simulation will only record local data for day 0.")
            
        isValid = True
        if errs != 0:
            isValid = False
        return (isValid, errMsgs)   
        
    def enableApply(self):
        if self.applyBtn.isEnabled() == False:
            self.applyBtn.setEnabled(True)
        
    def applyChanges(self, btn):
        # only apply changes if pass bound and other checks  
        isValid, errMsgs = self.validParams()
        if isValid:
            if errMsgs:
                errMsgs = "\n".join(errMsgs)
                QMessageBox.information(self, "Info", errMsgs)
            self.saveValues()
            self.applyBtn.setEnabled(False)
            if btn == "ok": # close dialog too if using ok button
                self.accept()
        else:
            errMsgs = "\n".join(errMsgs)
            QMessageBox.warning(self, "Invalid parameter(s)", errMsgs)
            
class AdvParams():
    setLabel = 1
    recIntervalGlobal = 1
    recStart = 0
    recEnd = 1000
    recIntervalLocal = 200
    recSitesFreq = 1
    muJ = 0.05
    muA = 0.125
    beta = 100
    theta = 9
    compPower = 0.066666667
    minDev = 10
    dispRate = 0.01
    maxDisp = 0.2
    dispType = "Radial"
    aestivation = False
    psi = 0
    muAes = 0
    tHide1 = 0
    tHide2 = 0
    tWake1 = 0
    tWake2 = 0
    alpha0Mean = 100000
    alpha0Var = 0 
    alpha1 = 0
    amp = 0
    rainfallFile = False
    rainfallFilename = ""
    resp = 0
    boundaryType = "Toroid"
    patchCoordsFile = False
    patchCoordsFilename = ""
    gamma = 0.025
    relTimesFile = False
    relTimesFilename = ""
  
class WidgetRun(QWidget):
    """ Creates a widget to run the simulation. """
    
    def __init__(self, winWidget):
        super().__init__()
        self.winWidget = winWidget 
        self.simulation = None
        self.setLayout(QGridLayout())
        self.initUI()
        
    def initUI(self):
        outputDirLabel = QLabel("Output directory")
        outputDirLabel.setToolTip("Output files directory")
        self.outputDirNameEdit = QLineEdit("")
        self.outputDirNameEdit.setReadOnly(True)
        outputDirDialogBtn = QPushButton("Select")
        outputDirDialogBtn.clicked.connect(lambda: self.openDirDialog(self.outputDirNameEdit))
        simNameLabel = QLabel("Simulation name (optional)")
        simNameLabel.setToolTip("Subdirectory name for simulation run")
        self.simNameEdit = QLineEdit("")
        
        self.progBar = QProgressBar()
        self.progBar.setMinimumHeight(40)
        self.progBar.setValue(0)
        self.progBar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.runBtn = QPushButton("Run")
        self.runBtn.setMinimumHeight(40)
        self.runBtn.setToolTip("Run simulation")
        self.runBtn.clicked.connect(self.runSim)
        pixmapi = QStyle.SP_MessageBoxCritical
        icon = self.style().standardIcon(pixmapi)
        self.abortBtn = QPushButton(icon, "")
        self.abortBtn.setMinimumHeight(40)
        self.abortBtn.setToolTip("Abort simulation process.")
        self.abortBtn.clicked.connect(self.abortSim)
        self.abortBtn.setEnabled(False)
        self.abortBtn.hide()
        msgBar = QLineEdit()
        msgBar.setText("Waiting for run.")
        msgBar.setReadOnly(True)
        msgBar.resize(msgBar.sizeHint())
        
        self.layout().setHorizontalSpacing(5)
        self.layout().addWidget(outputDirLabel, 0, 0)
        self.layout().addWidget(simNameLabel, 0, 5)
        self.layout().addWidget(self.outputDirNameEdit, 1, 0, 1, 4)
        self.layout().addWidget(outputDirDialogBtn, 1, 4)
        self.layout().addWidget(self.simNameEdit, 1, 5, 1, 3)
        self.layout().addWidget(self.progBar, 2, 0, 1, 6)
        self.layout().addWidget(self.runBtn, 2, 6, 1, 2)
        self.layout().addWidget(self.abortBtn, 2, 6, 1, 2)
        self.layout().addWidget(msgBar, 3, 0, 1, 8)
        
        
    def openDirDialog(self, dirNameEdit):
        """ Opens a directory dialog box to select the output directory. """
        dname = QFileDialog.getExistingDirectory(self, "Select an output directory", ".")
        if dname:
            outputDirName = Path(dname)
            dirNameEdit.setText(str(outputDirName))    
            
    def runSim(self):
        validDir = self.createOutputDir(self.outputDirNameEdit.text(), self.simNameEdit.text())
        if validDir:
            self.progBar.setValue(0)
            self.winWidget.runStarted()
            customSet = self.winWidget.createParamsFile(self.outputPath)
            
            # Create simulation run thread
            self.thread = QThread()
            self.simulation = Simulation(self.outputPath,
                                         self.simName,
                                         customSet.dispType, 
                                         customSet.boundaryType,
                                         customSet.rainfallFile,
                                         customSet.coordsFile,
                                         customSet.relTimesFile
                                         )
            self.simulation.moveToThread(self.thread)
            
            # Connect signals and slots
            self.thread.started.connect(self.simulation.run)
            self.simulation.finished.connect(self.thread.quit)
            self.simulation.finished.connect(self.simulation.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.simulation.error.connect(self.runError)
    
            self.abortCode = 0
            self.thread.start()
            
            # Disable and hide run button while subprocess is running and enable abort button in its place
            self.runBtn.setEnabled(False)
            self.runBtn.hide()
            self.abortBtn.setEnabled(True)
            self.abortBtn.show()
            self.thread.finished.connect(lambda: self.runFinished(self.abortCode))
    
            # Start the QTimer to read the output file periodically
            # self.timer = QTimer(self)
            # self.timer.timeout.connect(self.read_output_file)
            # self.timer.start(1000)  # Check for new output every 1 second
        
    def abortSim(self):
       if self.simulation:
           self.abortCode = 1
           self.simulation.abort()
           self.thread.quit()
           self.thread.wait()
           print("Aborting sim")
        
    def createOutputDir(self, dirPath, simName):
        isValidDir = False
        if Path(dirPath).is_dir() or dirPath == "":
            if dirPath == "":
                dirPath = basedir
            
            if simName != "":
                self.outputPath = dirPath / simName
            else:
                dt = datetime.now()
                simName = str(dt.year) + "_" + str(dt.month) + "_" + str(dt.day)
                simName +=  "_" + str(dt.hour) + str(dt.minute) + str(dt.second)
                self.outputPath = Path(dirPath) / simName
            
            if not self.outputPath.exists():
                os.makedirs(self.outputPath)
                
            self.simName = simName
            isValidDir = True
            
        else:
            QMessageBox.critical(self, "Error", "The output directory path does not exist.")
            isValidDir = False
        return isValidDir
        
    def runFinished(self, abortCode):
        # Re-enable the button
        #self.timer.stop()
        self.abortBtn.setEnabled(False)
        self.abortBtn.hide()
        self.runBtn.show()
        self.runBtn.setEnabled(True)
        if abortCode == 0:
            self.progBar.setValue(100)
            self.winWidget.runFinished(self.outputPath)
            QMessageBox.information(self, "Info", "Simulation completed successfully!")
        else:
            self.progBar.setValue(0)
            self.winWidget.runFinished(self.outputPath)
            QMessageBox.information(self, "Info", "Simulation aborted.")
        self.simulation = None
        
    def runError(self, errorMsg):
        # Stop the timer and show the error
        #self.timer.stop()
        QMessageBox.critical(self, "Error", errorMsg)
        self.abortSim()
        
    def isSimRunning(self):
        if self.simulation != None:
            return True
        else:
            return False
       
class Simulation(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    def __init__(self, outputPath, simName, dispType, boundaryType, rainfallFile, coordsFile, relTimesFile):
        super().__init__()
        
        self.exeFilepath = basedir / "gdsimsapp.exe"
        self.outputPath = outputPath
        self.simName = simName
        
        self.rainfallFile = rainfallFile
        self.coordsFile = coordsFile
        self.relTimesFile = relTimesFile
        self.dispType = dispType
        self.boundaryType = boundaryType
        
        self.process = None
    
    def run(self):
        os.chdir(self.outputPath) # directory for output files
        paramFile = self.outputPath / "params.txt"
        inputString = "100" + "\n" + str(paramFile.resolve()) + "\n" + "y" +"\n" + "y" + "\n"
        
        if self.boundaryType == "Toroid":
            inputString += "1" + "\n" + "t" + "\n"
        elif self.boundaryType == "Edge":
            inputString += "1" + "\n" + "e" + "\n"
        if self.dispType == "Distance kernel":
            inputString += "2" + "\n" + "d" + "\n" 
        elif self.dispType == "Radial":
            inputString += "2" + "\n" + "r" + "\n" 
        if self.rainfallFile != None:
            inputString += "3" + "\n" + self.rainfallFile + "\n"
        if self.coordsFile != None:
            inputString += "4" + "\n" + self.coordsFile + "\n"
        if self.relTimesFile != None:
            inputString += "5" + "\n" + self.relTimesFile + "\n"
        
        inputString += "0" + "\n"
       
        # Run C++ model with input data
        os.chdir(self.outputPath) # directory for output files
        env = os.environ.copy()
        env["PATH"] = r"C:\msys64\mingw64\bin;" + env["PATH"]
        self.process = subprocess.Popen([self.exeFilepath], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
        outs, errs = self.process.communicate(input=inputString)
        # check for errors whilst process is running and emit error signal
        # (can't use except because cerrs, not subprocess errs)
        if errs: 
            self.error.emit(errs)
            self.process.terminate()
        else: # don't let finished signal emit if have errors
            self.process.wait()
            self.finished.emit()
            
    def abort(self):
        if self.process:
            self.process.terminate()
        
class WidgetPlot(QWidget): # widget containing plotcanvas and toolbar in same place
    """Creates a widget for the plotspace and plot interaction components."""
    
    def __init__(self):
        QWidget.__init__(self)
        self.initUI()
    
    def initUI(self):
        layout = QGridLayout()
        
        self.canvas = PlotCanvas()
        self.toolbar = NavBar(self.canvas)
        self.runsCB = QComboBox()
        self.plotBtn = QPushButton("Plot")
        self.plotBtn.setMinimumHeight(40)
        self.plotBtn.setEnabled(False)
        self.plotBtn.clicked.connect(self.plotClick)
        
        interactBox = QGroupBox()
        interactLayout = QVBoxLayout()
        
        self.mWWcheckbox = QCheckBox("WW")
        self.mWWcheckbox.setToolTip("Wild homozygous males.")
        self.mWWcheckbox.resize(self.mWWcheckbox.sizeHint())
        self.mWWcheckbox.setChecked(True) 
        
        self.mWDcheckbox = QCheckBox("WD")
        self.mWDcheckbox.setToolTip("Drive heterozygous males.")
        self.mWDcheckbox.resize(self.mWDcheckbox.sizeHint()) 
        self.mWDcheckbox.setChecked(True) 
        
        self.mDDcheckbox = QCheckBox("DD")
        self.mDDcheckbox.setToolTip("Drive homozygous males.")
        self.mDDcheckbox.resize(self.mDDcheckbox.sizeHint()) 
        self.mDDcheckbox.setChecked(True) 
        
        self.mWRcheckbox = QCheckBox("WR")
        self.mWRcheckbox.setToolTip("Wild/drive resistant heterozygous males.")
        self.mWRcheckbox.resize(self.mWRcheckbox.sizeHint())
        self.mWRcheckbox.setChecked(True) 
        
        self.mRRcheckbox = QCheckBox("RR")
        self.mRRcheckbox.setToolTip("Drive resistant homozygous males.")
        self.mRRcheckbox.resize(self.mRRcheckbox.sizeHint())
        self.mRRcheckbox.setChecked(True) 
        
        self.mDRcheckbox = QCheckBox("DR")
        self.mDRcheckbox.setToolTip("Drive/drive resistant heterozygous males.")
        self.mDRcheckbox.resize(self.mDRcheckbox.sizeHint())
        self.mDRcheckbox.setChecked(True) 
        
        interactLayout.addWidget(self.runsCB)
        interactLayout.addWidget(self.mWWcheckbox)
        interactLayout.addWidget(self.mWDcheckbox)
        interactLayout.addWidget(self.mDDcheckbox)
        interactLayout.addWidget(self.mWRcheckbox)
        interactLayout.addWidget(self.mRRcheckbox)
        interactLayout.addWidget(self.mDRcheckbox)
        interactLayout.addWidget(self.plotBtn)
        interactLayout.addStretch() # create a stretch of filler space between components
        interactBox.setLayout(interactLayout)
        
        layout.addWidget(self.toolbar, 0, 0, 1, 5) # toolbar goes before so is placed above canvas
        layout.addWidget(self.canvas, 1, 0, 1, 5)
        layout.addWidget(interactBox, 1, 5, 1, 2)
        
        self.setLayout(layout)
        
    def checkboxState(self):
        """Returns a list of indices to be plotted depending on the checkboxes that are checked."""
        lines=[]
        if self.mWWcheckbox.isChecked() == True:
            lines.append(0)
        if self.mWDcheckbox.isChecked() == True:
            lines.append(1)
        if self.mDDcheckbox.isChecked() == True:
            lines.append(2)
        if self.mWRcheckbox.isChecked() == True:
            lines.append(3)
        if self.mRRcheckbox.isChecked() == True:
            lines.append(4)
        if self.mDRcheckbox.isChecked() == True:
            lines.append(5)
        return lines
    
    def plotClick(self):
        """Plots the function with the new selected parameters on the plot canvas."""
        runNum = re.search(r"\d+", self.runsCB.currentText())[0]
        rgx = r"Totals\d+run" + runNum
        plotFile = [f for f in self.totalsFiles if re.match(rgx, os.path.basename(f))][0]
        self.canvas.plot(plotFile, self.checkboxState())
        
    def runStarted(self):
        self.plotBtn.setEnabled(False)
        
    def runFinished(self, outputDir):
        self.plotBtn.setEnabled(True)
        self.findPlotFiles(outputDir)
        self.updateRuns()
        
    def findPlotFiles(self, outputDir):
        if os.path.exists(os.path.join(outputDir, "output_files")):
            allFiles = [f for f in os.listdir(outputDir / "output_files") 
                        if os.path.isfile(os.path.join(outputDir, "output_files", f))]
            self.coordFiles = [os.path.join(outputDir, "output_files", f) for f in allFiles if re.match("CoordinateList", os.path.basename(f))]
            self.localDataFiles = [os.path.join(outputDir, "output_files", f) for f in allFiles if re.match("LocalData", os.path.basename(f))]
            self.totalsFiles = [os.path.join(outputDir, "output_files", f) for f in allFiles if re.match("Totals", os.path.basename(f))]
    
    def updateRuns(self):
        runs = []
        for f in self.totalsFiles:
            m = re.search(r"run(\d+)", f)
            runs.append("Run "+ m.group(1))
            
        self.runsCB.clear()
        self.runsCB.addItems(runs)

class PlotCanvas(FigureCanvas):
    """Plots the function with the y and n parameters specified, where y and n are lists."""
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # tight layout makes sure the labels are not cut off in the canvas when they become bigger in replots
        fig = Figure(figsize=(width, height), dpi=dpi, layout='tight')
        self.axes = fig.add_subplot(111) # creates subplots

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self) # allows figure to change size with window
         
    def plot(self, file, lines:list): # sets variables of function (have to be lists)
        self.axes.clear() # clears plot on the plot canvas before plotting the new curve(s)

        totals = np.loadtxt(file, skiprows=2)
        times = totals[:, 0]
        total_males = totals[:, 1:]
        for line in lines:  # keep same colours for same type of line
            lbl = ""
            col = "mediumturquoise"
            if line == 0:
                lbl = "$M_{WW}$"
                col = "mediumturquoise"
            elif line == 1:
                lbl = "$M_{WD}$"
                col = "darkcyan"
            elif line == 2:
                lbl = "$M_{DD}$"
                col = "royalblue"
            elif line == 3:
                lbl = "$M_{WR}$"
                col = "slategray"
            elif line == 4:
                lbl = "$M_{RR}$"
                col = "black"
            elif line == 5:
                lbl = "$M_{DR}$"
                col = "darkviolet"
                
            self.axes.plot(times, total_males[:, line], label=lbl, color=col) 
     
        self.axes.set_xlabel("Day")
        self.axes.set_ylabel("Total number of individuals")
        self.axes.legend() # creates a legend for each curve
        self.draw() # draws the curve(s) on the canvas
        
if __name__ == "__main__":
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv) # creates an application object
    win = MainWindow() # uses class where the main application window is
    win.show()
    sys.exit(app.exec())
    
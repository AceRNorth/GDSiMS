# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 14:03:49 2025

@author: biol0117
"""

from PyQt5.QtWidgets import QWidget, QComboBox, QPushButton, QCheckBox, QGridLayout, QVBoxLayout, QGroupBox, QFrame, QSlider, QLabel, QStyle, QSpinBox
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QColor, QPalette
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavBar
import os
import re
import numpy as np
import plotcanvas

class WidgetPlot(QWidget): # widget containing plotcanvas and toolbar in same place
    """Creates a widget for the plotspace and plot interaction components."""
    
    def __init__(self, canvas):
        QWidget.__init__(self)
        self.canvas = canvas
        self.baseInitUI()
    
    def baseInitUI(self):
        self.toolbar = NavBar(self.canvas)
        self.runsCB = QComboBox()
        self.plotBtn = QPushButton("Plot")
        self.plotBtn.setMinimumHeight(40)
        self.plotBtn.setEnabled(False)
        self.plotBtn.clicked.connect(self.plotClick)
        
    def createGridLayout(self):
        """ """
    
    def plotClick(self):
        """Plots the function with the new selected parameters on the plot canvas."""
        
    def runStarted(self):
        self.plotBtn.setEnabled(False)
        
    def runFinished(self, outputDir):
        self.plotBtn.setEnabled(True)
        self.findPlotFiles(outputDir)
        self.updateBtns(outputDir)
        
    def findPlotFiles(self, outputDir):
        self.dataFiles = []
    
    def updateBtns(self, outputDir):
        """ Updates UI buttons in the interaction box for runs just made."""
        self.updateRuns()
    
    def updateRuns(self):
        runs = []
        for f in self.dataFiles:
            m = re.search(r"run(\d+)", f)
            runs.append("Run "+ m.group(1))
        self.runsCB.clear()
        self.runsCB.addItems(runs)

class WidgetPlotTotals(WidgetPlot):
    """Creates a widget for the plotspace and plot interaction components."""
    
    def __init__(self):
        self.canvas = plotcanvas.TotalsPlotCanvas()
        super().__init__(self.canvas)
        self.totalsInitUI()
        self.createGridLayout()
    
    def totalsInitUI(self):
        """ """
        self.allCheckbox = QCheckBox("All\ngenotypes")
        self.allCheckbox.setToolTip("WW + WD + DD + WR + RR + DR")
        self.allCheckbox.resize(self.allCheckbox.sizeHint())
        self.allCheckbox.setChecked(True)
        
        self.transmitCheckbox = QCheckBox("Capable of\nmalaria\ntransmission")
        self.transmitCheckbox.setToolTip("WW + WD + WR")
        self.transmitCheckbox.resize(self.transmitCheckbox.sizeHint())
        self.transmitCheckbox.setChecked(True)
        
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
        
    def createGridLayout(self):
        layout = QGridLayout()
        interactBox = QGroupBox()
        interactLayout = QVBoxLayout()
        
        interactLayout.addWidget(self.runsCB)
        interactLayout.addWidget(self.allCheckbox)
        interactLayout.addWidget(self.transmitCheckbox)
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
        layout.addWidget(interactBox, 1, 5, 1, 1)
        
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
        if self.allCheckbox.isChecked() == True:
            lines.append(6)
        if self.transmitCheckbox.isChecked() == True:
            lines.append(7)
        return lines
    
    def plotClick(self):
        """Plots the function with the new selected parameters on the plot canvas."""
        runNum = re.search(r"\d+", self.runsCB.currentText())[0]
        rgx = r"Totals\d+run" + runNum
        plotFile = [f for f in self.dataFiles if re.match(rgx, os.path.basename(f))][0]
        self.canvas.plot(plotFile, self.checkboxState())

    def findPlotFiles(self, outputDir):
        if os.path.exists(os.path.join(outputDir, "output_files")):
            allFiles = [f for f in os.listdir(outputDir / "output_files") 
                        if os.path.isfile(os.path.join(outputDir, "output_files", f))]
            self.dataFiles = [os.path.join(outputDir, "output_files", f) for f in allFiles if re.match("Totals", os.path.basename(f))]

class WidgetPlotCoords(WidgetPlot):
    """Creates a widget for the plotspace and plot interaction components."""
    def __init__(self):
        self.canvas = plotcanvas.CoordsPlotCanvas()
        super().__init__(self.canvas)
        self.createGridLayout()
        
    def createGridLayout(self):
        layout = QGridLayout()
        interactBox = QGroupBox()
        interactLayout = QVBoxLayout()
        
        interactLayout.addWidget(self.runsCB)
        interactLayout.addWidget(self.plotBtn)
        interactLayout.addStretch() # create a stretch of filler space between components
        interactBox.setLayout(interactLayout)
        
        layout.addWidget(self.toolbar, 0, 0, 1, 5) # toolbar goes before so is placed above canvas
        layout.addWidget(self.canvas, 1, 0, 1, 5)
        layout.addWidget(interactBox, 1, 5, 1, 2)
        
        self.setLayout(layout)    
        
    def plotClick(self):
        """Plots the function with the new selected parameters on the plot canvas."""
        runNum = re.search(r"\d+", self.runsCB.currentText())[0]
        rgx = r"CoordinateList\d+run" + runNum
        plotFile = [f for f in self.dataFiles if re.match(rgx, os.path.basename(f))][0]
        self.canvas.plot(plotFile)

    def findPlotFiles(self, outputDir):
        if os.path.exists(os.path.join(outputDir, "output_files")):
            allFiles = [f for f in os.listdir(outputDir / "output_files") 
                        if os.path.isfile(os.path.join(outputDir, "output_files", f))]
            self.dataFiles = [os.path.join(outputDir, "output_files", f) for f in allFiles if re.match("CoordinateList", os.path.basename(f))]

class WidgetPlotLocal(WidgetPlot):
    def __init__(self):
        self.canvas = plotcanvas.LocalPlotCanvas()
        super().__init__(self.canvas)
        self.createGridLayout()
        self.recStart = 0
        self.recEnd = 1
        self.recIntervalLocal = 1
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateAnim)
        
    def createGridLayout(self):
        layout = QGridLayout()
        interactBox = QGroupBox()
        interactLayout = QVBoxLayout()
        
        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        pal = line1.palette()
        pal.setColor(QPalette.WindowText, QColor("lightGray"))
        line1.setPalette(pal)
        
        self.plotSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.plotSlider.setMinimum(0)
        self.plotSlider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.plotSlider.setValue(0)
        self.sliderLabel = QLabel("day")
        self.sliderLabel.setToolTip("Simulation day")
        self.plotSlider.valueChanged.connect(self.updateSliderText)
        
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setPalette(pal)
        
        pixmapi = QStyle.SP_MediaPlay
        icon = self.style().standardIcon(pixmapi)
        self.playBtn = QPushButton(icon, "")
        self.playBtn.setFixedSize(65, 65)
        self.playBtn.setIconSize(QSize(50, 50))
        self.playBtn.clicked.connect(self.startAnim)
        self.playBtn.setEnabled(False)
        intervalLabel = QLabel("Interval (ms)")
        intervalLabel.setToolTip("Animation frame interval (milliseconds)")
        self.intervalSB = QSpinBox()
        self.intervalSB.setMinimum(1)
        self.intervalSB.setMaximum(10000)
        self.intervalSB.setValue(200)
        self.intervalSB.resize(self.intervalSB.sizeHint())
    
        interactLayout.addWidget(self.runsCB)
        interactLayout.addWidget(line1)
        interactLayout.addWidget(self.plotSlider)
        interactLayout.addWidget(self.sliderLabel)
        interactLayout.addWidget(self.plotBtn)
        interactLayout.addWidget(line2)
        interactLayout.addWidget(intervalLabel)
        interactLayout.addWidget(self.intervalSB)
        interactLayout.addWidget(self.playBtn)
        interactLayout.addStretch() # create a stretch of filler space between components
        interactLayout.setAlignment(self.sliderLabel, Qt.AlignmentFlag.AlignHCenter)
        interactLayout.setAlignment(self.playBtn, Qt.AlignmentFlag.AlignHCenter)
        interactBox.setLayout(interactLayout)
        
        layout.addWidget(self.toolbar, 0, 0, 1, 5) # toolbar goes before so is placed above canvas
        layout.addWidget(self.canvas, 1, 0, 1, 5)
        layout.addWidget(interactBox, 1, 5, 1, 2)
        
        self.setLayout(layout)    
        
    def runStarted(self):
         self.plotBtn.setEnabled(False)
         self.playBtn.setEnabled(False)
         
    def runFinished(self, outputDir):
        self.plotBtn.setEnabled(True)
        self.playBtn.setEnabled(True)
        self.findPlotFiles(outputDir)
        self.updateBtns(outputDir)
        
    def updateSliderText(self, value):
        """ Updates the slider text value, by scaling back the slider value to the original value."""
        origVal = (value * self.recIntervalLocal) + self.recStart
        self.sliderLabel.setText(f"day {origVal}")
        
    def plotClick(self):
        """Plots the function with the new selected parameters on the plot canvas."""
        coordsFile, localFile = self.findCurRunFiles()
        self.canvas.setMode('static')
        self.canvas.plot(coordsFile, localFile, self.plotSlider.value())
    
    def findCurRunFiles(self):
        """ Find data files for the current run selected. """
        runNum = re.search(r"\d+", self.runsCB.currentText())[0]
        coordsRgx = r"CoordinateList\d+run" + runNum
        coordsFile = [f for f in self.coordsDataFiles if re.match(coordsRgx, os.path.basename(f))][0]
        localRgx = r"LocalData\d+run" + runNum
        localFile = [f for f in self.localDataFiles if re.match(localRgx, os.path.basename(f))][0]
        return coordsFile, localFile
        
    def findPlotFiles(self, outputDir):
        if os.path.exists(os.path.join(outputDir, "output_files")):
            allFiles = [f for f in os.listdir(outputDir / "output_files") 
                        if os.path.isfile(os.path.join(outputDir, "output_files", f))]
            self.coordsDataFiles = [os.path.join(outputDir, "output_files", f) for f in allFiles if re.match("CoordinateList", os.path.basename(f))]
            self.localDataFiles = [os.path.join(outputDir, "output_files", f) for f in allFiles if re.match("LocalData", os.path.basename(f))]
    
    def updateBtns(self, outputDir):
        self.updateRuns()
        self.updateSlider(outputDir)

    def updateRuns(self):
        runs = []
        for f in self.coordsDataFiles:
            m = re.search(r"run(\d+)", f)
            runs.append("Run "+ m.group(1))
        self.runsCB.clear()
        self.runsCB.addItems(runs)
        
    def startAnim(self):
        """ """
        self.curCoordsFile, self.curLocalFile = self.findCurRunFiles()
        self.numFrames = int((self.recEnd - self.recStart) / self.recIntervalLocal)
        self.frame = 0
        self.interval = self.intervalSB.value()
        self.canvas.setMode('animation')
        self.timer.start(self.interval)  # frame interval (ms)
        
    def updateAnim(self):
        if self.frame <= self.numFrames:
            self.canvas.plot(self.curCoordsFile, self.curLocalFile, self.frame)
            self.frame += 1
        else:
            self.timer.stop()
      
    def updateSlider(self, outputDir):
        """ 
         Updates the slider range and scale factors according to the local data recording parameters used 
         (in the parameters file).
        """
        if os.path.exists(os.path.join(outputDir, "params.txt")):
            params = np.loadtxt(os.path.join(outputDir, "params.txt"))
            self.recStart = int(params[28])
            self.recEnd = int(params[29])
            self.recIntervalLocal = int(params[31])
            self.plotSlider.setMinimum(0) 
            self.plotSlider.setMaximum(int((self.recEnd - self.recStart) / self.recIntervalLocal))
            self.plotSlider.setSingleStep(1)
            self.plotSlider.setPageStep(1) 
            self.plotSlider.setTickInterval(1)
            self.plotSlider.setValue(0) 
            self.updateSliderText(0) 
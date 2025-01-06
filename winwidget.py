# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 16:10:48 2025

@author: biol0117
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QGridLayout, QTabWidget
import widgetparams
import widgetrun
import widgetplot

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
        
        self.paramSpace = widgetparams.WidgetParams(advWindow)
        self.simRunSpace = widgetrun.WidgetRun(self)
        plotTabs = QTabWidget(self)
        self.totalsPlotSpace = widgetplot.WidgetPlotTotals()
        self.coordsPlotSpace = widgetplot.WidgetPlotCoords()
        self.localPlotSpace = widgetplot.WidgetPlotLocal()
        self.plotSpaces = [self.totalsPlotSpace, self.coordsPlotSpace, self.localPlotSpace]
        plotTabs.addTab(self.totalsPlotSpace, "Totals")
        plotTabs.addTab(self.coordsPlotSpace, "Coords")
        plotTabs.addTab(self.localPlotSpace, "Local - Drive allele freq.")
        
        # layout structure
        self.mainBox = QGroupBox()
        layout = QGridLayout()
        
        # 'parameters' box
        parametersBox = QGroupBox()
        layout1 = QGridLayout()
        layout1.addWidget(self.paramSpace, 0, 0, 20, 2)
        parametersBox.setLayout(layout1)
        
        # 'running simulation' box
        runSimBox = QGroupBox()
        layout2 = QGridLayout()
        layout2.addWidget(self.simRunSpace, 0, 0, 18, 2)
        runSimBox.setLayout(layout2)
        
        # 'plotspace' box
        plotSpaceBox = QGroupBox()
        layout3 = QGridLayout()
        layout3.addWidget(plotTabs, 2, 0, 18, 5)
        plotSpaceBox.setLayout(layout3)
        
        layout.addWidget(parametersBox, 0, 0, 3, 1) 
        layout.addWidget(runSimBox, 0, 3, 1, 5)
        layout.addWidget(plotSpaceBox, 1, 3, 5, 5)
        self.mainBox.setLayout(layout)
        
    def createParamsFile(self, outputDir):
        customSet = self.paramSpace.createParamsFile(outputDir)
        return customSet
    
    def copyAdvFiles(self, outputDir):
        self.paramSpace.copyAdvFiles(outputDir)
    
    def runStarted(self):
        for plot in self.plotSpaces:
            plot.runStarted()
    
    def runFinished(self, outputDir):
        for plot in self.plotSpaces:
            plot.runFinished(outputDir)
        
    def isSimRunning(self):
        self.simRunSpace.isSimRunning()
      
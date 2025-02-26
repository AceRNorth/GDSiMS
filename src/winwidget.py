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
    """ Contains all section components of the main window. Manages interactions between them. """
    
    def __init__(self, advWindow): 
        """
        Parameters
        ----------
        advWindow : AdvancedWindow
            Advanced parameter window.
        """
        super().__init__()
        self.createGridLayout(advWindow) # creates layout to place widgets in window
        
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.mainBox)
        self.setLayout(windowLayout)
        self.show()
        
    def createGridLayout(self, advWindow):
        # widgets
        """
        Contains all widgets and sets the layout for the main window.
        
        Parameters
        ----------
        advWindow : AdvancedWindow
            Advanced parameter window.
        """
        
        self.paramSpace = widgetparams.WidgetParams(advWindow)
        self.simRunSpace = widgetrun.WidgetRun(self)
        plotTabs = QTabWidget(self)
        self.totalsGenPlotSpace = widgetplot.WidgetPlotTotalsGen()
        self.totalsAllelePlotSpace = widgetplot.WidgetPlotTotalsAllele()
        self.coordsPlotSpace = widgetplot.WidgetPlotCoords()
        self.localPlotSpace = widgetplot.WidgetPlotLocal(self)
        self.plotSpaces = [self.totalsGenPlotSpace, self.totalsAllelePlotSpace, self.coordsPlotSpace, self.localPlotSpace]
        plotTabs.addTab(self.totalsGenPlotSpace, "Totals - Genotype")
        plotTabs.addTab(self.totalsAllelePlotSpace, "Totals - Allele freq.")
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
        
    def createParamsFiles(self, outputDir):
        """
        Creates parameter files for the simulation run in the selected simulation output directory using the current UI parameter values.
        
        Parameters
        ----------
        outputDirPath : Path
            Absolute path to the simulation output directory.
        
        Returns
        -------
        InputParams
            Custom parameter set.

        """
        customSet = self.paramSpace.createParamsFiles(outputDir)
        return customSet
    
    def copyAdvFiles(self, outputDir):
        """
        Makes a copy of the advanced parameter files selected in the simulation output directory.

        Parameters
        ----------
        outputDir : Path
            Absolute path to the simulation output directory.

        Returns
        -------
        None.

        """
        self.paramSpace.copyAdvFiles(outputDir)
    
    def validParams(self):
        isValid, errMsgs = self.paramSpace.validParams()
        return (isValid, errMsgs)
    
    def runStarted(self):
        """ Makes changes to all plotspace components after a simulation run has started. """
        for plot in self.plotSpaces:
            plot.runStarted()
    
    def runFinished(self, outputDir):
        """ Makes changes to all plotspace components after a simulation run has finished. """
        for plot in self.plotSpaces:
            plot.runFinished(outputDir)
        
    def isSimRunning(self):
        """
        Returns
        -------
        bool
            Whether the simulation is still running.

        """
        self.simRunSpace.isSimRunning()
        
    def saveAnimStarted(self):
        """ Makes necessary changes to the UI after a saving animation file process has started. """
        self.simRunSpace.disableRunBtn()
        
    def saveAnimFinished(self):
        """ Makes necessary changes to the UI after a saving animation file process has finished. """
        self.simRunSpace.enableRunBtn()
      
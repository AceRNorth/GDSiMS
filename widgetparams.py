# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 15:12:05 2025

@author: biol0117
"""

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QComboBox, QPushButton, QFrame, QSpinBox, QDoubleSpinBox
from PyQt5.QtGui import QPalette, QColor
import csv
import params

class WidgetParams(QWidget):
    """ Contains simulation parameter UI components. """
    def __init__(self, advWindow):
        """
        Parameters
        ----------
        advWindow : AdvancedWindow
            Advanced parameter window.
        """
        super().__init__()
        self.advWindow = advWindow
        self.advWindow.hide()
        
        self.setLayout(QGridLayout())
        self.initUI()
        
        self.initParamSets()
        
    def initUI(self): 
        """ Creates the UI components and places them. """
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
        #setsCB.setFixedWidth(160)
        setsBtn = QPushButton("Load")
        setsBtn.setToolTip("Load selected parameter set")
        #setsBtn.setFixedWidth(100)
        setsBtn.clicked.connect(lambda: self.loadSet(setsCB.currentIndex()))
        
        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        pal = line1.palette()
        pal.setColor(QPalette.WindowText, QColor("lightGray"))
        line1.setPalette(pal)
        
        progTitle = QLabel("Simulation")
        self.numRunsLabel = QLabel("no. of replicates")
        self.numRunsLabel.setToolTip("Number of simulation replicates to run.")
        self.numRunsSB = QSpinBox()
        self.numRunsSB.setMinimum(1)
        self.numRunsSB.setMaximum(10000)
        self.numRunsSB.setValue(1)
        self.numRunsSB.resize(self.numRunsSB.sizeHint())
        self.maxTLabel = QLabel("simulation time")
        self.maxTLabel.setToolTip("Maximum simulated time (in days).")
        self.maxTSB = QSpinBox()
        self.maxTSB.setMinimum(1)
        self.maxTSB.setMaximum(10000)
        self.maxTSB.setValue(1500)
        self.maxTSB.setSingleStep(100)
        self.maxTSB.resize(self.maxTSB.sizeHint())
        self.numPatLabel = QLabel("no. of patches")
        self.numPatLabel.setToolTip("Number of population sites chosen for the simulation.")
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
        self.xiLabel = QLabel("fitness cost")
        self.xiLabel.setToolTip("Somatic Cas9 expression fitness cost.")
        self.xiSB = QDoubleSpinBox()
        self.xiSB.setMinimum(0.0)
        self.xiSB.setMaximum(1.0)
        self.xiSB.setValue(0.5)
        self.xiSB.setSingleStep(0.05)
        self.xiSB.resize(self.xiSB.sizeHint())
        self.eLabel = QLabel("homing rate")
        self.eLabel.setToolTip("Homing rate in females.")
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
        self.driverStartLabel = QLabel("release time")
        self.driverStartLabel.setToolTip("Time to start releasing drive alleles into the mosquito population.")
        self.driverStartSB = QSpinBox()
        self.driverStartSB.setMinimum(1)
        self.driverStartSB.setMaximum(10000)
        self.driverStartSB.setValue(200)
        self.driverStartSB.setSingleStep(100)
        self.driverStartSB.resize(self.driverStartSB.sizeHint())
        
        self.numDriverMLabel = QLabel("release size")
        self.numDriverMLabel.setToolTip("Number of drive heterozygous (WD) male mosquitoes per release.")
        self.numDriverMSB = QSpinBox()
        self.numDriverMSB.setMinimum(0)
        self.numDriverMSB.setMaximum(100000)
        self.numDriverMSB.setValue(1000)
        self.numDriverMSB.setSingleStep(100)
        self.numDriverMSB.resize(self.numDriverMSB.sizeHint())
        self.numDriverSitesLabel = QLabel("no. of release patches")
        self.numDriverSitesLabel.setToolTip("Number of gene drive release sites per year.")
        self.numDriverSitesSB = QSpinBox()
        self.numDriverSitesSB.setMinimum(0)
        self.numDriverSitesSB.setMaximum(100000)
        self.numDriverSitesSB.setValue(1)
        self.numDriverSitesSB.resize(self.numDriverSitesSB.sizeHint())
        
        line4 = QFrame()
        line4.setFrameShape(QFrame.HLine)
        line4.setPalette(pal)
        
        recTitle = QLabel("Recording")
        self.setLabelLabel = QLabel("simulation label")
        self.setLabelLabel.setToolTip("'Set of repetitions' index label for output files.")
        self.setLabelSB = QSpinBox()
        self.setLabelSB.setMaximum(10000000)
        self.setLabelSB.setValue(1)
        self.setLabelSB.resize(self.setLabelSB.sizeHint())
        self.recIntervalLocalLabel = QLabel("output frequency (full data)")
        self.recIntervalLocalLabel.setToolTip("Time interval at which to collect/record local data (in days). A low value produces higher temporal resolution data though will result in larger output file sizes.")
        self.recIntervalLocalSB = QSpinBox()
        self.recIntervalLocalSB.setMinimum(1)
        self.recIntervalLocalSB.setMaximum(100000)
        self.recIntervalLocalSB.setValue(365)
        self.recIntervalLocalSB.setSingleStep(100)
        self.recIntervalLocalSB.resize(self.recIntervalLocalSB.sizeHint())
        
        line5 = QFrame()
        line5.setFrameShape(QFrame.HLine)
        line5.setPalette(pal)

        advancedBtn = QPushButton("Advanced")
        advancedBtn.setToolTip("Advanced parameters")
        advancedBtn.clicked.connect(self.openAdvanced)
        
        self.layout().addWidget(setsLabel, 1, 0, 1, 2)
        self.layout().addWidget(setsCB, 2, 0, 1, 1)
        self.layout().addWidget(setsBtn, 2, 1)
        self.layout().addWidget(line1, 3, 0, 1, 2)
        self.layout().addWidget(progTitle, 4, 0, 1, 2)
        self.layout().addWidget(self.numRunsLabel, 5, 0)
        self.layout().addWidget(self.numRunsSB, 5, 1)
        self.layout().addWidget(self.maxTLabel, 6, 0)
        self.layout().addWidget(self.maxTSB, 6, 1)
        self.layout().addWidget(self.numPatLabel, 7, 0)
        self.layout().addWidget(self.numPatSB, 7, 1)
        self.layout().addWidget(line2, 8, 0, 1, 2)
        self.layout().addWidget(inherTitle, 9, 0, 1, 2)
        self.layout().addWidget(self.xiLabel, 10, 0)
        self.layout().addWidget(self.xiSB, 10, 1)
        self.layout().addWidget(self.eLabel, 11, 0)
        self.layout().addWidget(self.eSB, 11, 1)
        self.layout().addWidget(line3, 12, 0, 1, 2)
        self.layout().addWidget(releaseTitle, 13, 0, 1, 2)
        self.layout().addWidget(self.driverStartLabel, 14, 0)
        self.layout().addWidget(self.driverStartSB, 14, 1)
        self.layout().addWidget(self.numDriverMLabel, 15, 0)
        self.layout().addWidget(self.numDriverMSB, 15, 1)
        self.layout().addWidget(self.numDriverSitesLabel, 16, 0)
        self.layout().addWidget(self.numDriverSitesSB, 16, 1)
        self.layout().addWidget(line4, 18, 0, 1, 2)
        self.layout().addWidget(recTitle, 19, 0)
        self.layout().addWidget(self.setLabelLabel, 20, 0)
        self.layout().addWidget(self.setLabelSB, 20, 1)
        self.layout().addWidget(self.recIntervalLocalLabel, 21, 0)
        self.layout().addWidget(self.recIntervalLocalSB, 21, 1)
        self.layout().addWidget(line5, 22, 0, 1, 2)
        self.layout().addWidget(advancedBtn, 23, 0)
        
        self.layout().setColumnStretch(0, 3)
        self.layout().setColumnStretch(1, 2)
      
    def initParamSets(self):
        """ Initialises the pre-defined parameter sets. """
        # set 1 - default
        set1 = params.InputParams(
                numRuns = 1, 
                maxT = 1500,
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
                recStart = 200,
                recEnd = 1500,
                recIntervalGlobal = 1,
                recIntervalLocal = 365,
                recSitesFreq = 1,
                setLabel = 1,
                dispType = "Radial",
                boundaryType = "Toroid",
                rainfallFile = None,
                coordsFile = None,
                relTimesFile = None
                )
        # set 2 - low fitness cost
        set2 = params.InputParams(
                numRuns = 1, 
                maxT = 1500,
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
                recStart = 200,
                recEnd = 1500,
                recIntervalGlobal = 1,
                recIntervalLocal = 365,
                recSitesFreq = 1,
                setLabel = 2,
                dispType = "Radial",
                boundaryType = "Toroid",
                rainfallFile = None,
                coordsFile = None,
                relTimesFile = None
                )
        # set 3 - high fitness cost
        set3 = params.InputParams(
                numRuns = 1, 
                maxT = 1500,
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
                recStart = 200,
                recEnd = 1500,
                recIntervalGlobal = 1,
                recIntervalLocal = 365,
                recSitesFreq = 1,
                setLabel = 3,
                dispType = "Radial",
                boundaryType = "Toroid",
                rainfallFile = None,
                coordsFile = None,
                relTimesFile = None
                )
        # set 4 - high number of release sites
        set4 = params.InputParams(
                numRuns = 1, 
                maxT = 1500,
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
                recStart = 200,
                recEnd = 1500,
                recIntervalGlobal = 1,
                recIntervalLocal = 365,
                recSitesFreq = 1,
                setLabel = 4,
                dispType = "Radial",
                boundaryType = "Toroid",
                rainfallFile = None,
                coordsFile = None,
                relTimesFile = None
                )
        # set 5 - low dispersal rate
        set5 = params.InputParams(
                numRuns = 1, 
                maxT = 1500,
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
                recStart = 200,
                recEnd = 1500,
                recIntervalGlobal = 1,
                recIntervalLocal = 365,
                recSitesFreq = 1,
                setLabel = 5,
                dispType = "Radial",
                boundaryType = "Toroid",
                rainfallFile = None,
                coordsFile = None,
                relTimesFile = None
                )
        # set 6 - high dispersal rate
        set6 = params.InputParams(
                numRuns = 1, 
                maxT = 1500,
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
                recStart = 200,
                recEnd = 1500,
                recIntervalGlobal = 1,
                recIntervalLocal = 365,
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
        """
        Update the UI parameter box values on all windows with those from the parameter set selected .

        Parameters
        ----------
        setIndex : int
            Parameter set index (respective to sets attribute).

        Returns
        -------
        None.

        """
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
        self.setLabelSB.setValue(self.sets[setIndex].setLabel)
        self.recIntervalLocalSB.setValue(self.sets[setIndex].recIntervalLocal)
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
        """ Opens the advanced parameters window."""
        self.advWindow.openWin()
        
    def createParamsFiles(self, outputDirPath):
        """
        Creates a parameters file for the simulation run in the selected simulation output directory using the current UI parameter values.

        Parameters
        ----------
        outputDirPath : Path
            Absolute path to the simulation output directory.

        Returns
        -------
        InputParams
            Custom parameter set.

        """
        advParams = self.advWindow.getParams()
        self.customSet = params.InputParams(
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
                            recStart = self.driverStartSB.value() if advParams.relTimesFile == False else advParams.newDriverStart,
                            recEnd = self.maxTSB.value(),
                            recIntervalGlobal = 1,
                            recIntervalLocal = self.recIntervalLocalSB.value(),
                            recSitesFreq = 1,
                            setLabel = self.setLabelSB.value(),
                            dispType = self.advWindow.dispType,
                            boundaryType = self.advWindow.boundaryType,
                            rainfallFile = None if advParams.rainfallFile == False else self.advWindow.rainfallFile,
                            coordsFile = None if advParams.patchCoordsFile == False else self.advWindow.coordsFile,
                            relTimesFile = None if advParams.relTimesFile == False else self.advWindow.relTimesFile
                        )
        
        advParamsInfo = self.advWindow.getParamsInfo()
        self.customSetInfo = params.InputParams(
                                numRuns = (self.numRunsLabel.text(), self.numRunsLabel.toolTip()), 
                                maxT = (self.maxTLabel.text(), self.maxTLabel.toolTip()),
                                numPat = (self.numPatLabel.text(), self.numPatLabel.toolTip()),
                                muJ = advParamsInfo.muJ,
                                muA = advParamsInfo.muA,
                                beta = advParamsInfo.beta,
                                theta = advParamsInfo.theta,
                                compPower = advParamsInfo.compPower,
                                minDev = advParamsInfo.minDev,
                                gamma = advParamsInfo.gamma,
                                xi = (self.xiLabel.text(), self.xiLabel.toolTip()),
                                e = (self.eLabel.text(), self.eLabel.toolTip()),
                                driverStart = (self.driverStartLabel.text(), self.driverStartLabel.toolTip()),
                                numDriverM = (self.numDriverMLabel.text(), self.numDriverMLabel.toolTip()),
                                numDriverSites = (self.numDriverSitesLabel.text(), self.numDriverSitesLabel.toolTip()),
                                dispRate = advParamsInfo.dispRate,
                                maxDisp = advParamsInfo.maxDisp,
                                psi = advParamsInfo.psi,
                                muAes = advParamsInfo.muAes,
                                tHide1 = advParamsInfo.tHide1,
                                tHide2 = advParamsInfo.tHide2,
                                tWake1 = advParamsInfo.tWake1,
                                tWake2 = advParamsInfo.tWake2,
                                alpha0Mean = advParamsInfo.alpha0Mean,
                                alpha0Variance = advParamsInfo.alpha0Var,
                                alpha1 = advParamsInfo.alpha1,
                                amp = advParamsInfo.amp,
                                resp = advParamsInfo.resp,
                                recStart = ("output start (full data)", "Start time for the full data recording window. Has been set equal to the release time."),
                                recEnd = ("output end (full data)", "End time for the full data recording window. Has been set equal to the simulation time."),
                                recIntervalGlobal = ("output frequency (summary data)", "Time interval for summary data recording. Has been set to 1."),
                                recIntervalLocal = (self.recIntervalLocalLabel.text(), self.recIntervalLocalLabel.toolTip()),
                                recSitesFreq = ("local site freq.", "Fraction of sites to collect local data for (1 is all sites. 10 is 1 in 10 etc). Has been set to 1."),
                                setLabel = (self.setLabelLabel.text(), self.setLabelLabel.toolTip()),
                                dispType = advParamsInfo.dispType,
                                boundaryType = advParamsInfo.boundaryType,
                                rainfallFile = advParamsInfo.rainfallFile,
                                coordsFile = advParamsInfo.patchCoordsFile,
                                relTimesFile = advParamsInfo.relTimesFile
                            )
        
        self.createProgramParamsFile(outputDirPath, self.customSet)
        self.createUserParamsFile(outputDirPath, self.customSet, self.customSetInfo)
            
        return self.customSet
    
    def createProgramParamsFile(self, outputDir, paramSet):
        # turn class data into "params.txt" file in selected outputDir path
        filePath = outputDir / "params.txt"
        with open(filePath, "w") as file:
            file.write(str(paramSet.numRuns) + "\n")
            file.write(str(paramSet.maxT) + "\n")
            file.write(str(paramSet.numPat) + "\n")
            file.write(str(paramSet.muJ) + "\n")
            file.write(str(paramSet.muA) + "\n")
            file.write(str(paramSet.beta) + "\n")
            file.write(str(paramSet.theta) + "\n")
            file.write(str(paramSet.compPower) + "\n")
            file.write(str(paramSet.minDev) + "\n")
            file.write(str(paramSet.gamma) + "\n")
            file.write(str(paramSet.xi) + "\n")
            file.write(str(paramSet.e) + "\n")
            file.write(str(paramSet.driverStart) + "\n")
            file.write(str(paramSet.numDriverM) + "\n")
            file.write(str(paramSet.numDriverSites) + "\n")
            file.write(str(paramSet.dispRate) + "\n")
            file.write(str(paramSet.maxDisp) + "\n")
            file.write(str(paramSet.psi) + "\n")
            file.write(str(paramSet.muAes) + "\n")
            file.write(str(paramSet.tHide1) + "\n")
            file.write(str(paramSet.tHide2) + "\n")
            file.write(str(paramSet.tWake1) + "\n")
            file.write(str(paramSet.tWake2) + "\n")
            file.write(str(paramSet.alpha0Mean) + "\n")
            file.write(str(paramSet.alpha0Variance) + "\n")
            file.write(str(paramSet.alpha1) + "\n")
            file.write(str(paramSet.amp) + "\n")
            file.write(str(paramSet.resp) + "\n")
            file.write(str(paramSet.recStart) + "\n")
            file.write(str(paramSet.recEnd) + "\n")
            file.write(str(paramSet.recIntervalGlobal) + "\n")
            file.write(str(paramSet.recIntervalLocal) + "\n")
            file.write(str(paramSet.recSitesFreq) + "\n")
            file.write(str(paramSet.setLabel) + "\n")
            
    def createUserParamsFile(self, outputDir, paramSet, info):
        # turn class data into "params.txt" file in selected outputDir path
        filePath = outputDir / "paramsInfo.csv"
        with open(filePath, 'w', newline='') as csvfile:
            fw = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            fw.writerow(["Parameter name", "Program equivalent", "Value", "Description"])
            fw.writerow([info.numRuns[0], "num_runs", str(paramSet.numRuns), info.numRuns[1]])
            fw.writerow([info.maxT[0], "max_t", str(paramSet.maxT), info.maxT[1]])
            fw.writerow([info.numPat[0], "num_pat", str(paramSet.numPat), info.numPat[1]])
            fw.writerow([info.muJ[0], "mu_j", str(paramSet.muJ), info.muJ[1]])
            fw.writerow([info.muA[0], "mu_a", str(paramSet.muA), info.muA[1]])
            fw.writerow([info.beta[0], "beta", str(paramSet.beta), info.beta[1]])
            fw.writerow([info.theta[0], "theta", str(paramSet.theta), info.theta[1]])
            fw.writerow([info.compPower[0], "comp_power", str(paramSet.compPower), info.compPower[1]])
            fw.writerow([info.minDev[0], "min_dev", str(paramSet.minDev), info.minDev[1]])
            fw.writerow([info.gamma[0], "gamma", str(paramSet.gamma), info.gamma[1]])
            fw.writerow([info.xi[0], "xi", str(paramSet.xi), info.xi[1]])
            fw.writerow([info.e[0], "e", str(paramSet.e), info.e[1]])
            fw.writerow([info.driverStart[0], "driver_start", str(paramSet.driverStart), info.driverStart[1]])
            fw.writerow([info.numDriverM[0], "num_driver_M", str(paramSet.numDriverM), info.numDriverM[1]])
            fw.writerow([info.numDriverSites[0], "num_driver_sites", str(paramSet.numDriverSites), info.numDriverSites[1]])
            fw.writerow([info.dispRate[0], "disp_rate", str(paramSet.dispRate), info.dispRate[1]])
            fw.writerow([info.maxDisp[0], "max_disp", str(paramSet.maxDisp), info.maxDisp[1]])
            fw.writerow([info.psi[0], "psi", str(paramSet.psi), info.psi[1]])
            fw.writerow([info.muAes[0], "mu_aes", str(paramSet.muAes), info.muAes[1]])
            fw.writerow([info.tHide1[0], "t_hide1", str(paramSet.tHide1), info.tHide1[1]])
            fw.writerow([info.tHide2[0], "t_hide2", str(paramSet.tHide2), info.tHide2[1]])
            fw.writerow([info.tWake1[0], "t_wake1", str(paramSet.tWake1), info.tWake1[1]])
            fw.writerow([info.tWake2[0], "t_wake2", str(paramSet.tWake2), info.tWake2[1]])
            fw.writerow([info.alpha0Mean[0], "alpha0_mean", str(paramSet.alpha0Mean), info.alpha0Mean[1]])
            fw.writerow([info.alpha0Variance[0], "alpha0_variance", str(paramSet.alpha0Variance), info.alpha0Variance[1]])
            fw.writerow([info.alpha1[0], "alpha1", str(paramSet.alpha1), info.alpha1[1]])
            fw.writerow([info.amp[0], "amp", str(paramSet.amp), info.amp[1]])
            fw.writerow([info.resp[0], "resp", str(paramSet.resp), info.resp[1]])
            fw.writerow([info.recStart[0], "rec_start", str(paramSet.recStart), info.recStart[1]])
            fw.writerow([info.recEnd[0], "rec_end", str(paramSet.recEnd), info.recEnd[1]])
            fw.writerow([info.recIntervalGlobal[0], "rec_interval_global", str(paramSet.recIntervalGlobal), info.recIntervalGlobal[1]])
            fw.writerow([info.recIntervalLocal[0], "rec_interval_local", str(paramSet.recIntervalLocal), info.recIntervalLocal[1]])
            fw.writerow([info.recSitesFreq[0], "rec_sites_freq", str(paramSet.recSitesFreq), info.recSitesFreq[1]])
            fw.writerow([info.setLabel[0], "set_label", str(paramSet.setLabel), info.setLabel[1]])
            fw.writerow([info.dispType[0], "", str(paramSet.dispType), info.dispType[1]])
            fw.writerow([info.boundaryType[0], "", str(paramSet.boundaryType), info.boundaryType[1]])
            fw.writerow([info.rainfallFile[0], "", "None" if paramSet.rainfallFile==None else str(paramSet.rainfallFile), info.rainfallFile[1]])
            fw.writerow([info.coordsFile[0], "", "None" if paramSet.coordsFile==None else str(paramSet.coordsFile), info.coordsFile[1]])
            fw.writerow([info.relTimesFile[0], "", "None" if paramSet.relTimesFile==None else str(paramSet.relTimesFile), info.relTimesFile[1]])
      
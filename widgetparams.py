# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 15:12:05 2025

@author: biol0117
"""

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QComboBox, QPushButton, QFrame, QSpinBox, QDoubleSpinBox
from PyQt5.QtGui import QPalette, QColor
import os
import shutil
import params

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
        set1 = params.InputParams(
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
        
        set2 = params.InputParams(
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
        
        set3 = params.InputParams(
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
        
        set4 = params.InputParams(
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
        
        set5 = params.InputParams(
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
        
        set6 = params.InputParams(
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
    
    def copyAdvFiles(self, outputDir):
        if self.customSet.rainfallFile != None:
            shutil.copy(self.customSet.rainfallFile, os.path.join(outputDir, "rainfall.txt"))
        if self.customSet.coordsFile != None:
            shutil.copy(self.customSet.coordsFile, os.path.join(outputDir, "coords.txt"))
        if self.customSet.relTimesFile != None:
            shutil.copy(self.customSet.relTimesFile, os.path.join(outputDir, "reltimes.txt"))
      
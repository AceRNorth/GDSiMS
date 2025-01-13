# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 14:46:45 2025

@author: biol0117
"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QGroupBox, QGridLayout, QLabel, QSpinBox, QFrame, QDoubleSpinBox, QComboBox, QCheckBox, QLineEdit, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import Qt
from pathlib import Path
import numpy as np
import re

class AdvParams():
    """UI component values for the advanced parameters window. """
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
       

class AdvancedWindow(QDialog):
    """ Contains the simulation's advanced parameter UI components and applies the changes. """
    
    def __init__(self, parentWin):
        """
        Parameters
        ----------
        parentWin : MainWindow
            Parent window.
        """
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
        """ Initialises the UI. """
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height) # sets position and size of window
    
        self.createGridLayout() # creates layout to place widgets in window
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
        self.openWin()
        
    def openWin(self):
        """ Opens the window if closed and moves it to the top layer. """
        self.show()
        self.activateWindow() # moves the window to the top
        self.saveValues() # save starting values in case need to reset when close window without saving
        self.okBtn.setDefault(True)
        self.okBtn.setAutoDefault(True)
        
    def closeEvent(self, event):
        """ 
        Closes the window without applying the most recent changes. 
        Resets the parameter boxes to the last values applied.
        
        Parameters
        ----------
        event : QCloseEvent
        """
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
        """ Saves the last applied changes to UI parameter box values/states. """
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
        """
        Returns
        -------
        AdvParams()
            Last saved UI parameter box values/states.

        """
        return self.lastVals
    
    def createGridLayout(self):
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
        """  Shows/hides extra UI components depending on the boundary type selected. """
        self.coordsFileCheckbox.setChecked(False)
        if self.boundaryTypeCB.currentText() == "Toroid":
            self.coordsFileLabel.hide()
            self.coordsFileCheckbox.hide()
            
        if self.boundaryTypeCB.currentText() == "Edge":
            self.coordsFileLabel.show()
            self.coordsFileCheckbox.show()
        
    def checkboxState(self, checkBox, showLabelElements, showNumElements=[], showTextElements=[], hideLabelElements=[], hideNumElements=[]):
        """
        Shows or hides UI components depending on the state of the checkbox. 

        Parameters
        ----------
        checkBox : QCheckBox
        
        showLabelElements : list:QLabel
            Label elements to show when checkbox is checked.
        showNumElements : list:QSpinBox, optional
            Number-based box elements to show when checkbox is checked. The default is [].
        showTextElements : list:QLineEdit, optional
            Text edit elements to show when checkbox is checked. The default is [].
        hideLabelElements : list:QLabel, optional
            Label elements to hide when checkbox is checked. The default is [].
        hideNumElements : list:QSpinBox, optional
            Number-based box elements to hide when checkbox is checked. The default is [].

        Returns
        -------
        None.

        """
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
        """
        Opens a file dialog box to select a file, saves the filename and updates the text edit box with the filename. 

        Parameters
        ----------
        filename : Path
            Variable to save the absolute filepath to.
        filenameEdit : QLineEdit
            Text edit box to update.

        Returns
        -------
        None.

        """
        fname, ok = QFileDialog.getOpenFileName(self, "Select a file", ".", "Text files (*.txt)")
        if fname:
            filename = Path(fname)
            filenameEdit.setText(str(filename))
            
    def validParams(self):
        """
        Checks the validity of parameters. Checks for interval errors and file value errors, if advanced parameter files have been provided.

        Returns
        -------
        isValid : bool
            Whether all the parameters are valid.
        errMsgs : list:string
            Error messages.

        """
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
        """ Enables the apply button. """
        if self.applyBtn.isEnabled() == False:
            self.applyBtn.setEnabled(True)
        
    def applyChanges(self, btn):
        """
        Apply and save changes to parameter values with dialog button if values are valid. Otherwise, show error message.
        If the dialog button is OK, also close window.

        Parameters
        ----------
        btn : str
            Type of dialog button. Options: "ok", "apply"

        Returns
        -------
        None.

        """
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
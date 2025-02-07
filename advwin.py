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
    recIntervalLocal = 365
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
        self.left = 700
        self.top = 200
        self.width = 400
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
        self.recIntervalLocalSB.setValue(self.lastVals.recIntervalLocal)
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
        self.lastVals.recIntervalLocal = self.recIntervalLocalSB.value()
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
        self.setLabelLabel = QLabel("simulation label")
        self.setLabelLabel.setToolTip("'Set of repetitions' index label for output files.")
        self.setLabelSB = QSpinBox()
        self.setLabelSB.setMaximum(10000000)
        self.setLabelSB.setValue(1)
        self.setLabelSB.resize(self.setLabelSB.sizeHint())
        self.setLabelSB.valueChanged.connect(self.enableApply)
        self.recIntervalLocalLabel = QLabel("output frequency (full data)")
        self.recIntervalLocalLabel.setToolTip("Time interval at which to collect/record local data (in days). A low value produces higher temporal resolution data though will result in larger output file sizes.")
        self.recIntervalLocalSB = QSpinBox()
        self.recIntervalLocalSB.setMinimum(1)
        self.recIntervalLocalSB.setMaximum(100000)
        self.recIntervalLocalSB.setValue(365)
        self.recIntervalLocalSB.setSingleStep(100)
        self.recIntervalLocalSB.resize(self.recIntervalLocalSB.sizeHint())
        self.recIntervalLocalSB.valueChanged.connect(self.enableApply)
        
        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        pal = line1.palette()
        pal.setColor(QPalette.WindowText, QColor("lightGray"))
        line1.setPalette(pal)
        
        lifeTitle = QLabel("Mosquito life processes")
        self.muJLabel = QLabel("juvenile mortality rate")
        self.muJLabel.setToolTip("Juvenile density independent mortality rate per day.")
        self.muJSB = QDoubleSpinBox()
        self.muJSB.setMinimum(0)
        self.muJSB.setMaximum(0.99) # should not include 1
        self.muJSB.setValue(0.05)
        self.muJSB.setSingleStep(0.05)
        self.muJSB.resize(self.muJSB.sizeHint())
        self.muJSB.valueChanged.connect(self.enableApply)
        self.muALabel = QLabel("adult mortality rate")
        self.muALabel.setToolTip("Adult mortality rate per day.")
        self.muASB = QDoubleSpinBox()
        self.muASB.setDecimals(3)
        self.muASB.setMinimum(0.001) # should not include 0
        self.muASB.setMaximum(0.999) # should not include 1
        self.muASB.setValue(0.125)
        self.muASB.setSingleStep(0.005)
        self.muASB.resize(self.muASB.sizeHint())
        self.muASB.valueChanged.connect(self.enableApply)
        self.betaLabel = QLabel("mating rate factor")
        self.betaLabel.setToolTip("Number of males in a patch when local females mate with probability ½ per day.")
        self.betaSB = QDoubleSpinBox()
        self.betaSB.setMinimum(0.01) # should not include 0
        self.betaSB.setMaximum(10000) # ?
        self.betaSB.setValue(100)
        self.betaSB.setSingleStep(10)
        self.betaSB.resize(self.betaSB.sizeHint())
        self.betaSB.valueChanged.connect(self.enableApply)
        self.thetaLabel = QLabel("egg laying rate")
        self.thetaLabel.setToolTip("Average egg laying rate of wildtype females (eggs per day).")
        self.thetaSB = QDoubleSpinBox()
        self.thetaSB.setMinimum(0.01) # should not include 0
        self.thetaSB.setMaximum(10000)
        self.thetaSB.setValue(9)
        self.thetaSB.resize(self.thetaSB.sizeHint())
        self.thetaSB.valueChanged.connect(self.enableApply)
        self.compPowerLabel = QLabel("juvenile survival factor")
        self.compPowerLabel.setToolTip("Parameter that controls the juvenile survival probability.")
        self.compPowerSB = QDoubleSpinBox()
        self.compPowerSB.setMinimum(0.000000001) # should not include 0
        self.compPowerSB.setMaximum(10000)
        self.compPowerSB.setDecimals(9)
        self.compPowerSB.setValue(0.066666667)
        self.compPowerSB.setSingleStep(0.1)
        self.compPowerSB.resize(self.compPowerSB.sizeHint())
        self.compPowerSB.valueChanged.connect(self.enableApply)
        self.minDevLabel = QLabel("juvenile min. development time")
        self.minDevLabel.setToolTip("Minimum development time for a juvenile (in days).")
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
        self.dispRateLabel = QLabel("dispersal rate")
        self.dispRateLabel.setToolTip("Adult dispersal rate.")
        self.dispRateSB = QDoubleSpinBox()
        self.dispRateSB.setDecimals(3)
        self.dispRateSB.setMinimum(0)
        self.dispRateSB.setMaximum(1)
        self.dispRateSB.setValue(0.01)
        self.dispRateSB.setSingleStep(0.005)
        self.dispRateSB.resize(self.dispRateSB.sizeHint())
        self.dispRateSB.valueChanged.connect(self.enableApply)
        self.maxDispLabel = QLabel("max. dispersal distance")
        self.maxDispLabel.setToolTip("Maximum dispersal distance at which two sites are connected.")
        self.maxDispSB = QDoubleSpinBox()
        self.maxDispSB.setMinimum(0.01) # should not include 0
        self.maxDispSB.setMaximum(10000) # should be side
        self.maxDispSB.setValue(0.2)
        self.maxDispSB.resize(self.maxDispSB.sizeHint())
        self.maxDispSB.valueChanged.connect(self.enableApply)
        self.dispTypeLabel = QLabel("dispersal type")
        self.dispTypeCB = QComboBox()
        self.dispTypeCB.addItems(["Radial", "Distance kernel"])
        self.dispTypeCB.currentTextChanged.connect(self.enableApply)
        
        line3 = QFrame()
        line3.setFrameShape(QFrame.HLine)
        line3.setPalette(pal)
        
        self.aesTitle = QLabel("Aestivation")
        self.aesCheckbox = QCheckBox()
        self.aesCheckbox.stateChanged.connect(lambda: self.checkboxState(self.aesCheckbox,
            showLabelElements=[self.psiLabel, self.muAesLabel, self.tHide1Label, self.tHide2Label, self.tWake1Label, self.tWake2Label],
            showNumElements=[self.psiSB, self.muAesSB, self.tHide1SB, self.tHide2SB, self.tWake1SB, self.tWake2SB])
        )
        self.aesCheckbox.stateChanged.connect(self.enableApply)
        self.psiLabel = QLabel("aestivation rate")
        self.psiLabel.setToolTip("Aestivation rate.")
        self.psiSB = QDoubleSpinBox()
        self.psiSB.setMinimum(0)
        self.psiSB.setMaximum(1)
        self.psiSB.setValue(0)
        self.psiSB.setSingleStep(0.05)
        self.psiSB.resize(self.psiSB.sizeHint())
        self.psiSB.valueChanged.connect(self.enableApply)
        self.muAesLabel = QLabel("aestivation mortality")
        self.muAesLabel.setToolTip("Aestivation mortality rate.")
        self.muAesSB = QDoubleSpinBox()
        self.muAesSB.setMinimum(0)
        self.muAesSB.setMaximum(1)
        self.muAesSB.setValue(0)
        self.muAesSB.setSingleStep(0.05)
        self.muAesSB.resize(self.muAesSB.sizeHint())
        self.muAesSB.valueChanged.connect(self.enableApply)
        self.tHide1Label = QLabel("start hiding date")
        self.tHide1Label.setToolTip("Start day of aestivation-hiding period (exclusive).")
        self.tHide1SB = QSpinBox()
        self.tHide1SB.setMinimum(0)
        self.tHide1SB.setMaximum(365)
        self.tHide1SB.setValue(0)
        self.tHide1SB.resize(self.tHide1SB.sizeHint())
        self.tHide1SB.valueChanged.connect(self.enableApply)
        self.tHide2Label = QLabel("end hiding date")
        self.tHide2Label.setToolTip("End day of aestivation-hiding period (inclusive).")
        self.tHide2SB = QSpinBox()
        self.tHide2SB.setMinimum(0) # should be t_hide1
        self.tHide2SB.setMaximum(365)
        self.tHide2SB.setValue(0)
        self.tHide2SB.resize(self.tHide2SB.sizeHint())
        self.tHide2SB.valueChanged.connect(self.enableApply)
        self.tWake1Label = QLabel("start waking date")
        self.tWake1Label.setToolTip("Start day of aestivation-waking period (exclusive).")
        self.tWake1SB = QSpinBox()
        self.tWake1SB.setMinimum(0)
        self.tWake1SB.setMaximum(365)
        self.tWake1SB.setValue(0)
        self.tWake1SB.resize(self.tWake1SB.sizeHint())
        self.tWake1SB.valueChanged.connect(self.enableApply)
        self.tWake2Label = QLabel("end waking date")
        self.tWake2Label.setToolTip("End day of aestivation-waking period (inclusive).")
        self.tWake2SB = QSpinBox()
        self.tWake2SB.setMinimum(0) # should be t_wake1
        self.tWake2SB.setMaximum(365)
        self.tWake2SB.setValue(0)
        self.tWake2SB.resize(self.tWake2SB.sizeHint())
        self.tWake2SB.valueChanged.connect(self.enableApply)
        self.psiLabel.hide()
        self.psiSB.hide()
        self.muAesLabel.hide()
        self.muAesSB.hide()
        self.tHide1Label.hide()
        self.tHide1SB.hide()
        self.tHide2Label.hide()
        self.tHide2SB.hide()
        self.tWake1Label.hide()
        self.tWake1SB.hide()
        self.tWake2Label.hide()
        self.tWake2SB.hide()
        
        line4 = QFrame()
        line4.setFrameShape(QFrame.HLine)
        line4.setPalette(pal)
        
        seasonalityTitle = QLabel("Seasonality")
        self.alpha0MeanLabel = QLabel("population size factor")
        self.alpha0MeanLabel.setToolTip("Mean of the baseline contribution to the carrying capacity.")
        self.alpha0MeanSB = QDoubleSpinBox()
        self.alpha0MeanSB.setMinimum(0.01) # should not include 0
        self.alpha0MeanSB.setMaximum(100000000)
        self.alpha0MeanSB.setValue(100000)
        self.alpha0MeanSB.setSingleStep(10000)
        self.alpha0MeanSB.resize(self.alpha0MeanSB.sizeHint())
        self.alpha0MeanSB.valueChanged.connect(self.enableApply)
        self.alpha0VarLabel = QLabel("population size variance")
        self.alpha0VarLabel.setToolTip("Variance of the baseline contribution to the carrying capacity.")
        self.alpha0VarSB = QDoubleSpinBox()
        self.alpha0VarSB.setMinimum(0)
        self.alpha0VarSB.setMaximum(100000000)
        self.alpha0VarSB.setValue(0)
        self.alpha0VarSB.setSingleStep(1000)
        self.alpha0VarSB.resize(self.alpha0VarSB.sizeHint())
        self.alpha0VarSB.valueChanged.connect(self.enableApply)
        self.alpha1Label = QLabel("rainfall contribution\nto population size")
        self.alpha1Label.setToolTip("Rainfall contribution factor to carrying capacity.")
        self.alpha1SB = QDoubleSpinBox()
        self.alpha1SB.setMinimum(0)
        self.alpha1SB.setMaximum(100000000)
        self.alpha1SB.setValue(0)
        self.alpha1SB.setSingleStep(100)
        self.alpha1SB.resize(self.alpha1SB.sizeHint())
        self.alpha1SB.valueChanged.connect(self.enableApply)
        self.ampLabel = QLabel("rainfall seasonality")
        self.ampLabel.setToolTip("Amplitude of rainfall fluctuations.")
        self.ampSB = QDoubleSpinBox()
        self.ampSB.setMinimum(0)
        self.ampSB.setMaximum(1)
        self.ampSB.setValue(0)
        self.ampSB.setSingleStep(0.1)
        self.ampSB.resize(self.ampSB.sizeHint())
        self.ampSB.valueChanged.connect(self.enableApply)
        self.rainfallFileLabel = QLabel("rainfall file")
        self.rainfallFileLabel.setToolTip("Rainfall data file")
        self.rainfallFileCheckbox = QCheckBox()
        self.rainfallFileCheckbox.stateChanged.connect(lambda: self.checkboxState(self.rainfallFileCheckbox,
            showLabelElements=[rainfallFileDialogBtn, self.respLabel], 
            showNumElements=[self.respSB],
            showTextElements=[self.rainfallFilenameEdit],
            hideLabelElements=[self.ampLabel],
            hideNumElements=[self.ampSB])
        )
        self.rainfallFileCheckbox.stateChanged.connect(self.enableApply)
        
        self.rainfallFilenameEdit = QLineEdit("")
        self.rainfallFilenameEdit.setReadOnly(True)
        self.rainfallFilenameEdit.textChanged.connect(self.enableApply)
        rainfallFileDialogBtn = QPushButton("Select")
        rainfallFileDialogBtn.clicked.connect(lambda: self.openFileDialog(self.rainfallFile, self.rainfallFilenameEdit))
        self.respLabel = QLabel("responsiveness to rainfall")
        self.respLabel.setToolTip("Carrying capacity's responsiveness to rainfall contribution.")
        self.respSB = QDoubleSpinBox()
        self.respSB.setMinimum(0)
        self.respSB.setMaximum(10000)
        self.respSB.setValue(0)
        self.respSB.resize(self.respSB.sizeHint())
        self.respSB.valueChanged.connect(self.enableApply)
        self.rainfallFilenameEdit.hide()
        rainfallFileDialogBtn.hide()
        self.respLabel.hide()
        self.respSB.hide()
        
        line5 = QFrame()
        line5.setFrameShape(QFrame.HLine)
        line5.setPalette(pal)
        
        modelAreaTitle = QLabel("Model area")
        self.boundaryTypeLabel = QLabel("boundary type")
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
        self.gammaLabel = QLabel("resistance formation rate")
        self.gammaLabel.setToolTip("Rate of r2 allele formation from W/D meiosis.")
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
        self.relTimesFileLabel = QLabel("release times file")
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
        self.layout.addWidget(self.setLabelLabel, 1, 0)
        self.layout.addWidget(self.setLabelSB, 1, 1)
        self.layout.addWidget(self.recIntervalLocalLabel, 1, 2)
        self.layout.addWidget(self.recIntervalLocalSB, 1, 3)
        self.layout.addWidget(line1, 4, 0, 1, 4)
        self.layout.addWidget(lifeTitle, 5, 0)
        self.layout.addWidget(self.muJLabel, 6, 0)
        self.layout.addWidget(self.muJSB, 6, 1)
        self.layout.addWidget(self.muALabel, 6, 2)
        self.layout.addWidget(self.muASB, 6, 3)
        self.layout.addWidget(self.betaLabel, 7, 0)
        self.layout.addWidget(self.betaSB, 7, 1)
        self.layout.addWidget(self.thetaLabel, 7, 2)
        self.layout.addWidget(self.thetaSB, 7, 3)
        self.layout.addWidget(self.compPowerLabel, 8, 0)
        self.layout.addWidget(self.compPowerSB, 8, 1)
        self.layout.addWidget(self.minDevLabel, 8, 2)
        self.layout.addWidget(self.minDevSB, 8, 3)
        self.layout.addWidget(line2, 9, 0, 1, 4)
        self.layout.addWidget(dispTitle, 10, 0)
        self.layout.addWidget(self.dispRateLabel, 11, 0)
        self.layout.addWidget(self.dispRateSB, 11, 1)
        self.layout.addWidget(self.maxDispLabel, 11, 2)
        self.layout.addWidget(self.maxDispSB, 11, 3)
        self.layout.addWidget(self.dispTypeLabel, 12, 0)
        self.layout.addWidget(self.dispTypeCB, 12, 1, 1, 1)
        self.layout.addWidget(line3, 13, 0, 1, 4)
        self.layout.addWidget(self.aesTitle, 14, 0)
        self.layout.addWidget(self.aesCheckbox, 14, 1)
        self.layout.addWidget(self.psiLabel, 15, 0)
        self.layout.addWidget(self.psiSB, 15, 1)
        self.layout.addWidget(self.muAesLabel, 15, 2)
        self.layout.addWidget(self.muAesSB, 15, 3)
        self.layout.addWidget(self.tHide1Label, 16, 0)
        self.layout.addWidget(self.tHide1SB, 16, 1)
        self.layout.addWidget(self.tHide2Label, 16, 2)
        self.layout.addWidget(self.tHide2SB, 16, 3)
        self.layout.addWidget(self.tWake1Label, 17, 0)
        self.layout.addWidget(self.tWake1SB, 17, 1)
        self.layout.addWidget(self.tWake2Label, 17, 2)
        self.layout.addWidget(self.tWake2SB, 17, 3)
        self.layout.addWidget(line4, 18, 0, 1, 4)
        self.layout.addWidget(seasonalityTitle, 19, 0)
        self.layout.addWidget(self.alpha0MeanLabel, 20, 0)
        self.layout.addWidget(self.alpha0MeanSB, 20, 1)
        self.layout.addWidget(self.alpha0VarLabel, 20, 2)
        self.layout.addWidget(self.alpha0VarSB, 20, 3)
        self.layout.addWidget(self.alpha1Label, 21, 0)
        self.layout.addWidget(self.alpha1SB, 21, 1)
        self.layout.addWidget(self.ampLabel, 21, 2)
        self.layout.addWidget(self.ampSB, 21, 3)
        self.layout.addWidget(self.rainfallFileLabel, 22, 0)
        self.layout.addWidget(self.rainfallFileCheckbox, 22, 1)
        self.layout.addWidget(self.rainfallFilenameEdit, 23, 0, 1, 3)
        self.layout.addWidget(rainfallFileDialogBtn, 23, 3)
        self.layout.addWidget(self.respLabel, 24, 0)
        self.layout.addWidget(self.respSB, 24, 1)
        self.layout.addWidget(line5, 25, 0, 1, 4)
        self.layout.addWidget(modelAreaTitle, 26, 0)
        self.layout.addWidget(self.boundaryTypeLabel, 27, 0)
        self.layout.addWidget(self.boundaryTypeCB, 27, 1, 1, 1)
        self.layout.addWidget(self.coordsFileLabel, 28, 0)
        self.layout.addWidget(self.coordsFileCheckbox, 28, 1)
        self.layout.addWidget(self.coordsFilenameEdit, 29, 0, 1, 3)
        self.layout.addWidget(coordsFileDialogBtn, 29, 3)
        self.layout.addWidget(line6, 30, 0, 1, 4)
        self.layout.addWidget(inherTitle, 31, 0)
        self.layout.addWidget(self.gammaLabel, 32, 0)
        self.layout.addWidget(self.gammaSB, 32, 1)
        self.layout.addWidget(line7, 33, 0, 1, 4)
        self.layout.addWidget(releaseTitle, 34, 0)
        self.layout.addWidget(self.relTimesFileLabel, 35, 0)
        self.layout.addWidget(self.relTimesFileCheckbox, 35, 1)
        self.layout.addWidget(self.relTimesFilenameEdit, 36, 0, 1, 3)
        self.layout.addWidget(relTimesFileDialogBtn, 36, 3)
        self.layout.addWidget(line8, 37, 0, 1, 4)
        self.layout.addWidget(self.okBtn, 38, 2, 1, 1)
        self.layout.addWidget(self.applyBtn, 38, 3, 1, 1)
        
        self.horizontalGroupBox.setLayout(self.layout)
        
    def getParamsInfo(self):
        advSetInfo = AdvParams()
        advSetInfo.setLabel = (self.setLabelLabel.text(), self.setLabelLabel.toolTip())
        advSetInfo.recIntervalLocal = (self.recIntervalLocalLabel.text(), self.recIntervalLocalLabel.toolTip())
        advSetInfo.muJ = (self.muJLabel.text(), self.muJLabel.toolTip())
        advSetInfo.muA = (self.muALabel.text(), self.muALabel.toolTip())
        advSetInfo.beta = (self.betaLabel.text(), self.betaLabel.toolTip())
        advSetInfo.theta = (self.thetaLabel.text(), self.thetaLabel.toolTip())
        advSetInfo.compPower = (self.compPowerLabel.text(), self.compPowerLabel.toolTip())
        advSetInfo.minDev = (self.minDevLabel.text(), self.minDevLabel.toolTip())
        advSetInfo.dispRate = (self.dispRateLabel.text(), self.dispRateLabel.toolTip())
        advSetInfo.maxDisp = (self.maxDispLabel.text(), self.maxDispLabel.toolTip())
        advSetInfo.dispType = (self.dispTypeLabel.text(), "")
        advSetInfo.aestivation = (self.aesTitle.text(), "")
        advSetInfo.psi = (self.psiLabel.text(), self.psiLabel.toolTip())
        advSetInfo.muAes = (self.muAesLabel.text(), self.muAesLabel.toolTip())
        advSetInfo.tHide1 = (self.tHide1Label.text(), self.tHide1Label.toolTip())
        advSetInfo.tHide2 = (self.tHide2Label.text(), self.tHide2Label.toolTip())
        advSetInfo.tWake1 = (self.tWake1Label.text(), self.tWake1Label.toolTip())
        advSetInfo.tWake2 = (self.tWake2Label.text(), self.tWake2Label.toolTip())
        advSetInfo.alpha0Mean = (self.alpha0MeanLabel.text(), self.alpha0MeanLabel.toolTip())
        advSetInfo.alpha0Var = (self.alpha0VarLabel.text(), self.alpha0VarLabel.toolTip())
        advSetInfo.alpha1 = (self.alpha1Label.text(), self.alpha1Label.toolTip())
        advSetInfo.amp = (self.ampLabel.text(), self.ampLabel.toolTip())
        advSetInfo.rainfallFile = (self.rainfallFileLabel.text(), "")
        advSetInfo.resp = (self.respLabel.text(), self.respLabel.toolTip())
        advSetInfo.boundaryType = (self.boundaryTypeLabel.text(), self.boundaryTypeLabel.toolTip())
        advSetInfo.patchCoordsFile = (self.coordsFileLabel.text(), "")
        advSetInfo.gamma = (self.gammaLabel.text(), self.gammaLabel.toolTip())
        advSetInfo.relTimesFile = (self.relTimesFileLabel.text(), "")
    
        return advSetInfo
        
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
            if (self.tHide1SB.value() > maxT) or (self.tHide2SB.value() > maxT) or (self.tWake1SB.value() > maxT) or (self.tWake2SB.value() > maxT):
                errMsgs.append("The aestivation interval times are larger than max_t.\nThe simulation will only run partly through the aestivation period.")

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
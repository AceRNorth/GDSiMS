# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 14:39:54 2025

@author: biol0117
"""

from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QProgressBar, QStyle, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, QThread
from pathlib import Path
import os
from datetime import datetime
import sim
from progressreader import ProgressReader
import gdsimsgui

class WidgetRun(QWidget):
    """ Contains UI components for running and tracking a simulation. """
    
    def __init__(self, winWidget):
        """
        Parameters
        ----------
        winWidget : WindowWidget
        """
        super().__init__()
        self.winWidget = winWidget 
        self.simulation = None
        self.setLayout(QGridLayout())
        self.initUI()
        
    def initUI(self):
        """ Creates the UI components and places them. """
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
        self.msgBar = QLineEdit()
        self.msgBar.setText("Waiting for run.")
        self.msgBar.setReadOnly(True)
        self.msgBar.resize(self.msgBar.sizeHint())
        
        self.layout().setHorizontalSpacing(5)
        self.layout().addWidget(outputDirLabel, 0, 0)
        self.layout().addWidget(simNameLabel, 0, 5)
        self.layout().addWidget(self.outputDirNameEdit, 1, 0, 1, 4)
        self.layout().addWidget(outputDirDialogBtn, 1, 4)
        self.layout().addWidget(self.simNameEdit, 1, 5, 1, 3)
        self.layout().addWidget(self.progBar, 2, 0, 1, 6)
        self.layout().addWidget(self.runBtn, 2, 6, 1, 2)
        self.layout().addWidget(self.abortBtn, 2, 6, 1, 2)
        self.layout().addWidget(self.msgBar, 3, 0, 1, 8)
        
        
    def openDirDialog(self, dirNameEdit):
        """ Opens a directory dialog box to select the output directory. """
        dname = QFileDialog.getExistingDirectory(self, "Select an output directory", ".")
        if dname:
            outputDirName = Path(dname)
            dirNameEdit.setText(str(outputDirName))    
            
    def runSim(self):
        """ Sets up the simulation run on a separate thread."""
        areValidParams, errMsgs = self.winWidget.validParams()
        if not areValidParams:
            # pop-up with warning message
            errMsgs = "\n".join(errMsgs)
            QMessageBox.warning(self, "Invalid parameter(s)", errMsgs)
        else:
            validDir = self.createOutputDir(self.outputDirNameEdit.text(), self.simNameEdit.text())
            if validDir:
                self.winWidget.runStarted()
                customSet = self.winWidget.createParamsFiles(self.outputPath)
                
                # Set up progress bar
                self.progBar.setMinimum(0)
                self.progBar.setMaximum(customSet.numRuns * (customSet.maxT+1))
                self.progBar.reset()
                
                # Create simulation run thread
                self.simThread = QThread()
                self.simulation = sim.Simulation(self.outputPath,
                                             self.simName,
                                             customSet.dispType, 
                                             customSet.boundaryType,
                                             customSet.rainfallFile,
                                             customSet.coordsFile,
                                             customSet.relTimesFile
                                             )
                self.simulation.moveToThread(self.simThread)
                
                # Create progress reader thread
                self.progThread = QThread()
                outputFiles = [] 
                for i in range(1, customSet.numRuns + 1): # find filepaths to read for each run
                    filePath = os.path.join(self.outputPath, "output_files", "Totals{}run{}.txt").format(customSet.setLabel, i)
                    outputFiles.append(filePath)
                self.progReader = ProgressReader(outputFiles, customSet.maxT, customSet.numRuns)
                self.progReader.moveToThread(self.progThread)
                
                # Connect signals and slots
                self.simThread.started.connect(self.simulation.run)
                self.simulation.finished.connect(self.simThread.quit)
                self.simulation.finished.connect(self.simulation.deleteLater)
                self.simThread.finished.connect(self.simThread.deleteLater)
                self.simulation.error.connect(self.runError)
                
                self.progThread.started.connect(self.progReader.run)
                self.progReader.finished.connect(self.progThread.quit)
                self.progReader.finished.connect(self.progReader.deleteLater)
                self.progThread.finished.connect(self.progThread.deleteLater)
                self.progReader.progress.connect(lambda v: self.updateProg(v, customSet.maxT, customSet.numRuns))
        
                # Start threads
                self.abortCode = 0
                self.simThread.start()
                self.progThread.start()
                
                # Disable and hide run button while subprocess is running and enable abort button in its place
                self.runBtn.setEnabled(False)
                self.runBtn.hide()
                self.abortBtn.setEnabled(True)
                self.abortBtn.show()
                self.simThread.finished.connect(lambda: self.runFinished(self.abortCode))
        
                # Start the QTimer to read the output file periodically
                # self.timer = QTimer(self)
                # self.timer.timeout.connect(self.read_output_file)
                # self.timer.start(1000)  # Check for new output every 1 second
        
    def abortSim(self):
       """ Aborts the simulation run. """
       if self.simulation:
           self.msgBar.setText("Aborting simulation... Please wait.")
           QApplication.processEvents()
           self.progThread.quit()
           self.progThread.wait()
           self.abortCode = 1
           self.simulation.abort()
           self.simThread.quit()
           self.simThread.wait()
        
    def createOutputDir(self, dirPath, simName):
        """
        Creates a new directory for the simulation files in the selected directory path.
        If a simulation name is specified (not blank), the directory will have this name.
        Otherwise, a date-time stamp will be given.
        If the parent directory path is not given (blank), the parent directory will be taken as the base directory of the GUI file.

        Parameters
        ----------
        dirPath : string
            Absolute filepath for the parent directory of the simulation files.
        simName : string
            Name for the new subdirectory.

        Returns
        -------
        isValidDir : bool
            Whether the parent directory filepath is a valid directory.

        """
        isValidDir = True
        outputPath = Path()
        errMsgs = []
        if Path(dirPath).is_dir() or dirPath == "":
            if dirPath == "":
                dirPath = gdsimsgui.basedir
            
            if simName != "":
                outputPath = Path(dirPath) / Path(simName)
            else:
                dt = datetime.now()
                simName = str(dt.year) + "_" + str(dt.month) + "_" + "{:02d}".format(dt.day)
                simName +=  "_" + "{:02d}".format(dt.hour) + "{:02d}".format(dt.minute) + "{:02d}".format(dt.second)
                outputPath = Path(dirPath) / simName
            
            # check if the directory has already been used for simulations
            if not Path(outputPath / "params.txt").exists():
                self.outputPath = outputPath
                self.simName = simName
                if not self.outputPath.exists():
                    os.makedirs(self.outputPath)
            else:
                errMsgs.append("The selected simulation directory has already been used to run a simulation. Please select a different one.")
         
        else:
            errMsgs.append("The output directory path does not exist.")
            
        if len(errMsgs) != 0:  
            isValidDir = False
            errMsgs = "\n".join(errMsgs)
            QMessageBox.warning(self, "Warning", errMsgs)
        
        return isValidDir
        
    def runFinished(self, abortCode):
        """
        Updates UI upon finish of the simulation run.

        Parameters
        ----------
        abortCode : int
            Non-zero abort code means most recent simulation aborted.

        Returns
        -------
        None.

        """
        # Re-enable the button
        #self.timer.stop()
        self.abortBtn.setEnabled(False)
        self.abortBtn.hide()
        self.runBtn.show()
        self.runBtn.setEnabled(True)
        if abortCode == 0:
            self.msgBar.setText("Waiting for run.")
            self.winWidget.runFinished(self.outputPath)
            QMessageBox.information(self, "Info", "Simulation completed successfully!")
        else:
            self.progBar.reset()
            self.msgBar.setText("Waiting for run.")
            # no run finished for plots because don't want to access incomplete files
            QMessageBox.information(self, "Info", "Simulation aborted.")
        self.simulation = None
        
    def runError(self, errorMsg):
        """
        Aborts the simulation and displays the error message.

        Parameters
        ----------
        errorMsg : string
            Collection of concatenated error messages from the simulation.

        Returns
        -------
        None.

        """
        # Stop the timer and show the error
        #self.timer.stop()
        QMessageBox.critical(self, "Error", errorMsg)
        self.abortSim()
        
    def isSimRunning(self):
        """

        Returns
        -------
        bool
            Whether the simulation is still running.

        """
        if self.simulation != None:
            return True
        else:
            return False
        
    def updateProg(self, progValue, maxT, numRuns):
        self.progBar.setValue(progValue)
        curRun = int(progValue / (maxT + 1)) + 1
        if curRun <= numRuns:
            if progValue % (maxT + 1) == 0:
                self.msgBar.setText("Initialising simulation {} run {}/{}. Please wait.".format(self.simName, curRun, numRuns))
            else:
                curDay = progValue - ((curRun-1) * (maxT+1))
                self.msgBar.setText("Running simulation {} run {}/{} day {}/{}".format(self.simName, curRun, numRuns, curDay, maxT))
            
    def disableRunBtn(self):
        self.runBtn.setEnabled(False)
        
    def enableRunBtn(self):
        self.runBtn.setEnabled(True)
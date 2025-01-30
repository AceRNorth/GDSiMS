# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 14:39:54 2025

@author: biol0117
"""

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QProgressBar, QStyle, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, QThread
from pathlib import Path
import os
from datetime import datetime
import sim
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
        """ Sets up the simulation run on a separate thread."""
        validDir = self.createOutputDir(self.outputDirNameEdit.text(), self.simNameEdit.text())
        if validDir:
            self.progBar.setValue(0)
            self.winWidget.runStarted()
            customSet = self.winWidget.createParamsFile(self.outputPath)
            self.winWidget.copyAdvFiles(self.outputPath) # so have all files used saved in same sim run directory
            
            # Create simulation run thread
            self.thread = QThread()
            self.simulation = sim.Simulation(self.outputPath,
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
       """ Aborts the simulation run. """
       if self.simulation:
           self.abortCode = 1
           self.simulation.abort()
           self.thread.quit()
           self.thread.wait()
        
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
        isValidDir = False
        if Path(dirPath).is_dir() or dirPath == "":
            if dirPath == "":
                dirPath = gdsimsgui.basedir
            
            if simName != "":
                self.outputPath = Path(dirPath) / Path(simName)
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
            self.progBar.setValue(100)
            self.winWidget.runFinished(self.outputPath)
            QMessageBox.information(self, "Info", "Simulation completed successfully!")
        else:
            self.progBar.setValue(0)
            self.winWidget.runFinished(self.outputPath)
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
        
    def disableRunBtn(self):
        self.runBtn.setEnabled(False)
        
    def enableRunBtn(self):
        self.runBtn.setEnabled(True)
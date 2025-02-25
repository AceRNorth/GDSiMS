# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 14:14:15 2025

@author: biol0117
"""

from PyQt5.QtCore import QObject, pyqtSignal
import subprocess
import sys
import os
import gdsimsgui

class Simulation(QObject):
    """ Runs a simulation subprocess for secondary-thread execution. """
    finished = pyqtSignal()
    error = pyqtSignal(str)
    def __init__(self, outputPath, simName, dispType, boundaryType, rainfallFile, coordsFile, relTimesFile):
        """
        Parameters
        ----------
        outputPath : Path
            Output directory path.
        simName : string.
            Simulation run name for output subdirectory.
        dispType : string
            Dispersal type for simulation. Options: "Distance kernel", "Radial".
        boundaryType : string
            Boundary type for simulation. Options: "Toroid", "Edge".
        rainfallFile : string
            Absolute filepath of the rainfall file. Can be None. 
        coordsFile : string
            Absolute filepath of the coordinates file. Can be None.
        relTimesFile : string
            Absolute filepath of the release times file. Can be None.
        """
        super().__init__()
        
        self.exeFilepath = gdsimsgui.basedir / gdsimsgui.appname
        self.outputPath = outputPath
        self.simName = simName
        
        self.rainfallFile = rainfallFile
        self.coordsFile = coordsFile
        self.relTimesFile = relTimesFile
        self.dispType = dispType
        self.boundaryType = boundaryType
        
        self.process = None
    
    def run(self):
        """ Runs the simulation. """
        
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
        # Ensure process runs without creating a console window
        if sys.platform == "win32":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            self.process = subprocess.Popen(
                [self.exeFilepath],
                stdin = subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                startupinfo=startupinfo,
                creationflags=subprocess.CREATE_NO_WINDOW,
                text=True,
                env=env
            )
        else:
            self.process = subprocess.Popen(
                [self.exeFilepath],
                stdin = subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True,
                text=True,
                env=env
            )
        outs, errs = self.process.communicate(input=inputString)
        # check for errors whilst process is running and emit error signal
        # (can't use except because cerrs, not subprocess errs)
        if errs: 
            self.error.emit(errs)
            self.process.terminate()
            os.chdir(gdsimsgui.basedir)
        else: # don't let finished signal emit if have errors
            self.process.wait()
            self.finished.emit()
            os.chdir(gdsimsgui.basedir)
            
    def abort(self):
        """ Aborts the simulation. """
        if self.process:
            self.process.terminate()
            os.chdir(gdsimsgui.basedir)

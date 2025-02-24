# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 16:57:59 2025

@author: biol0117
"""

from PyQt5.QtCore import QObject, pyqtSignal, QTimer
import os


class ProgressReader(QObject):
    """ Monitors file progress in a separate thread. """
    progress = pyqtSignal(int)  # progress step value
    finished = pyqtSignal()  # Signal when tracking is done

    def __init__(self, files, maxT, numRuns):
        super().__init__()
        self.files = files
        self.maxT = maxT
        self.numRuns = numRuns
        self.totalSteps = numRuns * maxT
        self.running = True
        self.timer = QTimer(self)

    def run(self):
        for i in range(0, len(self.files)):
            self.running = True
            while self.running:
                if os.path.exists(self.files[i]):
                    with open(self.files[i], "r") as f:
                        lines = f.readlines()
                        if len(lines) <= 2:
                            progress = (i * (self.maxT+1)) # include initialisation day
                        else: 
                            progress = (i * (self.maxT+1)) + (len(lines) - 2) # subtract two header lines (but include initialisation day)
                        self.progress.emit(progress)
    
                        if (len(lines) - 3) >= self.maxT: # without two header lines and initialisation day
                            self.running = False
                            break
                self.timer.start(500)  # prevent excessive CPU usage
        self.finished.emit()
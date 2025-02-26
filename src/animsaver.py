# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 15:19:39 2025

@author: biol0117
"""

from PyQt5.QtCore import QObject, pyqtSignal

class AnimSaver(QObject):
    """ Saves an animation as a file."""
    finished = pyqtSignal()
    def __init__(self, fname, anim):
        """
        Parameters
        ----------
        fname : str
            Filepath for the output animation file.
        anim : matplotlib.animation.FuncAnimation
            Animation object to save to file.
        
        """
        super().__init__()
        self.filename = fname
        self.anim = anim
    
    def run(self):
        self.anim.save(filename=self.filename, writer="pillow")
        self.finished.emit()

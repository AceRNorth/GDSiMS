# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 15:19:39 2025

@author: biol0117
"""

from PyQt5.QtCore import QObject, pyqtSignal
import matplotlib.animation as animation

class AnimSaver(QObject):
    """ Creates an animation and saves the file."""
    finished = pyqtSignal()
    def __init__(self, fname, fig, func, numFrames, interval, coordsFile, localFile, recStart):
        """
        Parameters
        ----------
        fname : str
            Filepath for the output animation file.
        fig : matplotlib.Figure
            Figure on which to create the animation.
        func : function
            Updating function for the animation.
        numFrames : int
            Number of frames in the animation.
        interval : float
            Time interval between animation frames (in milliseconds).
        coordsFile : os.path
            Coordinates file for animation plotting.
        localFile : os.path
            Local data file for animation plotting.
        recStart : int
            Start time (in the simulation) for local data recording.
        """
        super().__init__()
        self.filename = fname
        self.fig = fig
        self.func = func
        self.numFrames = numFrames
        self.interval = interval
        self.coordsFile = coordsFile
        self.localFile = localFile
        self.recStart = recStart
    
    def run(self):
        anim = animation.FuncAnimation(fig=self.fig, func=self.func,
                                       fargs=(self.coordsFile, self.localFile, self.recStart),
                                       frames=self.numFrames, interval=self.interval, repeat=False)
        anim.save(filename=self.filename, writer="pillow")
        self.finished.emit()

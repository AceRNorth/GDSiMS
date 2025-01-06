# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 13:57:33 2025

@author: biol0117
"""

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from PyQt5.QtWidgets import QSizePolicy
import numpy as np

class PlotCanvas(FigureCanvas):
    """Creates a figure plot from a data file."""
    
    def __init__(self, parent=None, width=5, height=4, dpi=100, colorbar=False, annot=False):
        # tight layout makes sure the labels are not cut off in the canvas when they become bigger in replots
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111) # creates subplots
        if colorbar:
            mainCmap = ['aquamarine', 'mediumturquoise', 'darkcyan','steelblue', 'royalblue', 'mediumblue', 'slateblue', 'darkviolet', 'indigo', 'black']
            allColours = ['darkgray', 'lightgreen'] + mainCmap # add colours for no-population patch and wild-population patch
            self.cmap = mcolors.ListedColormap(allColours)
            bounds = [-2, -1, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
            self.cnorm = mcolors.BoundaryNorm(bounds, self.cmap.N)
            self.sm = plt.cm.ScalarMappable(cmap=self.cmap, norm=self.cnorm) # dummy scalar mappable for the colorbar
            self.sm.set_array([])  # Set to an empty array to avoid plotting data
            self.colorbar = self.fig.colorbar(self.sm, ax=self.axes)
            self.colorbar.set_label('Drive allele frequency', labelpad=-10) # reduce distance to colorbar label
            self.colorbar.ax.set_yticks([-2, -1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], labels=['no pop', 'wild', '0.0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0'])
            labels = self.colorbar.ax.get_yticklabels()
            labels[0].set_verticalalignment('bottom') # align first label text above the tick 
            labels[1].set_verticalalignment('bottom')
        
        if annot:
            self.annotation = self.fig.text(x=0.1, y=0.97, s='t = ')
        
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        self.mode = 'static'
        self.applyLayout()
        
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self) # allows figure to change size with window
 
    def applyLayout(self):
        if self.mode == 'static':
            self.fig.set_tight_layout(True)
        else:
            self.fig.set_tight_layout(False)
            self.axes.set_position([0.1, 0.1, 0.65, 0.85]) # fix axes position for animations
            self.colorbar.ax.set_position([0.80, 0.1, 0.04, 0.85])

    def setMode(self, mode):
        self.mode = mode
        self.applyLayout()
 
    def plot(self, file, *args): 
        self.axes.clear() # clears plot on the plot canvas before plotting the new curve(s)
        data = np.loadtxt(file, skiprows=2)
        x = data[:, 0]
        y_lines = data[:, 1:]
        for line in y_lines:  # keep same colours for same type of line
            self.axes.plot(x, line) 
        self.axes.set_xlabel("x")
        self.axes.set_ylabel("y")
        self.axes.legend() # creates a legend for each curve
        self.draw() # draws the curve(s) on the canvas
        
class TotalsPlotCanvas(PlotCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        super().__init__(parent, width, height, dpi)
         
    def plot(self, file, lines:list): # sets variables of function (have to be lists)
        self.axes.clear() # clears plot on the plot canvas before plotting the new curve(s)
        totals = np.loadtxt(file, skiprows=2)
        times = totals[100:, 0] - 100 # discard first 100 days and rescale day no. for (starts from day 0)
        total_males = totals[100:, 1:]
        for line in lines:  # keep same colours for same type of line
            lbl = ""
            col = "mediumturquoise"
            
            if line == 0:
                lbl = "$M_{WW}$"
                col = "mediumturquoise"
            elif line == 1:
                lbl = "$M_{WD}$"
                col = "darkcyan"
            elif line == 2:
                lbl = "$M_{DD}$"
                col = "royalblue"
            elif line == 3:
                lbl = "$M_{WR}$"
                col = "slategray"
            elif line == 4:
                lbl = "$M_{RR}$"
                col = "rebeccapurple"
            elif line == 5:
                lbl = "$M_{DR}$"
                col = "darkviolet"
            elif line == 6:
                lbl = "$M_{WW}$+$M_{WD}$+\n$M_{DD}$+$M_{WR}$+\n$M_{RR}$+$M_{DR}$"
                col = "black"
            elif line == 7:
                lbl = "$M_{WW}$+$M_{WD}$+\n$M_{WR}$"
                col = "hotpink"
            
            y = []
            if line == 6:
                y = np.sum(total_males, axis=1).tolist()
            if line == 7:
                y = np.sum(total_males[:, (0, 1, 3)], axis=1).tolist()
            if line >= 0 and line < 6:
                y = total_males[:, line]
            self.axes.plot(times, y, label=lbl, color=col) 
     
        self.axes.set_xlabel("Day")
        self.axes.set_ylabel("Total number of individuals")
        self.axes.legend() # creates a legend for each curve
        self.draw() # draws the curve(s) on the canvas
        
class CoordsPlotCanvas(PlotCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        super().__init__(parent, width, height, dpi)
    def plot(self, file, *args): 
        self.axes.clear() # clears plot on the plot canvas before plotting the new curve(s)
        data = np.loadtxt(file, skiprows=2)
        x = data[:, 1]
        y = data[:, 2]
        self.axes.scatter(x, y, marker='.', color="peru")
        self.axes.set_xlim(np.amin(x), np.amax(x))
        self.axes.set_ylim(np.amin(y), np.amax(y))
        self.axes.set_xlabel("x")
        self.axes.set_ylabel("y")
        self.draw() # draws the curve(s) on the canvas
        
class LocalPlotCanvas(PlotCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # have booleans so can still reuse PlotCanvas class for different cases
        super().__init__(parent, width, height, dpi, colorbar=True, annot=True) 
        self.scat = None
    def plot(self, coordsFile, localFile, t=0): 
        self.axes.clear() # clears plot on the plot canvas before plotting the new curve(s)
        
        ind, x, y = np.loadtxt(coordsFile, skiprows=2, unpack=True)
        localData = np.loadtxt(localFile, skiprows=2) # get populations
        self.simDay = int(localData[t*len(x), 0]) # get populations on one day
        localDataDay = localData[t*len(x):((t+1)*len(x)), 2:8]

        WW = localDataDay[:, 0]
        WD = localDataDay[:, 1]
        DD = localDataDay[:, 2]
        WR = localDataDay[:, 3]
        RR = localDataDay[:, 4]
        DR = localDataDay[:, 5]

        # calculate drive allele frequency for each patch
        driveFreq = np.zeros(len(x))
        for pat in range(0, len(x)):
            tot = WW[pat] + WD[pat] + DD[pat] + WR[pat] + RR[pat] + DR[pat]
            if tot == 0:
                driveFreq[pat] = -2 # assign different distinguishable value for no-population patches
            elif tot == WW[pat]:
                driveFreq[pat] = -0.5
            else:
                driveFreq[pat] = (WD[pat] + (2*DD[pat]) + DR[pat]) / (2*tot)

        # make a scatter plot with drive frequency colour map
        self.scat = self.axes.scatter(x, y, c=driveFreq, cmap=self.cmap, norm=self.cnorm, marker='.')
        self.annotation.set_text("t = {}".format(self.simDay))
        self.axes.set_xlabel("x")
        self.axes.set_ylabel("y")
        self.axes.set_xlim(np.amin(x), np.amax(x))
        self.axes.set_ylim(np.amin(y), np.amax(y))
        self.draw() # draws the curve(s) on the canvas        
        
        return self.scat
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
    """Creates a plot figure. """
    
    def __init__(self, parent=None, width=5, height=4, dpi=100, colorbar=False, annot=False):
        """
        Parameters
        ----------
        parent : TYPE, optional
            DESCRIPTION. The default is None.
        width : float, optional
            Figure width (inches). The default is 5.
        height : float, optional
            Figure height (inches). The default is 4.
        dpi : float, optional
            Figure dpi (resolution in dots-per-inch). The default is 100.
        colorbar : bool, optional
            Whether a colorbar is needed. The default is False.
        annot : bool, optional
            Whether a timestamp annotation is needed. The default is False.
        """
        # tight layout makes sure the labels are not cut off in the canvas when they become bigger in replots
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111) # creates subplots
        self.colorbar = None
        self.annotation = None
        
        # for local - drive allele freq plots
        if colorbar:
            mainCmap = ['aquamarine', 'mediumturquoise', 'darkcyan','steelblue', 'royalblue', 'mediumblue', 'slateblue', 'darkviolet', 'indigo', 'black']
            allColours = ['darkgray', 'lightgreen'] + mainCmap # add colours for no-population patch and wild-population patch
            self.cmap = mcolors.ListedColormap(allColours)
            bounds = [-2, -1, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
            self.cnorm = mcolors.BoundaryNorm(bounds, self.cmap.N)
            self.sm = plt.cm.ScalarMappable(cmap=self.cmap, norm=self.cnorm) # dummy scalar mappable for the colorbar
            self.sm.set_array([])  # set to an empty array to avoid plotting data
            self.colorbar = self.fig.colorbar(self.sm, ax=self.axes)
            self.colorbar.set_label('Drive allele frequency', labelpad=-10) # reduce distance to colorbar label
            self.colorbar.ax.set_yticks([-2, -1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                labels=['no pop', 'wild', '0.0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0'])
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
        """ 
        Sets the layout for the figure depending on the mode. 
        """
        if self.mode == 'static':
            self.fig.set_tight_layout(True)
        else:
            self.fig.set_tight_layout(False)
            self.axes.set_position([0.1, 0.1, 0.65, 0.85]) # fix axes position for animations
            if self.colorbar != None:
                self.colorbar.ax.set_position([0.80, 0.1, 0.04, 0.85])

    def setMode(self, mode):
        """  
        Sets the mode of the canvas. 
        Mode setting enables the use of the same canvas for static figures and animations. 
        
        Parameters
        ----------
        mode : string. options: "static", "animation"
        
        Returns
        -------
        None.

        """
        self.mode = mode
        self.applyLayout()
 
    def plot(self, file, *args): 
        """
        Plots curves on the canvas from the data files.

        Parameters
        ----------
        file : os.path for data file
        *args : 

        Returns
        -------
        None.

        """
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
    """ Creates a plot figure of total males across the simulation area, classed by genotype. """
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        """
        Parameters
        ----------
        parent : TYPE, optional
            DESCRIPTION. The default is None.
        width : float, optional
            Figure width (inches). The default is 5.
        height : float, optional
            Figure height (inches). The default is 4.
        dpi : float, optional
            Figure dpi (resolution in dots-per-inch). The default is 100.
        """
        super().__init__(parent, width, height, dpi)
         
    def plot(self, file, lines:list): # sets variables of function (have to be lists)
        """
        Plots the selected lines on the canvas from the data file.

        Parameters
        ----------
        file : os.path for totals data file
        lines : list of the selected lines

        Returns
        -------
        None.
        """
    
        self.axes.clear() # clears plot on the plot canvas before plotting the new curve(s)
        totals = np.loadtxt(file, skiprows=2)
        times = totals[365:, 0] - 365 # discard first 365 days and rescale day no. for (starts from day 0)
        total_males = totals[365:, 1:]
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
        self.axes.legend() 
        self.draw() # draws the curve(s) on the canvas
        
class CoordsPlotCanvas(PlotCanvas):
    """ Creates a plot figure of coordinate points. """
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        """
        Parameters
        ----------
        parent : TYPE, optional
            DESCRIPTION. The default is None.
        width : float, optional
            Figure width (inches). The default is 5.
        height : float, optional
            Figure height (inches). The default is 4.
        dpi : float, optional
            Figure dpi (resolution in dots-per-inch). The default is 100.
        """
        super().__init__(parent, width, height, dpi)
    def plot(self, file, *args): 
        """
        Scatter plots the points from the data file.

        Parameters
        ----------
        file : os.path for coords data file
        *args :

        Returns
        -------
        None.
        """
        self.axes.clear() 
        data = np.loadtxt(file, skiprows=2)
        x = data[:, 1]
        y = data[:, 2]
        self.axes.scatter(x, y, marker='.', color="peru")
        self.axes.set_xlim(np.amin(x), np.amax(x))
        self.axes.set_ylim(np.amin(y), np.amax(y))
        self.axes.set_xlabel("x")
        self.axes.set_ylabel("y")
        self.draw()
        
        
class LocalPlotCanvas(PlotCanvas):
    """ Creates a plot and animation figure of local male population data. """
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        """
        Parameters
        ----------
        parent : TYPE, optional
            DESCRIPTION. The default is None.
        width : float, optional
            Figure width (inches). The default is 5.
        height : float, optional
            Figure height (inches). The default is 4.
        dpi : float, optional
            Figure dpi (resolution in dots-per-inch). The default is 100.
        """
        # have booleans so can still reuse PlotCanvas class for different cases
        super().__init__(parent, width, height, dpi, colorbar=True, annot=True) 
        self.scat = None
    def plot(self, coordsFile, localFile, t, recStart): 
        """
        Scatter plots the points from the coords data file with a color map of the drive allele frequency.

        Parameters
        ----------
        coordsFile : os.path for coords data file
        localFile : os.path for local data file
        t : int, timestep (starting from 0, index of data row on local file)
        recStart: int, start time for recording local data

        Returns
        -------
        scat : matplotlib.collections.PathCollection (scatter points)
        """
        self.axes.clear() 
        ind, x, y = np.loadtxt(coordsFile, skiprows=2, unpack=True)
        numRecPats = len(x) # number of recorded patches in one day  --  num_pat / rec_sites_freq ??
        #print("t:", t)
        #print("numRecPats:", numRecPats)
        localData = np.loadtxt(localFile, skiprows=2) # get populations 
        recIntervalLocal = int(localData[2*numRecPats, 0]) - int(localData[1*numRecPats, 0])
        #print("Local data:", localData)
        #localData = localData[365:, :] # slicing from 365th row allows old timestep indexing going forwards
        self.simDay = int(localData[(t+1)*numRecPats, 0]) # get populations on one day, t+1 because always ignore initialisation day
        #print("simDay:", self.simDay)
        localDataDay = localData[t*numRecPats:((t+2)*numRecPats), 2:8]

        WW = localDataDay[:, 0]
        WD = localDataDay[:, 1]
        DD = localDataDay[:, 2]
        WR = localDataDay[:, 3]
        RR = localDataDay[:, 4]
        DR = localDataDay[:, 5]

        # calculate drive allele frequency for each patch
        driveFreq = np.zeros(numRecPats)
        for pat in range(0, numRecPats):
            tot = WW[pat] + WD[pat] + DD[pat] + WR[pat] + RR[pat] + DR[pat]
            if tot == 0:
                driveFreq[pat] = -2 # assign different distinguishable value for no-population patches
            elif tot == WW[pat]:
                driveFreq[pat] = -0.5
            else:
                driveFreq[pat] = (WD[pat] + (2*DD[pat]) + DR[pat]) / (2*tot)

        # make a scatter plot with drive frequency colour map
        self.scat = self.axes.scatter(x, y, c=driveFreq, cmap=self.cmap, norm=self.cnorm, marker='.')
        # discarded days have already not been locally recorded (due to internal rescaling of recStart) but still need to rescale sim day value
        self.annotation.set_text("t = {}".format((t * recIntervalLocal) + recStart))
        self.axes.set_xlabel("x")
        self.axes.set_ylabel("y")
        self.axes.set_xlim(np.amin(x), np.amax(x))
        self.axes.set_ylim(np.amin(y), np.amax(y))
        self.draw()      
        
        return self.scat
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 15:08:05 2025

@author: biol0117
"""

class InputParams():
    """ Input parameters for the simulation, including the boundary and dispersal types and the advanced parameter filepaths."""
    def __init__(self, numRuns, maxT, numPat, muJ, muA, beta, theta, compPower, minDev, gamma, xi, e, driverStart, numDriverM,
                 numDriverSites, dispRate, maxDisp, psi, muAes, tHide1, tHide2, tWake1, tWake2, alpha0Mean, alpha0Variance, alpha1,
                 amp, resp, recStart, recEnd, recIntervalGlobal, recIntervalLocal, recSitesFreq, setLabel, dispType, boundaryType,
                 rainfallFile, coordsFile, relTimesFile):
        """
        Parameters
        ----------
        numRuns : int
            Number of simulation replicates to run.
        maxT : int
            Maximum simulated time (in days).
        numPat : int
            Number of population sites chosen for the simulation.
        muJ : float
            Juvenile density independent mortality rate per day.
        muA : float
            Adult mortality rate per day.
        beta : float
            Parameter that controls mating rate.
        theta : float
            Average egg laying rate of wildtype females (eggs per day).
        compPower : float
            Parameter that controls the juvenile survival probability.
        minDev : int
            Minimum development time for a juvenile (in days).
        gamma : float
            Rate of r2 allele formation from W/D meiosis.
        xi : float
            Somatic Cas9 expression fitness cost.
        e : float
            Homing rate in females.
        driverStart : int
            Time to start releasing drive alleles into the mosquito population.
        numDriverM : int
            Number of drive heterozygous (WD) male mosquitoes per release.
        numDriverSites : int
            Number of gene drive release sites per year.
        dispRate : float
            Adult dispersal rate.
        maxDisp : float
            Maximum dispersal distance at which two sites are connected.
        psi : float
            Aestivation rate.
        muAes : float
            Aestivation mortality rate.
        tHide1 : int
            Start day of aestivation-hiding period (exclusive).
        tHide2 : int
            End day of aestivation-hiding period (inclusive).
        tWake1 : int
            Start day of aestivation-waking period (exclusive).
        tWake2 : int
            End day of aestivation-waking period (inclusive).
        alpha0Mean : float
            Mean of the baseline contribution to the carrying capacity.
        alpha0Variance : float
            Variance of the baseline contribution to the carrying capacity.
        alpha1 : float
            Rainfall contribution factor to carrying capacity.
        amp : float
            Amplitude of rainfall fluctuations.
        resp : float
            Carrying capacity's responsiveness to rainfall contribution.
        recStart : int
            Start time for the data recording window (inclusive).
        recEnd : int
            End time for the data recording window (inclusive).
        recIntervalGlobal : int
            Time interval for global data recording/output.
        recIntervalLocal : int
            Time interval at which to collect/record local data (in days).
        recSitesFreq : int
            Fraction of sites to collect local data for (1 is all sites, 10 is 1 in 10 etc).
        setLabel : int
            'Set of repetitions' index label for output files.
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
        
        self.numRuns = numRuns
       	self.maxT = maxT
       	self.numPat = numPat
       	self.muJ = muJ
       	self.muA = muA
       	self.beta = beta
       	self.theta = theta
       	self.compPower = compPower
       	self.minDev = minDev
        self.gamma = gamma
       	self.xi = xi
       	self.e = e
        self.driverStart = driverStart
       	self.numDriverM = numDriverM
       	self.numDriverSites = numDriverSites
        self.dispRate = dispRate
       	self.maxDisp = maxDisp
       	self.psi = psi
       	self.muAes = muAes
       	self.tHide1 = tHide1
       	self.tHide2 = tHide2
       	self.tWake1 = tWake1
       	self.tWake2 = tWake2
        self.alpha0Mean = alpha0Mean
        self.alpha0Variance = alpha0Variance
        self.alpha1 = alpha1
        self.amp = amp
        self.resp = resp
       	self.recStart = recStart
       	self.recEnd = recEnd
        self.recIntervalGlobal = recIntervalGlobal
       	self.recIntervalLocal = recIntervalLocal
       	self.recSitesFreq = recSitesFreq
       	self.setLabel = setLabel
        self.dispType = dispType
        self.boundaryType = boundaryType
        self.rainfallFile = rainfallFile
        self.coordsFile = coordsFile
        self.relTimesFile = relTimesFile
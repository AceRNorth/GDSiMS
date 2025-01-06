# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 15:08:05 2025

@author: biol0117
"""

class InputParams():
    def __init__(self, numRuns, maxT, numPat, muJ, muA, beta, theta, compPower, minDev, gamma, xi, e, driverStart, numDriverM,
                 numDriverSites, dispRate, maxDisp, psi, muAes, tHide1, tHide2, tWake1, tWake2, alpha0Mean, alpha0Variance, alpha1,
                 amp, resp, recStart, recEnd, recIntervalGlobal, recIntervalLocal, recSitesFreq, setLabel, dispType, boundaryType,
                 rainfallFile, coordsFile, relTimesFile):
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
            
class AdvParams():
    setLabel = 1
    recIntervalGlobal = 1
    recStart = 0
    recEnd = 1000
    recIntervalLocal = 200
    recSitesFreq = 1
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
       
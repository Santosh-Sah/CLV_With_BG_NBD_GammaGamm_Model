# -*- coding: utf-8 -*-
"""
Created on Sun May 10 10:40:18 2020

@author: Santosh Sah
"""
import pylab
from lifetimes.plotting import plot_frequency_recency_matrix
from lifetimes.plotting import plot_probability_alive_matrix
from lifetimes.plotting import plot_period_transactions

def visualizeFrequencyRecencyMatrix(betaGeoFitterModel):
    
    plot_frequency_recency_matrix(betaGeoFitterModel)
    
    pylab.savefig("FrequencyRecencyMatrixPlot.png")

def visualizeProbabilityAliveMatrix(betaGeoFitterModel):
    
    plot_probability_alive_matrix(betaGeoFitterModel)
    
    pylab.savefig("ProbabilityAliveMatrixPlot.png")

def visualizePlotPeriodTransaction(betaGeoFitterModel):
    
    plot_period_transactions(betaGeoFitterModel)
    
    pylab.savefig("PeriodTransactionPlot.png")
    
    
    
    

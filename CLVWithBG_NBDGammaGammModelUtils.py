# -*- coding: utf-8 -*-
"""
Created on Sun May 10 10:37:48 2020

@author: Santosh Sah
"""

import pandas as pd
import pickle
from lifetimes.utils import summary_data_from_transaction_data
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter

def importCLVWithBG_NBDGammaGammModelDataset(clvWithBG_NBDGammaGammModelDatasetFileName):
    
    #read dataset from csv files
    clvWithBG_NBDGammaGammModelDataset = pd.read_csv(clvWithBG_NBDGammaGammModelDatasetFileName,encoding = "cp1252")
    
    #remove time from date
    clvWithBG_NBDGammaGammModelDataset["InvoiceDate"] = pd.to_datetime(clvWithBG_NBDGammaGammModelDataset["InvoiceDate"], format = "%d-%m-%Y %H:%M").dt.date
    
    #our analysis is based on the customer and hence removing missing customer id from analysis.
    clvWithBG_NBDGammaGammModelDataset = clvWithBG_NBDGammaGammModelDataset[pd.notnull(clvWithBG_NBDGammaGammModelDataset["CustomerID"])]
    
    #taking only non-negative quantity
    clvWithBG_NBDGammaGammModelDataset = clvWithBG_NBDGammaGammModelDataset[(clvWithBG_NBDGammaGammModelDataset["Quantity"] > 0)]
    
    #adding new columns total_sales
    clvWithBG_NBDGammaGammModelDataset["Total_Sales"] = clvWithBG_NBDGammaGammModelDataset["Quantity"] * clvWithBG_NBDGammaGammModelDataset["Price"]
    
    #necessary columns
    clvWithBG_NBDGammaGammModelNecessaryColumns = ["CustomerID","InvoiceDate", "Total_Sales"]
    
    #taking necessary columns
    clvWithBG_NBDGammaGammModelDataset = clvWithBG_NBDGammaGammModelDataset[clvWithBG_NBDGammaGammModelNecessaryColumns]
    
    
    return clvWithBG_NBDGammaGammModelDataset

#Built-in utility functions from lifetimes package to transform the transactional data (one row per purchase) 
#into summary data (a frequency, recency, age and monetary).
def summaryDataFromTransactionData(clvWithBG_NBDGammaGammModelProcessedDataset):
    
    summaryDataFromTransactionDataForCLV = summary_data_from_transaction_data(clvWithBG_NBDGammaGammModelProcessedDataset,
                                       "CustomerID", "InvoiceDate", 
                                       monetary_value_col = "Total_Sales",
                                       observation_period_end = "2011-12-9")
    
    return summaryDataFromTransactionDataForCLV
    

"""
save CLVWithBG_NBDGammaGammModelProcessedDataset as a pickle file
"""

def saveCLVWithBG_NBDGammaGammModelProcessedDataset(clvWithBG_NBDGammaGammModelProcessedDataset):
    
    #Write CLVWithBG_NBDGammaGammModelProcessedDataset in a picke file
    with open("CLVWithBG_NBDGammaGammModelProcessedDataset.pkl",'wb') as clvWithBG_NBDGammaGammModelProcessedDataset_Pickle:
        pickle.dump(clvWithBG_NBDGammaGammModelProcessedDataset, clvWithBG_NBDGammaGammModelProcessedDataset_Pickle, protocol = 2)

"""
read CLVWithBG_NBDGammaGammModelProcessedDataset from pickle file
"""
def readCLVWithBG_NBDGammaGammModelProcessedDataset():
    
    #load CLVWithBG_NBDGammaGammModelProcessedDataset
    with open("CLVWithBG_NBDGammaGammModelProcessedDataset.pkl","rb") as clvWithBG_NBDGammaGammModelProcessedDataset_pickle:
        clvWithBG_NBDGammaGammModelProcessedDataset = pickle.load(clvWithBG_NBDGammaGammModelProcessedDataset_pickle)
    
    return clvWithBG_NBDGammaGammModelProcessedDataset

"""
save SummaryDataFromTransactionDataForCLV as a pickle file
"""

def saveSummaryDataFromTransactionDataForCLV(summaryDataFromTransactionDataForCLV):
    
    #Write SummaryDataFromTransactionDataForCLV in a picke file
    with open("SummaryDataFromTransactionDataForCLV.pkl",'wb') as summaryDataFromTransactionDataForCLV_Pickle:
        pickle.dump(summaryDataFromTransactionDataForCLV, summaryDataFromTransactionDataForCLV_Pickle, protocol = 2)

"""
read SummaryDataFromTransactionDataForCLV from pickle file
"""
def readsummaryDataFromTransactionDataForCLV():
    
    #load SummaryDataFromTransactionDataForCLV
    with open("SummaryDataFromTransactionDataForCLV.pkl","rb") as summaryDataFromTransactionDataForCLV_pickle:
        summaryDataFromTransactionDataForCLV = pickle.load(summaryDataFromTransactionDataForCLV_pickle)
    
    return summaryDataFromTransactionDataForCLV

"""
save BetaGeoFitterModel as a pickle file
"""

def saveBetaGeoFitterModel(betaGeoFitterModel):
    
    #Write BetaGeoFitterModel in a picke file
    betaGeoFitterModel.save_model("BetaGeoFitterModel.pkl")

"""
read BetaGeoFitterModel from pickle file
"""
def readBetaGeoFitterModel():
    
    betaGeoFitterModel = BetaGeoFitter()
    
    betaGeoFitterModel.load_model("BetaGeoFitterModel.pkl")
    
    return betaGeoFitterModel

"""
save GammaGammaFitterModel as a pickle file
"""

def saveGammaGammaFitterModel(gammaGammaFitterModel):
    
    #Write BetaGeoFitterModel in a picke file
    gammaGammaFitterModel.save_model("GammaGammaFitterModel.pkl")

"""
read GammaGammaFitterModel from pickle file
"""
def readGammaGammaFitterModel():
    
    gammaGammaFitterModel = GammaGammaFitter()
    
    gammaGammaFitterModel.load_model("GammaGammaFitterModel.pkl")
    
    return gammaGammaFitterModel

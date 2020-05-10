# -*- coding: utf-8 -*-
"""
Created on Sun May 10 10:39:18 2020

@author: Santosh Sah
"""
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter

from CLVWithBG_NBDGammaGammModelUtils import (saveBetaGeoFitterModel, readsummaryDataFromTransactionDataForCLV, 
                                              readBetaGeoFitterModel, saveGammaGammaFitterModel, readGammaGammaFitterModel)

from CLVWithBG_NBDGammaGammModelVisualization import (visualizeFrequencyRecencyMatrix, visualizeProbabilityAliveMatrix, visualizePlotPeriodTransaction)

"""
Train AutoRegressionForecastingMethod model on training set
"""
def trainBetaGeoFitterModel():
    
    summaryDataFromTransactionDataForCLV = readsummaryDataFromTransactionDataForCLV()
    
    #training model
    betaGeoFitterModel = BetaGeoFitter(penalizer_coef=0.0)
    
    betaGeoFitterModel.fit(summaryDataFromTransactionDataForCLV["frequency"], summaryDataFromTransactionDataForCLV["recency"],
                           summaryDataFromTransactionDataForCLV["T"])
    
    #saving the model in pickle file
    saveBetaGeoFitterModel(betaGeoFitterModel)
    
    print(betaGeoFitterModel.summary)
    
# =============================================================================
#                     coef   se(coef)  lower 95% bound  upper 95% bound
#     r       0.826433   0.026780         0.773944         0.878922
#     alpha  68.890678   2.611055        63.773011        74.008345
#     a       0.003443   0.010347        -0.016837         0.023722
#     b       6.749363  22.412933       -37.179985        50.678711
# 
# =============================================================================
    
def plotFrequencyRecencyMatrix():
    
    betaGeoFitterModel = readBetaGeoFitterModel()
    
    #visualizing relationship between frequency and recency using a matrix or with a heat map
    #imagine there is a customer who puchase everday for eight weeks and after that he did not purchase any thing for a month.
    #what are the chances that he is still alive, chance will be pretty small.
    #imaginethere is a customer who purchase every month and lastly he purchased last month. what is the chances that he is alive. High chances.
    #These king of relationship we can visulize with the help of frequency recency matrix.
    #it calculates expected number of transaction a customer make in a particualar period based on its recency value that age of its last purchase and 
    #frequency vlaue that is number of repeate transactions.
    #analyze the map and we can figure out that there is a customer who made 120 purchases and his latest purchase was when he is 350 old, he is considered
    #our best customers. They are present at bottom right corner.
    #customer who purchase frequntly but we have not seen him for a week he is oldest and not good customers. They are present at top right corner.
    #we can also figure out a tail between 20 and 250. This represents the customerwho purchase infrequentlyand we have seen them recently.
    #They might buy again. These are customer to whom we are not sure thatthey are dead or in between purchases. 
    visualizeFrequencyRecencyMatrix(betaGeoFitterModel)

def plotProbabilityAliveMatrix():
    
    betaGeoFitterModel = readBetaGeoFitterModel()
    
    #creating a matrix for the probability customer being alive.
    #analyze the map and we can figure out that there is a customer who made 120 purchases and his latest purchase was when he is 350 old, he is considered
    #our best customers. They are present at bottom right corner. These customers are still alive.
    visualizeProbabilityAliveMatrix(betaGeoFitterModel)
    
def assessmentOfModelFitWithPlotPeriodTransaction():
    
    betaGeoFitterModel = readBetaGeoFitterModel()
    
    visualizePlotPeriodTransaction(betaGeoFitterModel)
    
def relationBetweenPurchaseValueFrequency():
    
    #gamma gamma model has an assumption that there is no relationship between purchase value and the frequency.
    #let find out the correlation between them.
    summaryDataFromTransactionDataForCLV = readsummaryDataFromTransactionDataForCLV()
    
    print(summaryDataFromTransactionDataForCLV[["monetary_value", "frequency"]].corr())
    
    #the value or correlation is near to zero means both have no relation.
# =============================================================================
#                     monetary_value  frequency
#     monetary_value        1.000000   0.046161
#     frequency             0.046161   1.000000
# =============================================================================

def trainGammaGammaModel():
    
    summaryDataFromTransactionDataForCLV = readsummaryDataFromTransactionDataForCLV()
    
    #getting those customers who have done at least one transaction with the company
    shortlistedCustomers = summaryDataFromTransactionDataForCLV[summaryDataFromTransactionDataForCLV["frequency"] > 0]
    
    gammaGammaFitterModel = GammaGammaFitter(penalizer_coef=0.0)
    
    gammaGammaFitterModel.fit(shortlistedCustomers["frequency"], shortlistedCustomers["monetary_value"])
    
    saveGammaGammaFitterModel(gammaGammaFitterModel)
    
def conditionalExpectedAverageProfit():
    
    gammaGammaFitterModel = readGammaGammaFitterModel()
    
    summaryDataFromTransactionDataForCLV = readsummaryDataFromTransactionDataForCLV()
    
    summaryDataFromTransactionDataForCLV["pred_txn_value"] = round(gammaGammaFitterModel.conditional_expected_average_profit(summaryDataFromTransactionDataForCLV["frequency"],
                                                                                                      summaryDataFromTransactionDataForCLV["monetary_value"]),2)
    
    print(summaryDataFromTransactionDataForCLV.head(10))
    
# =============================================================================
#                 frequency  recency      T  monetary_value  pred_txn_value
#     CustomerID
#     12346.0           0.0      0.0  325.0        0.000000          416.92
#     12347.0           6.0    365.0  367.0      599.701667          569.99
#     12348.0           3.0    283.0  358.0      301.480000          333.76
#     12349.0           0.0      0.0   18.0        0.000000          416.92
#     12350.0           0.0      0.0  310.0        0.000000          416.92
#     12352.0           6.0    260.0  296.0      368.256667          376.17
#     12353.0           0.0      0.0  204.0        0.000000          416.92
#     12354.0           0.0      0.0  232.0        0.000000          416.92
#     12355.0           0.0      0.0  214.0        0.000000          416.92
#     12356.0           2.0    303.0  325.0      269.905000          324.01
# =============================================================================

def customerLifeTimeValue():
    
    gammaGammaFitterModel = readGammaGammaFitterModel()
    
    betaGeoFitterModel = readBetaGeoFitterModel()
    
    summaryDataFromTransactionDataForCLV = readsummaryDataFromTransactionDataForCLV()
    
    #calculate customerlife time value
    summaryDataFromTransactionDataForCLV["CLV"] = round(gammaGammaFitterModel.customer_lifetime_value(betaGeoFitterModel,
                                        summaryDataFromTransactionDataForCLV["frequency"],
                                        summaryDataFromTransactionDataForCLV["recency"],
                                        summaryDataFromTransactionDataForCLV["T"],
                                        summaryDataFromTransactionDataForCLV["monetary_value"],
                                        time = 12, discount_rate=0.01),2)
    
    print(summaryDataFromTransactionDataForCLV.sort_values(by = "CLV",ascending = False).head(10).reset_index())
    
# =============================================================================
#        CustomerID  frequency  recency      T  monetary_value        CLV
#     0     14646.0       44.0    353.0  354.0     6366.705909  222128.66
#     1     18102.0       25.0    367.0  367.0     9349.477200  178894.94
#     2     16446.0        1.0    205.0  205.0   168469.600000  175526.63
#     3     17450.0       26.0    359.0  367.0     7404.690385  147476.32
#     4     14096.0       16.0     97.0  101.0     4071.434375  127588.81
#     5     14911.0      131.0    372.0  373.0     1093.661679  109442.10
#     6     12415.0       15.0    313.0  337.0     7860.210000   96289.89
#     7     14156.0       42.0    362.0  371.0     2787.081667   89410.23
#     8     17511.0       27.0    371.0  373.0     3305.060741   67660.28
#     9     16029.0       38.0    335.0  373.0     2034.808421   58729.55
# =============================================================================
    
    
if __name__ == "__main__":
    #trainBetaGeoFitterModel()
    #plotFrequencyRecencyMatrix()
    #plotProbabilityAliveMatrix()
    #assessmentOfModelFitWithPlotPeriodTransaction()
    #relationBetweenPurchaseValueFrequency()
    #trainGammaGammaModel()
    #conditionalExpectedAverageProfit()
    customerLifeTimeValue()
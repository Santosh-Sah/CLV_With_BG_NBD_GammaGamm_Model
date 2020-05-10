# -*- coding: utf-8 -*-
"""
Created on Sun May 10 10:40:04 2020

@author: Santosh Sah
"""

from CLVWithBG_NBDGammaGammModelUtils import (importCLVWithBG_NBDGammaGammModelDataset, saveCLVWithBG_NBDGammaGammModelProcessedDataset,
                                              saveSummaryDataFromTransactionDataForCLV, readCLVWithBG_NBDGammaGammModelProcessedDataset,
                                              summaryDataFromTransactionData)


def preprocess():
    
    clvWithBG_NBDGammaGammModelDataset = importCLVWithBG_NBDGammaGammModelDataset("CustomerOnlineRetail.csv")
    
# =============================================================================
#     print(clvWithBG_NBDGammaGammModelDataset.head(10))
#     
#            CustomerID InvoiceDate  Total_Sales
#     0     17850.0  2010-12-01        15.30
#     1     17850.0  2010-12-01        20.34
#     2     17850.0  2010-12-01        22.00
#     3     17850.0  2010-12-01        20.34
#     4     17850.0  2010-12-01        20.34
#     5     17850.0  2010-12-01        15.30
#     6     17850.0  2010-12-01        25.50
#     7     17850.0  2010-12-01        11.10
#     8     17850.0  2010-12-01        11.10
#     9     13047.0  2010-12-01        25.50
# =============================================================================
    
    #getting the last order date
    last_order_date = clvWithBG_NBDGammaGammModelDataset["InvoiceDate"].max()
    
    print(last_order_date) #2011-12-09
    
    
    #saving processed dataset 
    saveCLVWithBG_NBDGammaGammModelProcessedDataset(clvWithBG_NBDGammaGammModelDataset)

def summaryDataFromTransactionDataForCLV():
    
    #reading the processed dataset
    clvWithBG_NBDGammaGammModelProcessedDataset = readCLVWithBG_NBDGammaGammModelProcessedDataset()
    
    #transforming the transaction dat, one row per purchase.
    summaryDataFromTransactionDataForCLV = summaryDataFromTransactionData(clvWithBG_NBDGammaGammModelProcessedDataset)
    
    #saving the processed dataset which has frequency, recency and monetary information
    saveSummaryDataFromTransactionDataForCLV(summaryDataFromTransactionDataForCLV)
    
    print(summaryDataFromTransactionDataForCLV.reset_index().head())
    
# =============================================================================
#            CustomerID  frequency  recency      T  monetary_value
#     0     12346.0        0.0      0.0  325.0        0.000000
#     1     12347.0        6.0    365.0  367.0      599.701667
#     2     12348.0        3.0    283.0  358.0      301.480000
#     3     12349.0        0.0      0.0   18.0        0.000000
#     4     12350.0        0.0      0.0  310.0        0.000000
# =============================================================================   
    
if __name__ == "__main__":
    #preprocess()
    summaryDataFromTransactionDataForCLV()
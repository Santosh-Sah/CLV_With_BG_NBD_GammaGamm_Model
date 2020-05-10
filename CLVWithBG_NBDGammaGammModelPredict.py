# -*- coding: utf-8 -*-
"""
Created on Sun May 10 10:39:46 2020

@author: Santosh Sah
"""

from CLVWithBG_NBDGammaGammModelUtils import (readsummaryDataFromTransactionDataForCLV, readBetaGeoFitterModel)


def predictTheFutureTransaction():
    
    #Predict future transaction in next 10 days i.e.top 10 customers that the model expects them to make purchases 
    #in the next 10 days, based on historical data
    
    summaryDataFromTransactionDataForCLV = readsummaryDataFromTransactionDataForCLV()
    
    betaGeoFitterModel = readBetaGeoFitterModel()
    
    futurePeriod = 10
    
    summaryDataFromTransactionDataForCLV["pred_num_txn"] = round(betaGeoFitterModel.conditional_expected_number_of_purchases_up_to_time(futurePeriod,
                                        summaryDataFromTransactionDataForCLV['frequency'], 
                                        summaryDataFromTransactionDataForCLV['recency'], 
                                        summaryDataFromTransactionDataForCLV['T']), 2)
    
    print(summaryDataFromTransactionDataForCLV.sort_values(by = "pred_num_txn",ascending = False).head(10).reset_index())

    
# =============================================================================
#            CustomerID  frequency  recency      T  monetary_value  pred_num_txn
#     0     14911.0      131.0    372.0  373.0     1093.661679          2.98
#     1     12748.0      113.0    373.0  373.0      298.360885          2.58
#     2     17841.0      111.0    372.0  373.0      364.452162          2.53
#     3     15311.0       89.0    373.0  373.0      677.729438          2.03
#     4     14606.0       88.0    372.0  373.0      135.890114          2.01
#     5     12971.0       70.0    369.0  372.0      159.211286          1.61
#     6     13089.0       65.0    367.0  369.0      893.714308          1.50
#     7     14527.0       53.0    367.0  369.0      155.016415          1.23
#     8     13798.0       52.0    371.0  372.0      706.650962          1.20
#     9     16422.0       47.0    352.0  369.0      702.472340          1.09
# =============================================================================
    
def predictTheFutureTransactionOfSingleCustomer():
        
    summaryDataFromTransactionDataForCLV = readsummaryDataFromTransactionDataForCLV()
        
    #individualCustomer = summaryDataFromTransactionDataForCLV[summaryDataFromTransactionDataForCLV["CustomerID"] == "14911"]
    
    individualCustomer = summaryDataFromTransactionDataForCLV.loc[14911]
        
    betaGeoFitterModel = readBetaGeoFitterModel()
        
    futurePeriod = 10
        
    predictedValue = betaGeoFitterModel.predict(futurePeriod,
                                   individualCustomer['frequency'], 
                                   individualCustomer['recency'], 
                                   individualCustomer['T'])
        
    print(predictedValue) #2.9830238639029005
    
if __name__ == "__main__":
    #predictTheFutureTransaction()
    predictTheFutureTransactionOfSingleCustomer()
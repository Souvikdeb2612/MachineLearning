# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 23:29:53 2020

@author: USER
"""

import pandas as pd 
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt


df_tr = pd.read_excel (r'Updated_dataset.xlsx', sheet_name='Transactions')
df_nc = pd.read_excel (r'Updated_dataset.xlsx', sheet_name='NewCustomerList')
df_cd = pd.read_excel (r'Updated_dataset.xlsx', sheet_name='CustomerDemographic')
df_ca = pd.read_excel (r'Updated_dataset.xlsx', sheet_name='CustomerAddress')

#df_tr.describe()
#df_cd.columns

rfm_data=df_tr[['customer_id','transaction_date','Profit']]


rfm_data['transaction_date'] = pd.to_datetime(rfm_data['transaction_date'])



#For Monetary, Calculate sum of purchase price for each customer

#rfm_data.groupby(['customer_id']).groups.keys()
#rfm_data.groupby(['customer_id']).first()
df_profit=rfm_data.groupby(['customer_id'])['Profit'].sum()


#For Frequency, Calculate the number of orders for each customer
df_l=df_tr.groupby(['customer_id'])['customer_id'].count().reset_index(drop=True)
df_l=pd.DataFrame(df_l)
df_profit=df_profit.reset_index()
df_profit=df_profit.merge(df_l, left_index=True, right_index=True, how='outer')

#For Recency, Calculate the number of days between present date and
# date of last purchase each customer

df_recency=rfm_data.groupby(['customer_id'])['transaction_date'].max()
df_recency=df_recency.reset_index()
PRESENT = dt.date.today()
df_recency.transaction_date= pd.to_datetime(df_recency.transaction_date) 
PRESENT=pd.to_datetime(PRESENT)

df_recency.transaction_date=(PRESENT-df_recency.transaction_date)
df_recency.transaction_date=df_recency.transaction_date.astype(str)
df_recency.transaction_date = df_recency.transaction_date.apply(lambda x: int(x.split(' ')[0]))
df_recency.transaction_date=df_recency.transaction_date.astype(int)

rfm=df_profit.merge(df_recency['transaction_date'], left_index=True, right_index=True, how='outer')

#Form the RFM dataframe to analyse further
rfm = rfm.rename(columns = {'customer_id_x': 'CustomerID', 'Profit': 'Monetary','customer_id_y': 'Frequency','transaction_date': 'Recency'}, inplace = False)

#Calculate RFM score
rfm['M'] = pd.qcut(rfm['Monetary'], 4, ['1','2','3','4'])
rfm['F'] = pd.qcut(rfm['Frequency'], 4, ['1','2','3','4'])
rfm['R'] = pd.qcut(rfm['Recency'], 4, ['4','3','2','1'])

rfm['RFM_Segment'] = rfm.R.astype(str)+ rfm.F.astype(str) + rfm.M.astype(str)
rfm.R=rfm.R.astype(int)
rfm.F=rfm.F.astype(int)
rfm.M=rfm.M.astype(int)
rfm['RFM_Score'] = rfm[['R','F','M']].sum(axis=1)
print(rfm['RFM_Score'].unique())
print(rfm['RFM_Segment'].unique())


# Define rfm_level function
def rfm_level(rfm):
    if (rfm['RFM_Segment'] >= 434 or (rfm['RFM_Score'] >= 9)) :
        return 'Platinum customers'
    elif ((rfm['RFM_Score'] >= 8) and (rfm['M'] == 4)):
        return 'Champions Big Spenders'
    elif ((rfm['RFM_Score'] >= 6) and (rfm['F'] >= 2)):
        return 'Loyal Customers'
    elif ((rfm['RFM_Segment'] >= 221) or (rfm['RFM_Score'] >= 6)):
        return 'Potential Loyalists'
    elif (((rfm['RFM_Segment'] >= 121) and (rfm['R'] == 1)) or rfm['RFM_Score'] == 5):
        return 'Needs Attention'
    elif ((rfm['RFM_Score'] >= 4) and (rfm['R'] == 1)):
        return 'Hibernating customers'
    else:
        return 'Lost Customers'
    
# Define rfm_level function
def rfm_action(df):
    if (df['RFM_Segment'] >= 434 or (df['RFM_Score'] >= 9)) :
        return 'No Price Incentives; Offer Limited edition and Loyality programs'
    elif ((df['RFM_Score'] >= 8) and (df['M'] == 4)):
        return 'Upsell most expensive items'
    elif ((df['RFM_Score'] >= 6) and (df['F'] >= 2)):
        return 'Loyality programs;Cross Sell'
    elif ((df['RFM_Segment'] >= 221) or (df['RFM_Score'] >= 6)):
        return 'Cross Sell Recommendations and Discount coupons'
    elif (((df['RFM_Segment'] >= 121) and (df['R'] == 1)) or df['RFM_Score'] == 5):
        return 'Price incentives and Limited time offer'
    elif ((df['RFM_Score'] >= 4) and (df['R'] == 1)):
        return 'Aggressive price incentives'
    else:
        return 'Don\'t spend too much trying to re-acquire'
    
    
# Create a new variable RFM_Level
rfm['RFM_Segment'] = rfm.RFM_Segment.apply(lambda x: int(x))
rfm['Customer Segment'] = rfm.apply(rfm_level, axis=1)
# Create a new variable RFM_Level
rfm['Marketing Action'] = rfm.apply(rfm_action, axis=1)


# Calculate average values for each Customer Segment, and return a size of each segment 
rfm_level_agg = rfm.groupby('Customer Segment').agg({
    'Recency': 'mean',
    'Frequency': 'mean',
    'Monetary': ['mean', 'count'],
    'Marketing Action': 'unique'
}).round(1)
# Print the aggregated dataset
print(rfm_level_agg)

rfm_level_ag = pd.DataFrame(rfm_level_agg)
rfm_level_ag = rfm_level_ag.reset_index()
rfm_level_ag







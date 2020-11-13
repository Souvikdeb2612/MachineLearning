# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 12:56:13 2020

@author: USER
"""

import pandas as pd 
import datetime as dt


df_tr = pd.read_excel (r'KPMG_VI_New_raw_data_update_final.xlsx', sheet_name='Transactions')
df_nc = pd.read_excel (r'KPMG_VI_New_raw_data_update_final.xlsx', sheet_name='NewCustomerList')
df_cd = pd.read_excel (r'KPMG_VI_New_raw_data_update_final.xlsx', sheet_name='CustomerDemographic')
df_ca = pd.read_excel (r'KPMG_VI_New_raw_data_update_final.xlsx', sheet_name='CustomerAddress')

df_tr.Profit = df_tr.list_price - df_tr.standard_cost

age = pd.to_datetime(df_nc.DOB)

def from_dob_to_age(born):
    today = dt.date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
#age column for new customers 
age = age.apply(lambda x: from_dob_to_age(x))
df_nc.insert(5, "Age", age, True)

age = pd.to_datetime(df_cd.DOB)

#age column for old customers
age = age.apply(lambda x: from_dob_to_age(x))
df_cd.insert(6, "Age", age, True)
    

    
bins= [0,10,20,30,40,50,60,70,80,90]
labels = ['0-10','10-20','20-30','30-40','40-50','50-60','60-70','70-80','80+']  
df_nc['AgeGroup'] = pd.cut(df_nc['Age'], bins=bins, labels=labels, right=False)
df_cd['AgeGroup'] = pd.cut(df_cd['Age'], bins=bins, labels=labels, right=False)

with pd.ExcelWriter('Updated_dataset.xlsx') as writer:
    df_tr.to_excel(writer, sheet_name='Transactions')
    df_nc.to_excel(writer, sheet_name='NewCustomerList')
    df_cd.to_excel(writer, sheet_name='CustomerDemographic')
    df_ca.to_excel(writer, sheet_name='CustomerAddress')



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
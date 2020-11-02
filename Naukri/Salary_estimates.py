# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 12:59:27 2020

@author: USER
"""
#Importing the libraries
import pandas as pd


df = pd.read_csv('naukri_jobs.csv')

#CLEANING THE DATA 

#Parsing Job salary
df['Job Salary'] = df['Job Salary'].astype(str)
df.sort_values(['Job Salary'], axis=0, 
                 ascending=True, inplace=True)

df['Job Salary'] = df['Job Salary'].apply(lambda x: x.lower().replace('not disclosed by recruiter', 'nan').replace('openings: 1', 'nan').replace('no bar for right candidate', 'nan').replace('salary based on %', 'nan').replace('not disclosed', 'nan').replace(' ', '').replace('12000/-to18000/-monthly+incentive', 'nan').replace('20-25%hikeonthecurrentctc', 'nan').replace('1cr&above', 'nan'))
df['Salary'] = df['Job Salary'].apply(lambda x: 0 if 'nan' in x.lower() else 1)
df['highfen'] = df['Job Salary'].apply(lambda x: 0 if '-' in x.lower() else 1)
df = df.set_index('Salary')
df = df.drop(0, axis=0)
#df = df.reset_index('Salary')
df = df.set_index('highfen')
df = df.drop(1, axis=0)
#df = df.reset_index('highfen')
df = df[18:-1296]
df = df.reset_index(drop = True)

salary = df['Job Salary'].apply(lambda x: x.split('p')[0])
minus_comma = salary.apply(lambda x: x.replace(',', ''))

df['min_salary'] = minus_comma.apply(lambda x: int(x.split('-')[0]))
df['max_salary'] = minus_comma.apply(lambda x: int(x.split('-')[1]))
df['avg_salary'] = (df['min_salary'] + df['max_salary'])/2
df['avg_salary'] = df['avg_salary'].astype('int64')
print(df['max_salary'].dtype)
print(df['avg_salary'].dtype)


#pd.options.display.float_format = '{: .2f}'.format
df['avg_salary'] = df['avg_salary'].map('{:.0f}'.format)

#Remove unique ID and Timestamp
df = df.drop(['Uniq Id', 'Crawl Timestamp'], axis=1)

#parsing experience required
Experience_Required = df['Job Experience Required'].apply(lambda x: x.lower().replace('yrs', ''))
df['min_experience'] = Experience_Required.apply(lambda x: int(x.split('-')[0]))
df['max_experience'] = Experience_Required.apply(lambda x: int(x.split('-')[1]))

#parsing Job description
#df['Key Skills'] = df['Key Skills'].astype(str)
#df['python_yn'] = df['Key Skills'].apply(lambda x: 1 if 'python' in x.lower() else 0)
#print(df.python_yn.value_counts())

df.to_csv('Naukri_cleaned.csv')













# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 12:59:27 2020

@author: USER
"""
#Importing the libraries
import pandas as pd
import re


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
df['min_salary'] = df['min_salary']/10000
df['max_salary'] = minus_comma.apply(lambda x: int(x.split('-')[1]))
df['max_salary'] = df['max_salary']/10000
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
#print(df.Role.value_counts())

#parsing Location
df['Location'] = df['Location'].apply(lambda x: x.replace('(', ','))
df['Location'] = df['Location'].apply(lambda x: x.split(',')[0])
#print(df.Location.value_counts()) 

#parsing Functional Area
df['Functional Area'] = df['Functional Area'].apply(lambda x: x.replace('-', ',').replace('/', ','))
df['Functional Area'] = df['Functional Area'].apply(lambda x: x.split(',')[0])

#parsing Industry
df['Industry'] = df['Industry'].apply(lambda x: x.replace('-', ',').replace('/', ','))
df['Industry'] = df['Industry'].apply(lambda x: x.split(',')[0])

#parsing Role Category
df['Role Category'] = df['Role Category'].astype(str)
df['Role Category'] = df['Role Category'].apply(lambda x: x.replace('-', ',').replace('/', ','))
df['Role Category'] = df['Role Category'].apply(lambda x: x.split(',')[0])

#parsing Key Skills
df['Key Skills'] = df['Key Skills'].astype(str)
df['Key Skills'] = df['Key Skills'].apply(lambda x: x.replace('|', '').replace('.', '').replace('#', '').replace('nan', 'empty'))
print(df['Key Skills'].dtype)

#letters_only = re.sub('[^a-zA-Z]',' ', str(location))

def Clean_skills(Skill_name): 
    # Search for opening bracket in the name followed by 
    # any characters repeated any number of times 
    if re.search('\(.*', Skill_name): 
  
        # Extract the position of beginning of pattern 
        pos = re.search('\(.*', Skill_name).start() 
  
        # return the cleaned name 
        return Skill_name[:pos] 
  
    else: 
        # if clean up needed return the same name 
        return Skill_name 
    
df['Key Skills'] = df['Key Skills'].apply(Clean_skills)
df.to_csv('Naukri_cleaned.csv', index= False)













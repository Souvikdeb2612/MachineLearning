# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 14:04:17 2020

@author: USER
"""
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('Naukri_cleaned.csv')


#selecting relevant columns

print(df.columns)
df_model = df[['avg_salary', 'Location', 'Industry', 'Role']]

#creating dummy variables
df_dum = pd.get_dummies(df_model)

#train test split
from sklearn.model_selection import train_test_split
X = df_dum.drop('avg_salary', axis = 1)
y = df_dum['avg_salary'].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

'''
#multiple linear regression
import statsmodels.api as sm
X_sm = X.iloc[0:20,0:5] = sm.add_constant(X)
model = sm.OLS(y, X_sm)
model.fit().summary()
'''

from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import cross_val_score
 
lm = LinearRegression()
lm.fit(X_train, y_train)

np.mean(cross_val_score(lm, X_train, y_train, scoring = 'neg_mean_absolute_error', cv =5))

#Lasso regression 
lml = Lasso(alpha=0.01)
lml.fit(X_train, y_train)
np.mean(cross_val_score(lml, X_train, y_train, scoring = 'neg_mean_absolute_error', cv =5))

alpha=[]
error=[]
for i in range(1, 100):
    alpha.append(i/100)
    lm_l = Lasso(alpha =(i/100))
    error.append(np.mean(cross_val_score(lm_l, X_train, y_train, scoring = 'neg_mean_absolute_error', cv =5)))
    
plt.plot(alpha, error)
    
err =tuple(zip(alpha, error))
df_err = pd.DataFrame(err, columns = ['alpha', 'error'])
df_err[df_err.error == max(df_err.error)]

# Random Forest Regression
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor()
np.mean(cross_val_score(rf, X_train, y_train,scoring = 'neg_mean_absolute_error', cv =5))

#Grid Search
from sklearn.model_selection import GridSearchCV
parameters = {'n_estimators':range(10,300,10), 'criterion':('mse','mae'), 'max_features':('auto','sqrt')}
gs = GridSearchCV(rf, parameters, scoring = 'neg_mean_absolute_error', cv =5, verbose= 10)
gs.fit(X_train, y_train)

gs.best_score_
gs.best_estimator_

# test ensembles 
tpred_lm = lm.predict(X_test)
tpred_lml = lml.predict(X_test)
tpred_rf = gs.best_estimator_.predict(X_test)

from sklearn.metrics import mean_absolute_error
mean_absolute_error(y_test,tpred_lm)
mean_absolute_error(y_test,tpred_lml)
mean_absolute_error(y_test,tpred_rf)

mean_absolute_error(y_test,(tpred_lm+tpred_rf)/2)










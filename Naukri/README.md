# Naukri Jobs Salary Estimator: Project Overview

Created a tool that estimates Job salaries posted in Naukri website (MSE ~ 26K) to help people negotiate their income when they get a job.
Downloaded the raw dataset from Kaggle.
Optimized Linear, Lasso, and Random Forest Regressors using GridsearchCV to reach the best model.
Built a client facing API using flask

# Code and Resources Used

Python Version: 3.7
Packages: pandas, numpy, sklearn, matplotlib, seaborn, selenium, flask, json, pickle

For Web Framework Requirements: pip install -r requirements.txt

Dataset: https://www.kaggle.com/souvikdeb/naukri

Flask Productionization: https://towardsdatascience.com/productionize-a-machine-learning-model-with-flask-and-heroku-8201260503d2


# Data Cleaning

After downloading the data, I needed to clean it up so that it was usable for our model. I made the following changes and created the following variables:

Parsed numeric data out of salary
Removed rows without salary
Made a new column for average salary
Droped irrelavant colums like crawl timestamps and Uniq ID
Parsed the location, Functional Area, Role category, Industry columns.
Parsed out punctuations and symbols from Key Skills column.
Made separarte columns for minimum and maximum experience required.

# EDA
I looked at the distributions of the data and the value counts for the various categorical variables. Below are a few highlights from the pivot tables.
![alt text](https://github.com/Souvikdeb2612/ML/Naukri/blob/master/image.png?raw=true)

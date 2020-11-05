# Naukri Jobs Salary Estimator: Project Overview

* Created a tool that estimates Job salaries posted in Naukri website (MSE ~ 26K) to help people negotiate their income when they get a job.    
* Downloaded the raw dataset from Kaggle.    
* Optimized Linear, Lasso, and Random Forest Regressors using GridsearchCV to reach the best model.    
* Built a client facing API using flask.    
  
___

# Code and Resources Used

Python Version: 3.7
Packages: pandas, numpy, sklearn, matplotlib, seaborn, selenium, flask, json, pickle  
For Web Framework Requirements: pip install -r requirements.txt  
Dataset: https://www.kaggle.com/souvikdeb/naukri  
Flask Productionization: https://towardsdatascience.com/productionize-a-machine-learning-model-with-flask-and-heroku-8201260503d2  

___


# Data Cleaning

After downloading the data, I needed to clean it up so that it was usable for our model. I made the following changes and created the following variables:

Parsed numeric data out of salary.   
Removed rows without salary.   
Made a new column for average salary.   
Droped irrelavant colums like crawl timestamps and Uniq ID.   
Parsed the location, Functional Area, Role category, Industry columns.  
Parsed out punctuations and symbols from Key Skills column.  
Made separarte columns for minimum and maximum experience required.  
___

# EDA
I looked at the distributions of the data and the value counts for the various categorical variables. Below are a few highlights from the pivot tables.  

![alt text](https://github.com/Souvikdeb2612/ML/blob/master/Naukri/Locations.png?raw=true)  

![alt text](https://github.com/Souvikdeb2612/ML/blob/master/Naukri/Wordcloud.png?raw=true)  
___

# Model Building
First, I transformed the categorical variables into dummy variables. I also split the data into train and tests sets with a test size of 20%.  

I tried three different models and evaluated them using Mean Square Error. I chose MSE because it is relatively easy to interpret.

I tried three different models:  

Multiple Linear Regression – Baseline for the model  
Lasso Regression – Because of the sparse data from the many categorical variables, I thought a normalized regression like lasso would be effective.  
Random Forest – Again, with the sparsity associated with the data, I thought that this would be a good fit.  

# Model performance
The Random Forest model far outperformed the other approaches on the test and validation sets.  

Random Forest : MSE = 26.22    
Lasso Regression: MSE = 29.67  

# Productionization
In this step, I built a flask API endpoint that was hosted on a local webserver by following along with the TDS tutorial in the reference section above. The API endpoint takes in a request with a list of values from a job listing and returns an estimated salary.

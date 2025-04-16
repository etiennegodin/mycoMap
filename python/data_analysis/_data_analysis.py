import numpy as np 
import pandas as pd
import statsmodels.api as sm
import seaborn as sns

import matplotlib.pyplot as plt

# https://chatgpt.com/c/67842692-c814-800d-aa2f-627792370f2d

def lnr_reg(df, x, y):

    # Features (X) and target (y)
    X = df[x].values
    Y = df[y].values
    # Add a constant term for the intercept
    X_with_const = sm.add_constant(X)

    # Fit the linear regression model
    results = sm.OLS(Y, X_with_const).fit()

    # Print the results summary
    #print(results.summary())

    print(results.rsquared)
    print(results.f_pvalue)
    # Predictions
    df["predicted_frequency"] = results.predict(X_with_const)

    return df


def exploratory_data_analysis(df):
    print('')
    print('--------------------------------------------------------------')
    print('Exploratory Data Analysis')
    print('')

    df.shape

    print(df.describe())
    print(df.dtypes)

    #sns.pairplot(df)
    #plt.show()

    '''

    logistic regression if feed with other random data points without occurence
    presence, abscence
    same number as real occurence 

    Y = df['Salary]
    # get dependant variable 
    # in my case count , (occurence)
    # poisson ????

    #_-------------------------

    logistic regression if feed with other random data points without occurence
    same number as real occurence 
    '''

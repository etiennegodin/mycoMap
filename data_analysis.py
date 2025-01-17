import numpy as np 
import pandas as pd
import statsmodels.api as sm
import seaborn as sns

import matplotlib.pyplot as plt

# https://chatgpt.com/c/67842692-c814-800d-aa2f-627792370f2d

def lnr_reg(df, key, plot = False):

    # Features (X) and target (y)
    X = df[key].values
    y = df["count"].values
    # Add a constant term for the intercept
    X_with_const = sm.add_constant(X)

    # Fit the linear regression model
    model = sm.OLS(y, X_with_const).fit()

    # Print the model summary
    print(model.summary())

    # Predictions
    df["predicted_frequency"] = model.predict(X_with_const)

    # Plot the data and regression line
    plt.scatter(df[key], df["count"], color='blue', label='Actual data')
    plt.plot(df[key], df["predicted_frequency"], color='red', label='Regression line')
    plt.xlabel(key)
    plt.ylabel('Count')
    plt.title('Linear Regression: {} vs Frequency'.format(key))
    plt.legend()

    if plot == True:
        plt.show()

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

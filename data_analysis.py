
import pandas as pd 
import tools
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm


#https://medium.com/analytics-vidhya/implementing-linear-regression-using-sklearn-76264a3c073c

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



# https://www.geeksforgeeks.org/dependent-and-independent-variable/


#perform occurence stats based on value

#eventually help predicting where said specie can be found based on geo data points and env factors

# Whole other module 
# weather

#Ex: validate expected relationships hypothesis

    # 1. find relationship between tree composition and mycorrizhal certain specie (expected)
        # "Ectomycorrhizal species richness was mainly affected by stand characteristics."

    # 2. find relationship between tree diversity and sapotrophic species (expected)


#starts simple on densite

#linear regression on one factor
#best Fit Line

# Import geodata as dataframe
#df = pd.read_csv(file)
# Convert tree_cover columns to dict (read as string by pd.read_csv)
#df = tools.convert_tree_cover_data_type(df)


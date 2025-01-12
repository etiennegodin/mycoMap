
import pandas as pd 
import tools
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

file = 'data/gbifQueries/Cantharellus_enelensis/Cantharellus_enelensis_geodata.csv'

df = pd.read_csv(file)

df = tools.convert_tree_cover_data_type(df)

def richnessIndex(tree_cover):


    print(tree_cover)
    #indice de ricnesse (nb especes)
    n = len(tree_cover)
    return(n)

def shannonIndex(tree_cover):
    #indice shannon 
    #creer liste proportions d'essence
    proportions_list = []
    for key in tree_cover:
        #print(key)
        proportions_list.append(tree_cover[key])

    #numpy array
    proportions = np.array(proportions_list)

    try:
        # Vérifiez que la somme des proportions est égale à 1 (100%)
        if not np.isclose(np.sum(proportions), 1.0):
            raise ValueError("Les proportions des espèces doivent totaliser 1")
        
        # Calculez l'indice de Shannon
        shannon_index = -np.sum(proportions * np.log(proportions))
        
    except ValueError:
        # En cas d'erreur, attribuez la valeur 0 à l'indice de Shannon
        shannon_index = 0
        
    shannon_index = -np.sum(proportions * np.log(proportions))

    # Entropy 
    # SUm of surprise for each of elements
    return(shannon_index)


def interpret_tree_cover(df):
    df['richness_index'] = df['tree_cover'].apply(richnessIndex) 
    df['shannon_index'] = df['tree_cover'].apply(shannonIndex)

    return df 

def lnr_reg(df, parameter, plot = False):

    df = df[parameter]

    value_counts = df.value_counts().reset_index()
    value_counts.columns = ["value", "frequency"]

    # Sort by value
    value_counts = value_counts.sort_values("value")
    print(value_counts)


    # Features (X) and target (y)
    X = value_counts["value"].values
    y = value_counts["frequency"].values


    # Add a constant term for the intercept
    X_with_const = sm.add_constant(X)

    print(X_with_const)

    # Fit the linear regression model
    model = sm.OLS(y, X_with_const)
    results = model.fit()

    intercept, slope = results.params


    # Print the model summary
    print(results.summary())

    value_counts["predicted_frequency"] = results.predict(X_with_const)
    print(value_counts)

    # Plot the data and regression line
    plt.scatter(value_counts["value"], value_counts["frequency"], color='blue', label='Actual data')
    plt.plot(value_counts["value"], value_counts["predicted_frequency"], color='red', label='Regression line')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Linear Regression: Value vs Frequency')
    plt.legend()
    if plot == True:
        plt.show()


df = interpret_tree_cover(df)

lnr_reg(df, 'richness_index', plot = True)



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



def lnr_reg(df, parameter):

    df = df[parameter]

    value_counts = df.value_counts().reset_index()
    value_counts.columns = ["value", "frequency"]

    # Sort by value
    value_counts = value_counts.sort_values("value")
    print(value_counts)


    # Features (X) and target (y)
    X = value_counts["value"].values
    y = value_counts["frequency"].values


    # Add a constant term for the intercept
    X_with_const = sm.add_constant(X)

    print(X_with_const)

    # Fit the linear regression model
    model = sm.OLS(y, X_with_const)
    results = model.fit()

    intercept, slope = results.params


    # Print the model summary
    print(results.summary())

    value_counts["predicted_frequency"] = results.predict(X_with_const)
    print(value_counts)

    # Plot the data and regression line
    plt.scatter(value_counts["value"], value_counts["frequency"], color='blue', label='Actual data')
    plt.plot(value_counts["value"], value_counts["predicted_frequency"], color='red', label='Regression line')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Linear Regression: Value vs Frequency')
    plt.legend()
    #plt.show()

    #Line = x  value_counts["value"]
    # y = value_counts["predicted_frequency"]
    


# https://chatgpt.com/c/677b5036-d09c-800d-94db-d194a41724dc

# 


# We utilize the cost function to compute the best values ???

#Assume there is a linear relationship between X and Y




#multi factor linear regression ??




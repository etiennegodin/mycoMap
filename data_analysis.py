import numpy as np 
import pandas as pd
import statsmodels.api as sm
import seaborn as sns


import matplotlib.pyplot as plt
from tools import random_number_generator

# https://chatgpt.com/c/67842692-c814-800d-aa2f-627792370f2d


geodata_dictionnary = pd.read_csv('data/geodata_dictionnary.csv', header = 0 )

encoding_dictionnary = { 'cl_pent':
                        {
                            'A' : 1,
                            'B' : 2,
                            'C' : 3,
                            'D' : 4,
                            'E' : 5,
                            'F' : 6
                        },

                        'cl_drai' : 10,
                        'densite' : 10,
                        'cl_age_et': 
                        {
                            '10' : 10,
                            '30' : 30,
                            '50' : 50,
                            '70' : 70,
                            '90' : 90,
                            '110' : 110,
                            '120' : 120,
                            '130' : 130,
                            'VIN' : 40, # 30 a 50
                            'JIN' : 95 # 70 a 120
                        }

}


def dep_sur_map_category(value):
    if value.startswith('1'):
        return 'Depot Glaciaire'
    elif value.startswith('2'):
        return 'Depot fluvio-glaciaire'
    elif value.startswith('3'):
        return 'Depot fluviatile'
    elif value.startswith('4'):
        return 'Depot lacustre'
    elif value.startswith('5'):
        return 'Depot marin'
    elif value.startswith('6'):
        return 'Depot litoral marin'
    elif value.startswith('7'):
        return 'Depot organique'
    elif value.startswith('8'):
        return 'Depot de pente'
    elif value.startswith('9'):
        return 'Depot eolien'
    elif value.startswith('R'):
        return 'Rocheux'
    else:
        return 'Autre depot'

def encode_categorical_data(df, collumn, show = False):

    if collumn == 'dep_sur':

        df[collumn] = df[collumn].apply(dep_sur_map_category)


         # Count per value 
        value_counts = df[collumn].value_counts().reset_index()
        value_counts = value_counts.sort_values(collumn)

    return value_counts

def encode_ordinal_data(df, collumn, encoding):

    # Assign numerical values on ordinal values based on encoding
    df[collumn] = df[collumn].map(encoding)

    # Count per value
    value_counts = df[collumn].value_counts().reset_index()

    if collumn == 'cl_age_et':
        #Specific case for age where VIN and JIN represent range of age 
        #Creating random number between range with count as size
        #print(value_counts)
        #print('')

        jin_count = df[collumn].value_counts().get('JIN', 0)
        vin_count = df[collumn].value_counts().get('VIN', 0)
        # Custom code for age to remap JIN & VIN

        #Create dataframe with random vales for JIN
        rand_jin = pd.DataFrame({'cl_age_et' : random_number_generator(jin_count, 30, 50)})

        #Create dataframe with random vales for VIN
        rand_vin = pd.DataFrame({'cl_age_et' : random_number_generator(vin_count, 70, 120)})

        # Get count of each random number generated
        jin_value_counts = rand_jin['cl_age_et'].value_counts().reset_index()
        vin_value_counts = rand_vin['cl_age_et'].value_counts().reset_index()

        # Add count of random JIN to values_count_df
        value_counts = pd.concat([value_counts, jin_value_counts], axis=0, ignore_index=True)

        # Add count of random VIN to values_count_df
        value_counts = pd.concat([value_counts, vin_value_counts], axis=0, ignore_index=True)



        # remove rows of JIN, VIN (now random number between age range)
        values_to_drop = ['JIN', 'VIN']
        value_counts = value_counts[~value_counts[collumn].isin(values_to_drop)]

        # Group by column 'A' and sum the values in column 'B'
        value_counts = value_counts.groupby(collumn, as_index=False)['count'].sum()

    # Sort by collumn value
    value_counts = value_counts.sort_values(collumn)
    #print(value_counts)

    return value_counts

def encode_discrete_data(df, collumn, encoding):
    bin_size = encoding

    value_counts = df[collumn].value_counts().reset_index()

    #Round to lowest tens
    value_counts[collumn] = (value_counts[collumn] // bin_size) * bin_size

    # Group by column 'A' and sum the values in column 'B'
    value_counts = value_counts.groupby(collumn, as_index=False)['count'].sum()

    value_counts = value_counts.sort_values(collumn)

    return value_counts

def normalize_continuous_data(df, collumn):
    new_df = pd.DataFrame()

    if collumn == 'year':
        # Don't normalise years
        new_df[collumn] = df[collumn]
    else:
        new_df[collumn] = (df[collumn] - df[collumn].min()) / (df[collumn].max() - df[collumn].min())

    return new_df 

def encode_continuous_data(df, collumn, bin_size = 0.05):

    value_counts = df[collumn].value_counts().reset_index()

    #Round to lowest tens
    value_counts[collumn] = (value_counts[collumn] // bin_size) * bin_size

    # Group by column 'A' and sum the values in column 'B'
    value_counts = value_counts.groupby(collumn, as_index=False)['count'].sum()

    value_counts = value_counts.sort_values(collumn)


    return value_counts

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

def prepare_data_old(df):

    data = {}
    iter_count = len(geodata_dictionnary)
    print(iter_count)
    for index, row in geodata_dictionnary.iterrows():

        if index == iter_count:
            break 
        # reset dfTemp for each row
        dfTemp = df

        print('')
        print('-----------------------')
        name = row['name']
        independent_var_type = row['independent_var_type']

        print(name + ' ({}/{})'.format(index+1, iter_count))
        print(independent_var_type)

        try:
            encoding = encoding_dictionnary[name]
        except:
            pass

        if independent_var_type == 'categorical':
            categorical_data = encode_categorical_data(dfTemp, name)
            print(categorical_data)
            data[name] = categorical_data 

        elif independent_var_type == 'ordinal':
            ordinal_data = encode_ordinal_data(dfTemp, name, encoding)
            print(ordinal_data)
            data[name] = ordinal_data 

        elif independent_var_type == 'discrete':
           discrete_data = encode_discrete_data(dfTemp, name, encoding)
           print(discrete_data)
           data[name] = discrete_data 

        elif independent_var_type == 'continuous':
           normalized_continuous_data =  normalize_continuous_data(dfTemp, name)
           continuous_data = encode_continuous_data(normalized_continuous_data, name)
           print(continuous_data)
           data[name] = continuous_data
           
        
        
    return data

def prepare_data(df):
    collumns_to_keep = ['year',
                        'eventDate',
                        'cl_pent',
                        'dep_sur',
                        'cl_drai',
                        'cl_haut',
                        'ty_couv_et',
                        'densite',
                        'cl_age_et',
                        'richness_index',
                        'shannon_index',
                        'tree_cover']
    
    #remove tree_cover for now
    del collumns_to_keep[-1]
    
    # Keep only specified coluns
    df = df[collumns_to_keep]

    # Catch NaNs
    df = df.replace('NaN', 0)
    df.fillna(0, inplace=True)
    
    # Encode ordinal data 
    for series_name, series in df.items():
        try:
            df[series_name] = df[series_name].map(encoding_dictionnary[series_name])
        except:
            pass

    # Describe depot surface categorical data
    df['dep_sur'] = df['dep_sur'].apply(dep_sur_map_category)

    # Chnage datatypes from floats to int 
    df = df.astype({"year": 'int',
                    "cl_drai": 'int',
                    'densite' : 'int'
                     })
    

   # hot-one encoding for categorical 

    print(df.head())

    #df = pd.get_dummies(data=df, drop_first=True)

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

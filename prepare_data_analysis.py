import numpy as np 
import pandas as pd

import matplotlib.pyplot as plt
from tools import random_number_generator
import csv

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
                            'VIN' : 'VIN',
                            'JIN' : 'JIN'
                        }

}

def encode_categorical_data(df, collumn, show = False):

    series = df[collumn]
    # Count per value 
    value_counts = series.value_counts().reset_index()


    if show == True:
        print(value_counts)
        ax = value_counts.plot(kind='bar')
        plt.show()

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

def prepare_data(df):

    data = {}
    iter_count = len(geodata_dictionnary)
    print(iter_count)
    for index, row in geodata_dictionnary.iterrows():

        if index == iter_count:
            break 
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

            #categorical_data = encode_categorical_data(dfTemp, name)
            #data[name] = categorical_data 
            pass

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
           print(normalized_continuous_data)

           data[name] = normalized_continuous_data
           pass
           
        
        
    return data

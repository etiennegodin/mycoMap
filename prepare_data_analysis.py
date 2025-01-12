import numpy as np 
import pandas as pd

import matplotlib.pyplot as plt
import tools
import csv

# https://chatgpt.com/c/67842692-c814-800d-aa2f-627792370f2d


geodata_dictionnary = pd.read_csv('data/geodata_dictionnary.csv', header = 0 )

def pepare_categorical_data(df, collumn, show = False):

    series = df[collumn]
    # Count per value 
    value_counts = series.value_counts().reset_index()

    if show == True:
        print(value_counts)
        ax = value_counts.plot(kind='bar')
        plt.show()

    return value_counts




def prepare_data(df):

    data = {}

    for index, row in geodata_dictionnary.iterrows():

        name = row['name']
        independent_var_type = row['independent_var_type']
        
        if independent_var_type == 'categorical':
            categorical_data = pepare_categorical_data(df, name)

            data[name] = categorical_data 
        
        elif independent_var_type == 'ordinal':
            pass

        elif independent_var_type == 'discrete':
           pass
        elif independent_var_type == 'continuous':
           pass
        
        
    return data








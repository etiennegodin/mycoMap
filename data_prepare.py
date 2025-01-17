import pandas as pd
import utilities
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt


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

def fungi_ecology_index(df):

    df_fungi_index = df[['geoc_maj', 'species']]
    
    # Step 1: Calculate diversity index (distinct species count per geo-point)
    df_fungi_index['fungi_diversity_index'] = df_fungi_index.groupby('geoc_maj')['species'].transform('nunique')

    # Step 2: Calculate Shannon index
    # Count occurrences of each species per geo-point
    species_counts = df_fungi_index.groupby(['geoc_maj', 'species']).size().reset_index(name='count')

    # Calculate proportions and Shannon index
    species_counts['proportion'] = species_counts['count'] / species_counts.groupby('geoc_maj')['count'].transform('sum')
    species_counts['shannon_component'] = species_counts['proportion'] * np.log(species_counts['proportion'])
    shannon_index = species_counts.groupby('geoc_maj')['shannon_component'].sum().reset_index(name='fungi_shannon_index')
    shannon_index['fungi_shannon_index'] *= -1  # Multiply by -1 as Shannon index is negative

    # Step 3: Merge Shannon index back into the original DataFrame
    df_fungi_index = df_fungi_index.merge(shannon_index, on='geoc_maj', how='right')

    #Removies species duplicate
    df_fungi_index = df_fungi_index.drop(columns= ['species'])

    # Merge with origianl df
    df = df.merge(df_fungi_index, on = 'geoc_maj', how = 'right')

    return df

def prepare_data(df):

    collumns_to_keep = [
                        'year',
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
                        'fungi_diversity_index',
                        'fungi_shannon_index',
                        'tree_cover']
    

    #remove tree_cover for now
    del collumns_to_keep[-1]
    
    # Keep only specified coluns
    df = df[collumns_to_keep]

    df = df.rename(columns= {'richness_index' : 'tree_diversity_index', 'shannon_index': 'tree_shannon_index'})


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
    


    utilities.explore_df(df)


    return df

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

if __name__ == '__main__':


    path = 'data/output/allOccurences.csv'

    df = pd.read_csv(path)

    # Calculate ecology index from mushroom species
    df = fungi_ecology_index(df)
    # Clean, prepare, encode data
    df = prepare_data(df)
    print(df.head())

    df2 = df[['tree_diversity_index', 'tree_shannon_index','fungi_diversity_index','fungi_shannon_index']]
    df3 = df[['ty_couv_et','cl_age_et','densite','fungi_diversity_index','fungi_shannon_index']]
    df4 = df[['cl_pent','cl_drai','cl_haut','fungi_diversity_index','fungi_shannon_index']]



    sns.pairplot(df)
    plt.show()


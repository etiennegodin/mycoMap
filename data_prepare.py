import pandas as pd

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
    


    print(df.head())


    return df




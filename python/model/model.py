import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

occurences = 'data/occurences/processedOccurencesCleanup.csv'

df = pd.read_csv(occurences)


def prep_df(df):


    env_vars = [ 'roadDist',
     'pop_densit',
     'type_couv',
     'gr_ess',
     'cl_dens',
     'cl_haut',
     'cl_age',
     'cl_pent',
     'dep_sur',
     'cl_drai',
     'type_eco',
     'ty_couv_et',
     'densite',
     'hauteur',
     'cl_age_et',
     'tree_cover',
     'tree_diversity_index',
     'tree_shannon_index',
     'region_code',
     'bioclim_01',
     'bioclim_02',
     'bioclim_03',
     'bioclim_04',
     'bioclim_05',
     'bioclim_06',
     'bioclim_07',
     'bioclim_08',
     'bioclim_09',
     'bioclim_10',
     'bioclim_11',
     'bioclim_12',
     'bioclim_13',
     'bioclim_14',
     'bioclim_15',
     'bioclim_16',
     'bioclim_17',
     'bioclim_18',
     'bioclim_19',
     'twi']


def prep_df(df):

    #which factor influence more fungi species richness 
    columns = [ 'species',
               'roadDist',
     'pop_densit',
     'type_couv',
     'gr_ess',
     'cl_dens',
     'cl_haut',
     'cl_age',
     'cl_pent',
     'dep_sur',
     'cl_drai',
     'type_eco',
     'ty_couv_et',
     'densite',
     'hauteur',
     'cl_age_et',
     'tree_cover',
     'tree_diversity_index',
     'tree_shannon_index',
     'region_code',
     'bioclim_01',
     'bioclim_02',
     'bioclim_03',
     'bioclim_04',
     'bioclim_05',
     'bioclim_06',
     'bioclim_07',
     'bioclim_08',
     'bioclim_09',
     'bioclim_10',
     'bioclim_11',
     'bioclim_12',
     'bioclim_13',
     'bioclim_14',
     'bioclim_15',
     'bioclim_16',
     'bioclim_17',
     'bioclim_18',
     'bioclim_19',
     'twi']
    
    categorical_vars = []
    ordered_vars = []
    numerical_vars = []

    species_col = 'species'
    df = df[columns]

    


    for col, dtype  in df.dtypes.items():
        if col == 'species':
            pass 
        elif pd.api.types.is_float_dtype(dtype):
            numerical_vars.append(col)

        elif pd.api.types.is_integer_dtype(dtype):
            ordered_vars.append(col)
        else:
            categorical_vars.append(col)

    #manual fixes
    numerical_vars.remove('cl_age')
    ordered_vars.append('cl_age')

    numerical_vars.remove('cl_age_et')
    ordered_vars.append('cl_age_et')

    numerical_vars.remove('twi')
    ordered_vars.append('twi')

    print(categorical_vars)
    print(numerical_vars)
    print(ordered_vars)

    non_numerical_vars = categorical_vars + ordered_vars
    richness_series = []    
    #get richness of each variable as series 
    for var in non_numerical_vars:
        if var == 'species' or var == 'tree_cover' or var == 'type_eco' or var == 'type_couv':
            pass
        else:
            richness = df.groupby(var)['species'].nunique().reset_index()
            richness_series.append(richness)

    for var in numerical_vars:
        df['binned'] = pd.cut(df[var], bins=10)
        richness = df.groupby('binned')['species'].nunique().reset_index()
        richness_series.append(richness)


        print(len(richness_series))
        # get spread min, max etc of richness based on each 
        # get info omn which influences more 

        for r in richness_series:
            #print(r.describe())

            #print(r['species'].mean())
            print(r['species'].std())




    
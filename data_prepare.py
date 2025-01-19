import pandas as pd
import utilities
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm

import data_analysis as da

def _print_geoc_maj_duplicates(df):
    print('df has {} duplicates'.format(df.duplicated(subset=['geoc_maj']).sum()))

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

    df_fungi_index.drop_duplicates(subset=['geoc_maj'], inplace = True)
    df.drop_duplicates(subset=['geoc_maj'], inplace = True)

    #Merge
    df = df.merge(df_fungi_index, on ='geoc_maj', how = 'inner')

    # Remove most occurences-based collumns as now this is geo point space 
    collumns_to_keep = ['geoc_maj',
                        'X',
                        'Y',
                        'cl_pent',
                        'dep_sur',
                        'cl_drai',
                        'cl_haut',
                        'ty_couv_et',
                        'densite',
                        'cl_age_et',
                        'tree_diversity_index',
                        'tree_shannon_index',
                        'fungi_diversity_index',
                        'fungi_shannon_index']
    

    
    # Keep only specified coluns
    df = df[collumns_to_keep]

    return df

def prepare_data(df):

    collumns_to_keep = ['geoc_maj',
                        'X',
                        'Y',
                        'species',
                        'year',
                        'eventDate',
                        'cl_pent',
                        'dep_sur',
                        'cl_drai',
                        'cl_haut',
                        'ty_couv_et',
                        'densite',
                        'cl_age_et',
                        'tree_diversity_index',
                        'tree_shannon_index']
    

    
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

    # Catch NaNs
    df = df.replace('NaN', 0)
    df.fillna(0, inplace=True)
    
    return df

def filter_single_specie_point(df, col, count = 1):
    mean_value = df[col].mean()
    min_value = df[col].min()
    max_value = df[col].max()
    std = df[col].std()
    median_value = df[col].median()


    threshold = min_value + 5 * std

    #filtered_df = df[(df[col] > 1)]

    #filtered_df = df[(df[col] <= threshold)]
    filtered_df = df[(df[col] > count)]
    return filtered_df

def plot_lnr_reg(df):
    fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(12, 6))  # Adjust figsize as needed
    axs = axs.flat

    y = df['fungi_diversity_index']

    for col, ax in zip(df.columns[1:],axs):
        X = df[col]

        X_with_const = sm.add_constant(X)
        
        # Fit the linear regression model
        model = sm.OLS(y, X_with_const).fit()
        
        # Predict values for the regression line
        y_pred = model.predict(X_with_const)
        
        # Plot the data points
        ax.scatter(X, y, label='Data', color='blue')
        r = round(model.rsquared, ndigits= 5)
        p = round(model.f_pvalue)
        # Plot the regression line
        ax.plot(X, y_pred, label='r {}, p{}'.format(r,p), color='red')
        
        # Add title and legend
        ax.set_title(f"Linear Regression: {col} vs X")
        ax.legend()

    plt.tight_layout()
    plt.show()

def plot_iter(df, Y):
    
    fig, axs = plt.subplots(nrows=2, ncols=4, figsize=(12, 6))  # Adjust figsize as needed
    axs = axs.flat
    # Iterate through the DataFrame columns (excluding the independent variable)
    for col, ax in zip(df.columns[1:], axs):
        # Scatterplot with regression line for each dependent variable
        # x_jitter when the x variable is discrete:

        #Or aggregate over the distinct x values:

        # x_estimator=np.mean, order=2

        #with a continuous x variable, bin and then aggregate:
        #x_bins=np.arange(0, 7, 0.25)

        sns.regplot(x=col, y=Y, data=df, ax=ax,x_estimator=np.mean,order = 3,scatter_kws={'color': 'blue'}, line_kws={'color': 'red'})
        #sns.boxenplot(x=col, y=Y, data=df, ax=ax)

        #sns.boxplot(x=col, y='fungi_diversity_index', data=df, ax=ax)
        #sns.violinplot(x=col, y=Y, data=df, ax=ax)

        # Add title
        ax.set_title(f"{col} vs {Y}")
        ax.legend()

    plt.tight_layout()
    plt.show()

def plot_iter_counts(df):

    
    fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(12, 6))  # Adjust figsize as needed
    axs = axs.flat
    # Iterate through the DataFrame columns (excluding the independent variable)
    for col, ax in zip(df.columns[1:], axs):

        # Scatterplot with regression line for each dependent variable
        #sns.regplot(x=col, y='fungi_diversity_index', data=df, ax=ax, scatter_kws={'color': 'blue'}, line_kws={'color': 'red'})
        sns.countplot(x=col, data=df, ax=ax)

        # Add title
        ax.set_title(f"Occurences by {col} categories ")
        ax.legend()

    plt.tight_layout()
    plt.show()



geodata_dictionnary = pd.read_csv('data/geodata_dictionnary.csv', header = 0 )

encoding_dictionnary = { 'cl_pent':
                        {
                            'A' : 6,
                            'B' : 5,
                            'C' : 4,
                            'D' : 3,
                            'E' : 2,
                            'F' : 1,
                            'S' : 10
                        },

                        'cl_drai' : 10,
                        'densite' : 10,
                        'cl_haut' : {
                                1 : 7,
                                2 : 6,
                                3 : 5,
                                4 : 4,
                                5 : 3,
                                6 : 2,
                                7 : 1},
 
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
    #path = 'data/gbifQueries/Cerioporus_squamosus/Cerioporus_squamosus_geodata.csv'


    df = pd.read_csv(path)

    #_print_geoc_maj_duplicates(df)

    # Clean, prepare, encode data
    df = prepare_data(df)
    df_occ = df
    # Calculate ecology index from mushroom species
    # This is now in geo dimension instead of occurence dimension
    df = fungi_ecology_index(df)

    utilities.saveDfToCsv(df, 'data/output/AllOccurences_withFungidata.csv')

    #df = filter_single_specie_point(df, 'fungi_diversity_index', count = 1)

    utilities.explore_df(df,describe=True, corr = True)



    df = df[['fungi_diversity_index', 'tree_shannon_index', 'tree_diversity_index','cl_age_et','densite','cl_pent','cl_drai','cl_haut']]
    #df = df[['fungi_shannon_index', 'tree_shannon_index', 'tree_diversity_index','cl_age_et','densite','cl_pent','cl_drai','cl_haut']]

    df_occ = df_occ[['tree_diversity_index','cl_age_et','densite','cl_pent','cl_drai','cl_haut']]

    #plot_iter_counts(df_occ)
    #plot_iter(df, 'fungi_diversity_index' )

    #plt.show()
    

    

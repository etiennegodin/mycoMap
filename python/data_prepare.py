import pandas as pd
import utilities
import numpy as np
import os

import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import statsmodels.api as sm

from scipy.stats import entropy
from scipy.stats import gaussian_kde

import data_analysis as da

import python.data_geodata as data_geodata

def prepare_test_data(file1, factors):

    file1_name = file1[-7:]

    file2 = 'data/geodata/region_env_factors/CARTE_ECO_MAJ_' + file1_name
    file1_collumns_to_keep = ['geoc_maj',
                        'X',
                        'Y',
                        'cl_dens',
                        'cl_haut',
                        'cl_age',
                        'cl_pent',
                        'dep_sur',
                        'cl_drai']
    

    file2_collumns_to_keep = ['geoc_maj',
                        'densite',
                        'hauteur',
                        'cl_age_et',
                        'tree_cover']


                    
    df1 = pd.read_csv(file1,  usecols= file1_collumns_to_keep)

    df2 = pd.read_csv(file2,  usecols= file2_collumns_to_keep)

    df2 = utilities.convert_string_to_numeral(df2)
    #df2['tree_cover'] = df2['tree_cover'].apply(geodata.interpret_tree_cover_string)

    df2 = data_geodata.ecology_factors(df2)

    df = pd.merge(df1,df2, on='geoc_maj')

    # Keep only specified coluns

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
    df = df.astype({
                    "cl_drai": 'int',
                    'densite' : 'int'
                     })

    # Catch NaNs
    df = df.replace('NaN', 0)
    df.fillna(0, inplace=True)



    df_test = df[factors]

    cols = ['X','Y', 'geoc_maj']

    df_coords = df[cols]
    
    return df_test, df_coords

def prepare_model_data(df):

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

def _print_geoc_maj_duplicates(df):
    print('df has {} duplicates'.format(df.duplicated(subset=['geoc_maj']).sum()))

def dep_sur_map_category(value):
    value = str(value)
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

def fungi_ecology_index_niche_dimension(df,dimension):

    df = df[[dimension, 'species']]

    # Return catories for dimension 
    categories = df[dimension].unique()

    for cat in categories:
        print(cat)



    #df = df.transform('nunique').agg(['min', 'max', 'mean', 'std']).reset_index()
    #Simple df with only categories 
    print(df )

    diversity_stats =df.groupby('species')[dimension].transform('nunique').agg(['min', 'max', 'mean', 'std']).reset_index()
    

    #diversity_stats =df.groupby(dimension)['species'].transform('nunique').agg(['min', 'max', 'mean', 'std']).reset_index()
    print(diversity_stats)
    #diversity_stats.columns = [dimension, 'Category_Min', 'Category_Max', 'Category_Mean', 'Category_Std']
    
    '''
    # Step 1: Calculate diversity index (distinct species count per geo-point)
    #df_fungi_index['fungi_diversity_index'] = df_fungi_index.groupby(dimension)['species'].transform('nunique')

    # Step 2: Calculate Shannon index
    # Count occurrences of each species per geo-point
    species_counts = df_fungi_index.groupby([dimension, 'species']).size().reset_index(name='count')

    # Calculate proportions and Shannon index
    species_counts['proportion'] = species_counts['count'] / species_counts.groupby(dimension)['count'].transform('sum')
    species_counts['shannon_component'] = species_counts['proportion'] * np.log(species_counts['proportion'])
    shannon_index = species_counts.groupby(dimension)['shannon_component'].sum().reset_index(name='fungi_shannon_index')
    shannon_index['fungi_shannon_index'] *= -1  # Multiply by -1 as Shannon index is negative

    # Step 3: Merge Shannon index back into the original DataFrame
    df_fungi_index = df_fungi_index.merge(shannon_index, on=dimension, how='right')


    # Distribution 

    print(df_fungi_index.head(20))
    print('y' * 50)


    diversity_stats = df_fungi_index.groupby(dimension)['species'].transform('nunique').agg(['min', 'max', 'mean', 'std']).reset_index()
    print(diversity_stats.head(20))
    #diversity_stats.columns = [dimension, 'Category_Min', 'Category_Max', 'Category_Mean', 'Category_Std']

    df_fungi_index = pd.merge(df_fungi_index, diversity_stats, on=dimension, how='left')

    print(df_fungi_index.head(20))
    print('-' * 50)

    df_fungi_index.drop_duplicates(subset=[dimension], inplacwe = True)
    df.drop_duplicates(subset=[dimension], inplace = True)

    print(df_fungi_index.head(20))

    print('x' * 50)

    #Merge
    df = df.merge(df_fungi_index, on = dimension, how = 'inner')

    print(df.head(20))

    return df

    '''

def fungi_ecology_index_geoc(df):

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

def plot_auto_rows(df_cols):
    df_cols = 8 
    for i in range(4,1, -1):
        x = df_cols % i 
        print(i ,x)



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

    col_count = df_model.shape[1]



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

def plot_scatter_3d_factors(df, factors, value = None ,jitter = 0.1):

    jitter_strength = jitter
    df[factors[0]] = df[factors[0]] + np.random.uniform(-jitter_strength, jitter_strength, len(df))
    df[factors[0]] = df[factors[0]] + np.random.uniform(-jitter_strength, jitter_strength, len(df))
    df[factors[0]] = df[factors[0]] + np.random.uniform(-jitter_strength, jitter_strength, len(df))

    x = df[factors[0]]
    y = df[factors[1]]
    z = df[factors[2]]

    c = df[value]  # Or use 'num_individual_species' or 'diversity'

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    sc = ax.scatter(x, y, z, c=c, cmap='viridis', s=50, edgecolor='k', alpha=0.7)

    #print(occurences_counts['occurrences'].sum())
    ax.set_xlabel(f'{factors[0]}')
    ax.set_ylabel(f'{factors[1]}')
    ax.set_zlabel(f'{factors[2]}')
    ax.set_title('3D Scatter Plot of Abiotic Factors')

    plt.colorbar(sc, label=value)

    plt.show()
 
def plot_kde_3d_factors(df, factors):

    x = df[factors[0]]
    y = df[factors[1]]
    z = df[factors[2]]

    # Stack the data points into a 2D array where each column is a variable
    data = np.vstack([x, y, z])

    # Calculate KDE using scipy's gaussian_kde
    kde = gaussian_kde(data)

    # Create a grid for evaluating the KDE (we'll use a 3D grid)
    xgrid = np.linspace(x.min(), x.max(), 30)
    ygrid = np.linspace(y.min(), y.max(), 30)
    zgrid = np.linspace(z.min(), z.max(), 30)

    # Create a meshgrid for 3D evaluation (x, y, z)
    xgrid, ygrid, zgrid = np.meshgrid(xgrid, ygrid, zgrid)

    # Flatten the grid for evaluation
    grid_points = np.vstack([xgrid.ravel(), ygrid.ravel(), zgrid.ravel()])

    # Evaluate the KDE on the 3D grid
    density = kde(grid_points)

    # Reshape the density to the 3D grid shape
    density = density.reshape(xgrid.shape)

    # Create a 3D plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plot the KDE surface using plot_surface
    surf = ax.plot_surface(xgrid, ygrid, density, cmap='viridis', edgecolor='none')

    # Add labels and title
    ax.set_xlabel(factors[0])
    ax.set_ylabel(factors[1])
    ax.set_zlabel('Density')
    ax.set_title('3D KDE Plot of Abiotic Factors')

    # Add color bar for density
    fig.colorbar(surf, label='Density')

    # Show the plot
    plt.show()

def shannon_diversity(species_counts):
    # Shannon Index: H' = -sum(p_i * log(p_i))
    p = species_counts / species_counts.sum()
    return -np.sum(p * np.log(p))

def derive_abiotic_factors(df_model,factors):


    max_species = df_model['species'].nunique()
    max_occurences = len(df_model)

    grouped = df_model.groupby(factors)
    
    print(f'Analysing {max_occurences} occurences of {max_species} species')
    print(f'Deriving model based on {len(factors)} factors')
    print(f'{len(grouped)} possible combinations of factors')

    diversity_values = grouped['species'].value_counts().unstack().apply(shannon_diversity, axis=1).reset_index(name='shannon_index_fungi')
    species_count_values = grouped['species'].nunique().reset_index(name='fungi_diversity_index')
    species_count_values['sp_prop'] = species_count_values.apply(lambda row: row['fungi_diversity_index'] /max_species, axis = 1)
    
    counts = grouped.size().reset_index(name='occurrences')
    proportion = counts.apply(lambda row: row['occurrences'] / max_occurences, axis = 1 ).reset_index(name = 'occ_prop')
    print(counts)
    #diversity_values = diversity_values.reset_index()
    #species_count_values = species_count_values.reset_index()

    temp = pd.merge(diversity_values,species_count_values, on=factors, how='inner')

    model = pd.merge(diversity_values,species_count_values, on=factors, how='inner')
    model = pd.merge(model, counts, on=factors, how='inner' )
    model = model.join(proportion)
    model.drop(columns=['index'], inplace = True)
    #model.sort_values(by=['fungi_diversity_index', 'shannon_index_fungi'], ascending=False, inplace= True)
    return model


def apply_model(dfmodel,df_test,factors):

    result = pd.merge(df_test,dfmodel, on=factors, how='left')

    return result


def main_iter(region_list):


    for region in region_list:

        file1 = f'data/geodata/regions_data/{region}/{region}.csv'

        df_model = pd.read_csv(path)

        factors = ['tree_diversity_index', 'tree_shannon_index','densite','cl_pent','cl_drai','cl_haut']

        # Clean, prepare, encode data
        df_model = prepare_model_data(df_model)

        df_model = derive_abiotic_factors(df_model, factors)


        '''
        df_test, df_coords = prepare_test_data(file1, factors)

        df_test_mapped = apply_model(df_model, df_test, factors)

        #Reapply X Y coords ( eviter de le faire dans le apply model )
        df_out = pd.merge(df_test_mapped,df_coords,  left_index=True, right_index=True)

        print('output')
        print(df_out)

        file1_name = file1[-7:]

        utilities.saveDfToCsv(df_out, f'data/output/regions/derivedRegion{region}.csv')
        '''
    
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

    regions_list = os.listdir('data/geodata/regions_data')    
    #main_iter(regions_list)

    df_model = pd.read_csv(path)

    factors = ['tree_diversity_index', 'tree_shannon_index','densite','cl_pent','cl_drai','cl_haut']



    factors = ['tree_diversity_index', 'densite', 'cl_haut']

    #factors = [ 'tree_diversity_index','cl_pent','cl_drai']

    # Clean, prepare, encode data
    #df_model = prepare_model_data(df_model)

    #df_model = derive_abiotic_factors(df_model, factors)
    

    col_count = df_model.shape[1]

    plot_auto_rows(8)

    #plot_scatter_3d_factors(df_model, factors, value = ['sp_prop'] )


'''
    occurences_counts = df.groupby(factors)['species'].count().reset_index(name='occurrences')

    species_diversity = df.groupby(factors)['species'].value_counts().unstack(fill_value=0)

    individual_species = df.groupby(factors)['species'].nunique().reset_index(name='diversity')


    diversity_scores = species_diversity.apply(shannon_index, axis=1).reset_index(name='shannon_index')

    result = pd.merge(occurences_counts, individual_species, on=factors)

    result = pd.merge(result,diversity_scores,  on=factors)

    result = result.sort_values(by=['occurrences', 'shannon_index'], ascending=False)

    print(result)

    '''



    # Calculate ecology index from mushroom species
    # This is now in geo dimension instead of occurence dimension
    #df_geoc = fungi_ecology_index_geoc(df)

    #df = fungi_ecology_index_niche_dimension(df, 'cl_haut')


    #df = filter_single_specie_point(df, 'fungi_diversity_index', count = 1)

    #utilities.explore_df(df,describe=True, corr = True)



    #df = df[['fungi_diversity_index', 'tree_shannon_index', 'tree_diversity_index','cl_age_et','densite','cl_pent','cl_drai','cl_haut']]
    #df = df[['fungi_shannon_index', 'tree_shannon_index', 'tree_diversity_index','cl_age_et','densite','cl_pent','cl_drai','cl_haut']]

    #df_occ = df_occ[['tree_diversity_index','cl_age_et','densite','cl_pent','cl_drai','cl_haut']]

    #plot_iter_counts(df_occ)
    #plot_iter(df, 'fungi_diversity_index' )

    #plt.show()
    

    

# cleanup occurences data after process
import sys, os
import pandas as pd 
import geopandas as gpd
from shapely.geometry import Polygon, Point
import matplotlib.pyplot as plt
import numpy as np

import seaborn as sns 

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import utils 

pd.set_option('display.max_colwidth', 1000)

def df_to_gdf(df, xy = ['X', 'Y']):

    # Creates goepandas from dataframe with lat/long columns
    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df[xy[0]], df[xy[1]]), crs="EPSG:4326"
    )
    return gdf

def gdf_to_df(gdf):
    df = pd.DataFrame(gdf.drop(columns='geometry'))
    return df

def groupEnvVars(df, species_col = 'species'):

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

    return numerical_vars, ordered_vars, categorical_vars

def create_grid(gdf, grid_size_km = 1):
    min_x, min_y, max_x, max_y = gdf.total_bounds

    degrees_per_km_latitude = 1 / 111
    degrees_per_km_longitude = 1 / (111 * np.cos(np.radians((min_y + max_y) / 2)))
    grid_size_x_deg = grid_size_km * degrees_per_km_longitude
    grid_size_y_deg = grid_size_km * degrees_per_km_latitude

    x_coords = np.arange(min_x, max_x + grid_size_x_deg, grid_size_x_deg)
    y_coords = np.arange(min_y, max_y + grid_size_y_deg, grid_size_y_deg)

    grid_cells = []
    for i, x in enumerate(x_coords):
        for j, y in enumerate(y_coords):
            #print(i/len(x_coords), j / len(y_coords))
            top_left = (x,y + grid_size_y_deg)
            top_right = (x + grid_size_x_deg, y + grid_size_y_deg)
            bottom_right = (x + grid_size_x_deg, y)
            bottom_left = (x, y)

            grid_cell = Polygon([bottom_left, bottom_right, top_right, top_left])
            grid_cells.append(grid_cell)

    grid_gdf = gpd.GeoDataFrame({'geometry': grid_cells}, crs=gdf.crs)
    return grid_gdf


# Aggregates occurences in square km sites 

occurences = 'data/occurences/processedOccurencesCleanup.csv'
output_path = 'data/occurences/groupedOccurences.csv'
grid_size = 2

df = pd.read_csv(occurences)
print(df.shape)

# convert occurences df to gdf
occurences_gdf = df_to_gdf(df)

print('\n' + 'Occurences' + '\n')
print(occurences_gdf.head())

#get bounds of all observations 
xmin, ymin, xmax, ymax = occurences_gdf.total_bounds

#create polygon of area of interest 
polygon = Polygon([(xmin,ymin),(xmax,ymin),(xmax,ymax),(xmin,ymax)])
area_gdf = gpd.GeoDataFrame({'geometry': [polygon]}, crs = "EPSG:4326")

# xkm square grid in bounds of area 
grid = create_grid(area_gdf, grid_size_km = grid_size)

print(str(grid_size) +'km,', grid.shape[0], 'cells')

# find grid id 
occurences_in_grid = gpd.sjoin(occurences_gdf, grid, how = 'inner')
occurences_in_grid.rename(columns={'index_right':'site_id'}, inplace = True)


#richness
# as df
richness_df = occurences_in_grid.groupby('site_id').size().to_frame(name='fungi_richness')
print(richness_df.describe())
print(f'Found occurences in  {richness_df.shape[0]} grid cells')
print('%', richness_df.shape[0]/grid.shape[0])
#as series
#point_counts = occurences_in_grid.groupby('site_id').size()


#aggregate vars 
numerical_vars, ordered_vars, categorical_vars = groupEnvVars(df)

numerical_vars.append('site_id')
ordered_vars.append('site_id')
# numerical 

numerical_vars_df = occurences_in_grid[numerical_vars]
numerical_vars_df = numerical_vars_df.groupby('site_id').mean()

#ordered
ordered_vars_df = occurences_in_grid[numerical_vars]
ordered_vars_df = ordered_vars_df.groupby('site_id').mean()

site_df = grid.join(richness_df, how='left', lsuffix='_grid').fillna(0)
site_df = site_df.join(numerical_vars_df, how='left', lsuffix='_grid').fillna(0)
site_df = site_df.join(ordered_vars_df, how='left', lsuffix='_grid').fillna(0)

site_df = gdf_to_df(site_df)
print(site_df)
"""
 
grid_with_counts = grid.join(point_counts, how='left', lsuffix='_grid').fillna(0)


df_out = gdf_to_df(grid_with_counts)

print(df_out.head())
print(df_out.describe())
print(df_out['point_count'].var())
# check how many cells have 0 and inverse 

#sns.kdeplot(df_out,x = df_out['point_count'])
sns.displot(df_out,x = df_out['point_count'], bins = int(df_out['point_count'].max()))



plt.show()


debug = False
if debug:
    print('\n' + 'Grid' + '\n')
    print(grid)

    print('\n'+ 'Points in grid' + '\n')
    print(occurences_in_grid)

    print('\n'+ 'grid_with_counts' + '\n')
    print(grid_with_counts)

    print('\n'+ 'df_out' + '\n')
    print(df_out)

"""

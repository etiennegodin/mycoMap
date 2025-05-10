import geopandas as gpd
import pandas as pd
import numpy as np


from mycoMap.dataCleaning.occurences.clusterOccurences import * 
from mycoMap import utils 

occurences_path = 'data/interim/occurences/filteredOcurrences.csv'
occurences_output_path = 'data/interim/occurences/griddedOccurences.csv'
geoUtils_path = 'data/interim/geodata/vector/geoUtils/'

grid_size = 0.5
# load grid
grid = gpd.read_file(geoUtils_path + f'{grid_size}km_grid.shp')

#load occurences
df = pd.read_csv(occurences_path)
print(df.shape)
gdf = utils.df_to_gdf(df, xy = ['decimalLongitude','decimalLatitude'])
print(gdf.shape)
#spatial join
joined_gdf = gpd.sjoin(gdf, grid, how ='inner', predicate= 'intersects')
joined_gdf = joined_gdf.drop(['index_right'], axis = 1)
print(joined_gdf.shape)

df = utils.gdf_to_df(joined_gdf)
df.to_csv(occurences_output_path, index  = False)
import pandas as pd 
import geopandas as gpd
import numpy as np 

bias1 = 'data/interim/geodata/vector/bias/csv/distanceToUrban.csv'
bias2 = 'data/interim/geodata/vector/bias/csv/populationDensity.csv'
bias3 = 'data/interim/geodata/vector/bias/csv/roadDistance.csv'
bias4 = 'data/interim/geodata/vector/bias/csv/urbanGridded.csv'
bias5 = 'data/interim/geodata/vector/bias/csv/airesProtegeesGridded.csv'

grid_path = 'data/interim/geodata/vector/geoUtils/0.5km_centroid.shp'

output_csv = 'data/interim/geodata/vector/bias/csv/combinedBiases.csv'
output_shp = 'data/interim/geodata/vector/bias/shp/combinedBiases.shp'


biases = [bias1,bias2,bias3,bias4,bias5]

grid = gpd.read_file(grid_path)
grid_df = pd.DataFrame(grid.drop(columns='geometry'))


for bias in biases:
    df_temp = pd.read_csv(bias)
    print(df_temp.head())

    grid_df = grid_df.merge(df_temp, on = 'FID',how = 'left')


grid_df.rename(columns = {'HubDist' : 'distanceToUrban'}, inplace= True)
print(grid_df)
columns = ['FID', 'populationDensity', 'distanceToUrban', 'distanceRo', 'urbanArea', 'airesProtegees']

final_df = grid_df[columns]

# urban and aire proteges where counts, max to 1 
final_df.loc[final_df['urbanArea'] >= 0, 'urbanArea'] = 1
final_df.loc[final_df['airesProtegees'] >= 0, 'airesProtegees'] = 1

print(final_df)
print(final_df.describe())

final_df.to_csv(output_csv, index = False)

final_gdf = grid.merge(final_df, on = 'FID',how = 'left')
final_gdf.to_file(output_shp, driver='ESRI Shapefile')
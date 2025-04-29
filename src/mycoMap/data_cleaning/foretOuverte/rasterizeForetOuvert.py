
#Spatial Relationship Analysis

#grid 

#spatial join 

#summarize fields 
    #aggregates per field tpye 

import geopandas as gpd 

file = 'data/raw/geodata/vector/regions_data/21E/21E.shp'

gdf = gpd.read_file(file)
print(gdf)
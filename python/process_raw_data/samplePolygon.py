import geopandas as gpd
import pandas as pd 

# Load polygon and point datasets
polygons = gpd.read_file('data/geodata/raw/vector/regions_data/21E/21E.shp')
points = gpd.read_file("data/geodata/testing/randompoint.shp")      # Points GeoDataFrame

# Ensure both GeoDataFrames have the same CRS
polygons = polygons.to_crs(epsg=4326)
points = points.to_crs(epsg=4326)

# Spatial join: Find which polygon contains which point
joined = gpd.sjoin(points, polygons, predicate="within", how="left")

# Sample values from polygons for each matched point
sampled_values = joined.dropna().sample(n=1)  # Adjust 'n' for multiple samples

print(sampled_values)

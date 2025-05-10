import geopandas as gpd
import numpy as np 

from sklearn.cluster import KMeans

geoUtils_path = 'data/interim/geodata/vector/geoUtils/'
output_path = 'data/interim/occurences/clusteredGriddedOccurences.csv'

# load grid
grid = gpd.read_file(geoUtils_path + '0.5km_grid.shp')
centroids = grid.geometry.centroid

coords = np.vstack([centroids.x, centroids.y]).T

k = 5
kmeans = KMeans(n_clusters=k, random_state=42).fit(coords)
grid['block_id'] = kmeans.labels_

grid.to_file('data/interim/geodata/vector/geoUtils/clustered_0.5km_grid.shp', driver='ESRI Shapefile')
print('Exported')
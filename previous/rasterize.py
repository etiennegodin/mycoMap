# do this before sending to xarray
# to ensure extension is loaded
import rioxarray

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point


import numpy as np
from scipy.interpolate import griddata
import rasterio
from rasterio.transform import Affine
from rasterio import CRS

df = pd.read_csv('data/output/allRegionsMerged.csv')
df = df.drop(df.columns[2], axis=1)
print(df)

gdf = gpd.GeoDataFrame(df, 
    geometry = gpd.points_from_xy(df['X'], df['Y']), 
    crs = 'EPSG:4326')




# Extract relevant data
genericMycorrhizal = gdf['genericMycorrhizal'].values
X = gdf['X'].values
Y = gdf['Y'].values

# Set resolution and create grid
resolution = 50
x_range = np.arange(X.min(), X.max()+resolution, resolution)
y_range = np.arange(Y.min(), Y.max()+resolution, resolution)
grid_x, grid_y = np.meshgrid(x_range, y_range)

# Interpolate data onto grid
points = list(zip(X, Y))
grid_z = griddata(points, genericMycorrhizal, (grid_x, grid_y), method='cubic')

# Set negative values to 0
grid_z[grid_z < 0] = 0

# Define transformation and CRS
transform = Affine.translation(grid_x[0][0]-resolution/2, grid_y[0][0]-resolution/2) * Affine.scale(resolution, resolution)
crs = CRS.from_epsg(32198)

# Write interpolated raster to file
interp_raster = rasterio.open('Subsidence1.tif',
                              'w',
                              driver='GTiff',
                              height=grid_z.shape[0],
                              width=grid_z.shape[1],
                              count=1,
                              dtype=grid_z.dtype,
                              crs=crs,
                              transform=transform)
interp_raster.write(grid_z, 1)
interp_raster.close()
import numpy as np
from shapely.geometry import Polygon, Point
import geopandas as gpd
import pandas as pd 

from .. import utils 

def create_grid(gdf, grid_cell_size = 1, output_path = '', verbose = False):
    """
    Returns gdf grid based on input gdf bounds and grid cell size (in km)
    """
    min_x, min_y, max_x, max_y = gdf.total_bounds

    degrees_per_km_latitude = 1 / 111
    degrees_per_km_longitude = 1 / (111 * np.cos(np.radians((min_y + max_y) / 2)))
    grid_size_x_deg = grid_cell_size * degrees_per_km_longitude
    grid_size_y_deg = grid_cell_size * degrees_per_km_latitude

    x_coords = np.arange(min_x, max_x + grid_size_x_deg, grid_size_x_deg)
    y_coords = np.arange(min_y, max_y + grid_size_y_deg, grid_size_y_deg)

    grid_cells = []
    for i, x in enumerate(x_coords):
        if verbose:
            print(round(i / len(x_coords),2))
        for j, y in enumerate(y_coords):
            #print(i/len(x_coords), j / len(y_coords))
            top_left = (x,y + grid_size_y_deg)
            top_right = (x + grid_size_x_deg, y + grid_size_y_deg)
            bottom_right = (x + grid_size_x_deg, y)
            bottom_left = (x, y)

            grid_cell = Polygon([bottom_left, bottom_right, top_right, top_left])
            grid_cells.append(grid_cell)

    grid_gdf = gpd.GeoDataFrame({'geometry': grid_cells}, crs=gdf.crs)

    #save grid to disk 
    if output_path != '':
        grid_gdf.to_file(output_path)
        
    return grid_gdf

if __name__ == '__main__':


    occ = 'data/occurences/processedOccurences.csv'
    grid_size = 0.5
    
    output_path = f'data/interim/geodata/vector/grid/{grid_size}km_grid.shp'
    df = pd.read_csv(occ)
    gdf = utils.df_to_gdf(df)
    create_grid(gdf , grid_cell_size= grid_size, output_path = output_path, verbose= True)
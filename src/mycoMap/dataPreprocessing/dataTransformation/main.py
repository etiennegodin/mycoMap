import os 
import geopandas as gpd 
from sklearn.cluster import KMeans
import numpy as np 
import gc
from mycoMap.dataPreprocessing.dataTransformation import foretOuverte

CLUSTERED_GRID_OUTPUT_PATH = 'data/interim/geodata/vector/geoUtils/clustered_0.5km_grid.shp'

def encodeForetOuverteData(gdf, region, verbose = False):
    print(f'#{__name__}.encodeForetOuverteData')

    print(f'Encoding data for {region}')
    gdf = foretOuverte.encode_vector_fields(gdf, verbose = verbose)
    gdf = foretOuverte.encode_dep_sur(gdf, verbose = verbose)
    gdf = foretOuverte.encode_tree_cover(gdf, verbose = verbose)
    gdf = foretOuverte.processs_forest_ecology_indexes(gdf, verbose = verbose)

    return gdf 

def clusterGrid(grid_path, clusters = 5, overwrite = False):
    print(f'#{__name__}.clusterGrid')

    def main(grid_path,clusters):

        # load grid
        grid = gpd.read_file(grid_path)
        centroids = grid.geometry.centroid

        coords = np.vstack([centroids.x, centroids.y]).T

        k = clusters
        kmeans = KMeans(n_clusters=k, random_state=42).fit(coords)
        grid['block_id'] = kmeans.labels_

        grid.to_file(CLUSTERED_GRID_OUTPUT_PATH, driver='ESRI Shapefile')
        print(f'Exported {CLUSTERED_GRID_OUTPUT_PATH}')

    if os.path.isfile(CLUSTERED_GRID_OUTPUT_PATH):
        print(f'Grid already clustered')
        if overwrite:
            print('Overwritting')
            main(grid_path,clusters)
        else:
            pass
    else:
        main(grid_path,clusters)

    return CLUSTERED_GRID_OUTPUT_PATH


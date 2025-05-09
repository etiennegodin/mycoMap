import pandas as pd 
import geopandas 

from .. import utils
from ..dataCleaning.foretOuverte import mergeGpkg

input_gpkg_path = 'data/raw/geodata/foretOuverte/PEE_MAJ_PROV/gpkg' 
output_shp_path = 'data/interim/geodata/vector/bias/urbanAllRegion.shp'


def filter_gdf(gdf, filters = None):

    condition = (gdf['co_ter'] == 'ANT')
    filtered_gdf = gdf[condition]

    return filtered_gdf

if __name__ == '__main__':


    regions_list = utils.get_regionCodeList()

    allRegions_gdf = pd.DataFrame()

    for i, r in enumerate(regions_list):
        print('#'*5, f'{i+1}/{len(regions_list)}', '#'*5)

        gpkg_file = input_gpkg_path + f'/CARTE_ECO_MAJ_{r}.gpkg'

        layers = mergeGpkg.find_gpkg_layers(gpkg_file)
        layers_to_combine = [layers[1]]
        gdf_combined = mergeGpkg.combine_gpkg_layers(gpkg_file, layers = layers_to_combine)

        region_urban_gdf = filter_gdf(gdf_combined)

        allRegions_gdf = pd.concat([allRegions_gdf, region_urban_gdf])
    
    try:
        allRegions_gdf.to_file(output_shp_path, driver='ESRI Shapefile')
    except Exception as e:
        print(e)

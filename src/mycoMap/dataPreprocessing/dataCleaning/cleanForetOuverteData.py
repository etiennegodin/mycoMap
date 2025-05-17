import geopandas as gpd

from mycoMap.dataPreprocessing.dataIntegration import mergeForetOuverteData
from mycoMap import utils 

def test():
    x = 'test_text'
    return x

def main():
    data = gpd.GeoDataFrame()
    regions_list = utils.get_regionCodeList(verbose= True)
    for region in regions_list:
        gdf, perimeter_gdf = mergeForetOuverteData.merge_region_gpkg(region)
            #keep only relevant columns
        gdf = gdf[all_columns]

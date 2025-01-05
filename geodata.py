import geopandas as gpd
import matplotlib.pyplot as plt

from occurences import create_occurences_dataframe

def df_to_gdf(occ_df, xy = ['decimalLongitude', 'decimalLatitude']):

    # Creates goepandas from dataframe with lat/long columns
    occ_gdf = gpd.GeoDataFrame(
        occ_df, geometry=gpd.points_from_xy(occ_df[xy[0]], occ_df[xy[1]]), crs="EPSG:4326"
    )

    return occ_gdf
    
def gpd_assign_region(occ_gdf):

    regions_perimetre_file = 'data/geodata/regions_perimetre/regions_perimetre.shp'

    # Creat gdf from regions perimetre
    regions_gdf = gpd.read_file(regions_perimetre_file)

    # Join two geodataframe (naturally skips points not within bounds of perimetre)
    occ_gdf = gpd.sjoin(occ_gdf, regions_gdf, predicate='within')

    # Remove unecessary collumns
    occ_gdf = occ_gdf.drop(['index_right', 'decimalLongitude', 'decimalLatitude' ],axis=1)

    # Rename region_code collumn
    occ_gdf = occ_gdf.rename(columns={'idx_no_dec': 'region_code'})

    return occ_gdf





def populate_occurence_data(occ_gdf):

    regions_data_path = 'data/geodata/regions_data/'
    region_gdf_path = regions_data_path + occ_gdf['region_code']

    region_gdf = gpd.read_file(region_gdf_path)

    occ_gdf = gpd.sjoin(occ_gdf, region_gdf, predicate='within')

    print(occ_gdf)




    


# loop

    # load specific geo file based on region value

    # compare lat long with geodata from foret ouverte 
    # assign values of densite, cl_ag_et, tree_associations based on coordinate 





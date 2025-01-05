import matplotlib.pyplot as plt
import os
import pandas as pd
import geopandas as gpd
import numpy as np
from scipy.spatial import cKDTree
from shapely.geometry import Point

def df_to_gdf(df, xy = ['decimalLongitude', 'decimalLatitude']):

    # Creates goepandas from dataframe with lat/long columns
    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df[xy[0]], df[xy[1]]), crs="EPSG:4326"
    )

    return gdf


def gdf_to_df(gdf):
    df = pd.DataFrame(gdf.drop(columns='geometry'))
    return df

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


def ckdnearest(gdA, gdB):

    nA = np.array(list(gdA.geometry.apply(lambda x: (x.x, x.y))))
    nB = np.array(list(gdB.geometry.apply(lambda x: (x.x, x.y))))
    btree = cKDTree(nB)
    dist, idx = btree.query(nA, k=1)
    gdB_nearest = gdB.iloc[idx].drop(columns="geometry").reset_index(drop=True)

    gdf = pd.concat(
        [
            gdA.reset_index(drop=True),
            gdB_nearest,
            pd.Series(dist, name='dist'),
        ], 
        axis=1)

    return gdf

def find_nearest_point(occ_gdf):

    regions_data_path = 'data/geodata/regions_data/'

    print('')
    print('Feeding {} occurences to populate'.format(len(occ_gdf)))
    final_gdf = gpd.GeoDataFrame()

    region_code_list = os.listdir(regions_data_path)
    region_codes_amount = len(region_code_list)
    #region_codes_index = region_codes_amount  1
    for idx, region_code in enumerate(region_code_list):

        # End loop once all folders are done iterating
        if idx == region_codes_amount:
            break
        else:
            print(region_code)

            # Build path to read csv point of region
            region_gdf_path = regions_data_path + region_code + '/' + '{}.csv'.format(region_code)

            # Read region csv as dataframe
            df = pd.read_csv(region_gdf_path)

            # Reformat as gdf using xy as geometry
            region_gdf = df_to_gdf(df, xy = ['X','Y'])

            # Keep only relevant columns
            region_gdf = region_gdf[['geometry', 'geoc_maj']]

            # Keep only region occurences for region_occ_gdf
            region_occ_gdf = occ_gdf[(occ_gdf['region_code']==region_code)]

            # Check if occurence in this region
            if len(region_occ_gdf) != 0:
                print('{} occurences in {}'.format(len(region_occ_gdf), region_code))

                # nearest 
                gdf = ckdnearest(region_occ_gdf, region_gdf)
                #assign value from csv matching with geoc_maj

                #return partial df to final_gdf
                final_gdf = pd.concat([final_gdf, gdf])

            else:
                print(' - 0 occurences in {} - '.format(region_code))
                continue
            
    return final_gdf
    




    # Create geodataFrame for regions  
    #region_gdf = gpd.read_file(region_gdf_path)
    
    #print(region_gdf)
    # Read csv from region_code 

    

    #occ_gdf = gpd.sjoin(occ_gdf, region_gdf, predicate='within')

    





    


# loop

    # load specific geo file based on region value

    # compare lat long with geodata from foret ouverte 
    # assign values of densite, cl_ag_et, tree_associations based on coordinate 





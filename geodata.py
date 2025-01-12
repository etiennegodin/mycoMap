import os
import pandas as pd
import geopandas as gpd
import numpy as np
from scipy.spatial import cKDTree
from shapely.geometry import Point
import re

import tools 


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


    print('Debug flag for gpd_assign_region(). See comments')

        # debug
    #loosing some occurences in asign regions ??
    # check which by assigning new index collumns and compare with previous gdf
    # check if occurence just too far from forest points 
    
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

def interpret_tree_cover_string(code):
    # change tree cover infor from string to dict of percentage
    result = re.findall(r'([A-Z]+)(\d+)', code)
    result = dict(result)
    # value from string to %
    for key in result:
        result[key] = int(result[key]) / 100
    return(result)

def interpret_env_factors_data(path):

    # Read csv as df 
    df = pd.read_csv(path)

    # Interpret string descirption of tree composition as dict of {tree_kind : cover_percentage} 
    df['tree_cover'] = df['eta_ess_pc'].apply(interpret_tree_cover_string)

    #Keep only geoc_maj, densite, cl_age, tree_cover data
    df = df.iloc[:, [1,4,-3,-1]]

    return df 

def interpret_region_data(path):

    print('Debug flag for interpet_region_data(). See comments')

    #debug - could make loading region cv faster, complaining about columns (11,30) datatype 
    # -Specify dtype option on import
    df = pd.read_csv(path)

    #Keep only relevant collumns
    df = df[['geoc_maj', #id
                'cl_pent', # classe de pente
                'dep_sur', # depot surface
                'cl_drai', # classe drainage
                'origine', # Perturbation d'origine
                'an_origine', # annee pertrubation
                'perturb', # Perturbation partielle
                'an_perturb', # Année de la perturbation partielle
                'X',
                'Y']]
    
    return df

def assign_geodata_to_occurences(occ_gdf):

    regions_data_path = 'data/geodata/regions_data/'
    regions_env_factors_path = 'data/geodata/region_env_factors/CARTE_ECO_MAJ_'

    print('')
    print('Feeding {} occurences to populate'.format(len(occ_gdf)))
    final_gdf = gpd.GeoDataFrame()

    #list all regions to iterate over
    region_code_list = os.listdir(regions_data_path)
    # create int var for number of regions to check against loop index
    region_codes_amount = len(region_code_list)

    #Iterate over regions
    for idx, region_code in enumerate(region_code_list):

        # Check if iterated thourhg all regions 
        # End loop once all folders are done iterating
        if idx == region_codes_amount:
            break
        else:
            # From full occurence geodataframe, keep only occurences from current region
            region_occ_gdf = occ_gdf[(occ_gdf['region_code']==region_code)]

            # Check if any occurence in this region, otherwise skip to next
            if len(region_occ_gdf) != 0:

                print('{} occurences in {}'.format(len(region_occ_gdf), region_code))
                print(region_code)
                # Build path to read env factors data of region
                region_env_factors_path = regions_env_factors_path + region_code +'.csv'

                # Create dataframe from forest composition data of region 
                env_df = interpret_env_factors_data(region_env_factors_path)

                # Build path to read point data of region 
                region_gdf_path = regions_data_path + region_code + '/' + '{}.csv'.format(region_code)

                # Create dataframe from point data of region 
                df = interpret_region_data(region_gdf_path)

                #merge env_factors & point df based on geoc_maj index
                df = df.merge(env_df, on='geoc_maj')
            
                # Reformat as gdf using xy as geometry
                region_gdf = df_to_gdf(df, xy = ['X','Y'])

                #Remove redundant XY columns
                region_gdf = region_gdf.drop(columns=['X','Y'])



                # Find nearest point from occurence localisation and merge data
                gdf = ckdnearest(region_occ_gdf, region_gdf)
               
                #remove distance collumn from ckdnearest function, could be used for debug but not necessary in final 
                gdf = gdf.drop(columns=['dist'])

                #return region gdf as partial gdf to final_gdf
                final_gdf = pd.concat([final_gdf, gdf])

            else:
                print(' - 0 occurences in {} - '.format(region_code))
                continue
            
    return final_gdf
 
def interpet_env_factors(df):


    #interpet and gives value from columns of df referring to env_factors 
    # ex: cl_age_et : JIN = 80 years something something
    # cl_pente : A = pente 40 degrees etc 

    #create list of dicts for each columns using modified csv file from:

    #data/DICTIONNAIRE_CARTE_ECO_MAJ.xlsx
    pass


def geo(occ_df, specie):

    geodata_file = specie.path + specie.name + '_geodata.csv'
    
    if not os.path.exists(geodata_file):

    # Transform df in geopandas using Lat/Long info
        occ_gdf = df_to_gdf(occ_df)
        # Assign region based on geo coordinate
        occ_gdf = gpd_assign_region(occ_gdf)
        # Find closest data point and assign geo data to occurence
        occ_gdf = assign_geodata_to_occurences(occ_gdf)
        # Convert back to standard dataframe
        occ_df = gdf_to_df(occ_gdf)

        # Save df to file 
        tools.saveDfToCsv(occ_df, geodata_file)

        return occ_df

    elif os.path.exists(geodata_file):

        print('Geodata already processed for occurences and saved to ')
        print(geodata_file)
        occ_df = pd.read_csv(geodata_file)
        tools.convert_tree_cover_data_type(occ_df)

        return occ_df
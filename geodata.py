import os, re, utilities
import pandas as pd
import geopandas as gpd
import numpy as np
from scipy.spatial import cKDTree
from shapely.geometry import Point

import specie as sp 

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
    

    #Keep only geoc_maj, typ_couv_et, densite, cl_age, tree_cover data
    df = df.iloc[:, [1,3,4,-3,-1]]



    return df 

def interpret_region_data(path):

    collumns = ['geoc_maj', #id
                'cl_pent', # classe de pente
                'dep_sur',
                 'cl_age', # depot surface
                'cl_drai', # classe drainage
                'cl_haut', # classe hauteur
                 'type_couv', #ype couvert
                'origine', # Perturbation d'origine
                'an_origine', # annee pertrubation
                'perturb', # Perturbation partielle
                'an_perturb', # Année de la perturbation partielle
                'X',
                'Y']
    #debug - could make loading region cv faster, complaining about columns (11,30) datatype 
    # -Specify dtype option on import
    df = pd.read_csv(path, usecols= collumns)
    
    return df

def assign_geodata_to_occurences(occ_gdf, specie):

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

                print('{} {} occurences in {} (Species index {})'.format(len(region_occ_gdf), specie.name, region_code, specie.index))
                print(region_code + ' ({}/{})'.format(idx+1, len(region_code_list)))
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
                #region_gdf = region_gdf.drop(columns=['X','Y'])



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

def create_occurences_dataframe(occurences_file):

    occ_df = pd.read_csv(occurences_file, sep='\t')
    # Cleaning dataframe with only relevant info from occurence query

    occ_df = occ_df[['gbifID', 
                    'decimalLongitude', 
                    'decimalLatitude', 
                    'eventDate',
                    'year',
                    'stateProvince',
                    'species',
                    'occurrenceID']]
    
    # Removing rows not in quebec

    # Specified Canada only but Lat/ Long might make it in Ontario
    occ_df = occ_df[occ_df.stateProvince == 'Québec']

    # Reseting index from removed rows not in qc
    occ_df = occ_df.reset_index(drop=True)

    # Message printing how many occurences were in quebec
    print('From downloaded occurences {} were in Quebec and kept for analysis'.format(len(occ_df)))

    if len(occ_df) == 0:
        pass
    return occ_df

def richnessIndex(tree_cover):
    #indice de ricnesse (nb especes)
    n = len(tree_cover)
    return(n)

def shannonIndex(tree_cover):
    #indice shannon 
    #creer liste proportions d'essence
    proportions_list = []
    for key in tree_cover:
        #print(key)
        proportions_list.append(tree_cover[key])

    #numpy array
    proportions = np.array(proportions_list)

    try:
        # Vérifiez que la somme des proportions est égale à 1 (100%)
        if not np.isclose(np.sum(proportions), 1.0):
            raise ValueError("Les proportions des espèces doivent totaliser 1")
        
        # Calculez l'indice de Shannon
        shannon_index = -np.sum(proportions * np.log(proportions))
        
    except ValueError:
        # En cas d'erreur, attribuez la valeur 0 à l'indice de Shannon
        shannon_index = 0
        
    shannon_index = -np.sum(proportions * np.log(proportions))

    # Entropy 
    # SUm of surprise for each of elements
    return(shannon_index)

def ecology_factors(df):
    df['tree_diversity_index'] = df['tree_cover'].apply(richnessIndex) 
    df['tree_shannon_index'] = df['tree_cover'].apply(shannonIndex)

    return df 

def process_specie_geodata(specie,use_processed_geo_only):
    
    # First check if occurences are dwownloaded for this specie
    if os.path.exists(specie.occurence_file):

        # Check if geodata file already processed
        if not os.path.exists(specie.geodata_file):

            if not use_processed_geo_only:
                occ_df = create_occurences_dataframe(specie.occurence_file)
                if len(occ_df) == 0:
                    print(f'-- No occurence available for {specie}, skipping --')
                    return pd.DataFrame()
                else:
                    print(f'Processing geodata for {specie} {specie.index}')

                    # Read occurences data as dataframe 
                    

                    # Transform df in geopandas using Lat/Long info
                    occ_gdf = df_to_gdf(occ_df)
                    # Assign region based on geo coordinate
                    occ_gdf = gpd_assign_region(occ_gdf)
                    # Find closest data point and assign geo data to occurence
                    occ_gdf = assign_geodata_to_occurences(occ_gdf, specie)
                    # Convert back to standard dataframe
                    #occ_df = gdf_to_df(occ_gdf)

                    # Calculate ecology data such as shannon Index and richness Index
                    occ_gdf = ecology_factors(occ_gdf)

                    # Save df to file 
                    utilities.saveDfToCsv(occ_gdf, specie.geodata_file)

                    return occ_gdf
            else:
                return pd.DataFrame()


        elif os.path.exists(specie.geodata_file):

            print('Geodata already processed for occurences and saved to ')
            print(specie.geodata_file)
            occ_df = pd.read_csv(specie.geodata_file)
            utilities.convert_string_to_numeral(occ_df)

            return occ_df
    else:
        print(f'Occurences not downloaded for {specie}')
        print('Use the gbif module to get this data ')
        

def main(species_instances, dry_run, overwrite, use_processed_geo_only):
    # Create temp df for final export
    meta_occ_df = pd.DataFrame()

    if os.path.exists('data/output/allOccurences.csv'):
        print('AllOccurences already on disk')
        if overwrite:
            print('Overriding AllOccurences')
            # Get processed dataframe of all occurences, append to final df
            for specie in species_instances:
                occ_df = process_specie_geodata(specie,use_processed_geo_only)
                if occ_df.empty:
                    pass
                meta_occ_df = pd.concat([meta_occ_df, occ_df])
            
            if not dry_run:
                utilities.saveDfToCsv(meta_occ_df, 'data/output/allOccurences.csv')
            elif dry_run:
                print(meta_occ_df)
        else:
            print('Not overwritting, keeping current file ')


if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser(prog = 'Geo data procesing',
                                     description= "Assigns environmental variables to specie's occurences"
                                     )
    parser.add_argument('-f', '--file', help = 'Location of species list', type = str, default = 'data/input/species_list.csv')
    parser.add_argument('-l', '--length', help = 'Number of species to request from list', type = int, default = 5 )
    parser.add_argument('--dry_run', help = 'Run but do not save the final data', action ='store_true', default = False ) 
    parser.add_argument('-ow', '--overwrite', help = 'Overwrite final df', action ='store_true', default = True ) 
    parser.add_argument('--range', help = 'Specify species_list range to load ', default = None )       
     
    args = parser.parse_args()

    print('## No arguments specified, reverting to defaults ##')
    print(f'Species list location : {args.file}')
    print(f'Processing occurences data for {args.length} species')

    if args.range != None:
        species_list_range = utilities.interpret_args_range(args.range)
    else: 
        species_list_range = None

    override = not args.dry_run

    species_instances = sp.create_species(species_file= args.file,length = args.length, species_list_range = species_list_range)
    main(species_instances,override)
    plt.show()
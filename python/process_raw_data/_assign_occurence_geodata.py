import os, re, sys
import pandas as pd
import geopandas as gpd
import numpy as np
from scipy.spatial import cKDTree
import rasterio 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from python.species import create_species as sp
import python.utils as utils

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

    regions_perimetre_file = 'data/input/geodata/regions_perimetre/regions_perimetre.shp'

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

def sample_forest_composition(occ_gdf, specie):

    forest_composition_path = 'data/input/geodata/forest_composition'

    print('')
    print('Feeding {} occurences to populate with forest composition geodata'.format(len(occ_gdf)))
    final_gdf = gpd.GeoDataFrame()

    #list all regions to iterate over
    region_code_list = []

    for region in os.listdir(forest_composition_path):
        region_code = region.split('.')[0]
        region_code_list.append(region_code)

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
            local_occurrences = occ_gdf[(occ_gdf['region_code']==region_code)]

            # Check if any occurence in this region, otherwise skip to next
            if len(local_occurrences) != 0:

                print('{} {} occurences in {} (Species index {})'.format(len(local_occurrences), specie.name, region_code, specie.index))
                print(region_code + ' ({}/{})'.format(idx+1, len(region_code_list)))
                # Build path to read env factors data of region

                # Create dataframe from forest composition data of region 

                df = pd.read_csv(f'{forest_composition_path}/{region_code}.csv')
                # Reformat as gdf using xy as geometry
                local_gdf = df_to_gdf(df, xy = ['X','Y'])

                # Find nearest point from occurence localisation and merge data
                gdf = ckdnearest(local_occurrences, local_gdf)
               
                #remove distance collumn from ckdnearest function, could be used for debug but not necessary in final 
                #gdf = gdf.drop(columns=['dist'])

                #return region gdf as partial gdf to final_gdf
                final_gdf = pd.concat([final_gdf, gdf])

            else:
                print(' - 0 occurences in {} - '.format(region_code))
                continue
            
    return final_gdf
 
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

def processs_forest_ecology_indexes(df):

    # Convert tree cover string to dictS
    utils.convert_string_to_numeral(df)

    df['tree_diversity_index'] = df['tree_cover'].apply(richnessIndex) 
    df['tree_shannon_index'] = df['tree_cover'].apply(shannonIndex)

    return df 

def sample_bioclim(gdf):
    # 19 bioclim layers
    biolcim_layers = range(1,20)
    # create coordinate list for occurences
    coord_list = [(x,y) for x,y in zip(gdf['geometry'].x, gdf['geometry'].y)]

    for layer in biolcim_layers:
        layer = str(layer)
        layer = layer.zfill(2)
        raster= rasterio.open(f'data/input/geodata/bioclim/QC_bio_{layer}.tif')

        gdf[f'bioclim_{layer}'] = [x for x in raster.sample(coord_list)]

    return gdf

def get_all_occurence_geodata(specie,use_processed_geo_only):
    
    # First check if occurences are downloaded for this specie
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

                    
                    # Transform df in geopandas using Lat/Long info
                    occ_gdf = df_to_gdf(occ_df)
                    # Assign region based on geo coordinate
                    occ_gdf = gpd_assign_region(occ_gdf)
                    # Find closest data point and assign forest composition data to occurence
                    occ_gdf = sample_forest_composition(occ_gdf, specie)

                    # Calculate tree stand ecology index (shannon Index and richness Index)
                    occ_gdf = processs_forest_ecology_indexes(occ_gdf)

                    occ_gdf = sample_bioclim(occ_gdf)

                    # Save df to file 
                    utils.saveDfToCsv(occ_gdf, specie.geodata_file)

                    return occ_gdf
            else:
                return pd.DataFrame()


        elif os.path.exists(specie.geodata_file):

            print('Geodata already processed for occurences and saved to ')
            print(specie.geodata_file)
            occ_df = pd.read_csv(specie.geodata_file)
            utils.convert_string_to_numeral(occ_df)

            return occ_df
    else:
        print(f'Occurences not downloaded for {specie}')
        print('Use the gbif module to get this data ')
        
def main(species_instances, dry_run, overwrite, use_processed_geo_only):
    # Create temp df for final export
    meta_occ_df = pd.DataFrame()
    print('Checking if all species occurences are already on disk')
    if not os.path.exists('data/occurences/sampledOccurences.csv'):
        print('All Species occurences already on disk')
        # Get processed dataframe of all occurences, append to final df
        for specie in species_instances:
            occ_df = get_all_occurence_geodata(specie,use_processed_geo_only)
            if occ_df.empty:
                pass
            meta_occ_df = pd.concat([meta_occ_df, occ_df])
        
        if not dry_run:
            utils.saveDfToCsv(meta_occ_df, 'data/occurences/sampledOccurences.csv')
        elif dry_run:
                print(meta_occ_df)
    

        


if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser(prog = 'Geo data procesing',
                                     description= "Assigns environmental variables to specie's occurences"
                                     )
    parser.add_argument('-f', '--file', help = 'Location of species list', type = str, default = 'data/input/table/species_list.csv')
    parser.add_argument('-l', '--length', help = 'Number of species to request from list', type = int, default = 5 )
    parser.add_argument('--dry_run', help = 'Run but do not save the final data', action ='store_true', default = False ) 
    parser.add_argument('-ow', '--overwrite', help = 'Overwrite final df', action ='store_true', default = True ) 
    parser.add_argument( '--redo_species_geo', help = 'Delete and reprocess each species geodata', action ='store_true', default = False )
    parser.add_argument( '--use_processed_geo_only', help = 'Use already processed geo data only', action ='store_true', default = False ) 

    parser.add_argument('--range', help = 'Specify species_list range to load ', default = None )       
     
    args = parser.parse_args()

    # Interpret arguments
    if args.range != None:
        print('Using range')
        species_list_range = utils.interpret_args_range(args.range) 
    else: 
        species_list_range = None

    dry_run = args.dry_run
    overwrite = args.overwrite

    print(f'Species list location : {args.file}')

    print(f'Requesting {args.length} species')
    species_instances = sp.create_species(species_file= args.file,length = args.length, species_list_range = species_list_range)
    print('running main')
    main(species_instances,dry_run, overwrite, args.use_processed_geo_only)

    # run main data preprocessing pipeline 
import os
import pandas as pd
import geopandas as gpd
import argparse



# Load main moodule & submodules 
from mycoMap.dataPreprocessing import *

RAW_OCCURENCES_PATH = 'data/raw/occurences/allOcurrences.csv'
GRID_PATH = 'data/interim/geodata/vector/geoUtils/0.5km_grid.shp'

CLEANED_OCCURENCES_PATH = 'data/interim/occurences/filteredOcurrences.csv'
SJOIN_OCCURENCES_PATH = 'data/interim/occurences/griddedOccurences.csv'

SAMPLED_BIOCLIM_PATH = 'data/interim/geodata/vector/sampledBioclim/0.5km_bioclim.shp'
SUBSETS_OUTPUT_PATH = 'data/interim/geodata/vector/sampled_grid/'

INTEGRATED_DATA_OUTPUT_PATH = 'data/interim/geodata/vector/allIntegratedData/'

def overwriteDecisionTree(file, overwrite:bool):
        
    if os.path.isfile(file):
        if overwrite:
            return True
        else:
            return False
    else:
        return True
    

def fullPipeline(regions_list, overwriteFinal = False, overwriteForetOuvert = False, overwriteOccurences = False, overwriteGrid = False):

    integratedDataFile = INTEGRATED_DATA_OUTPUT_PATH + 'allIntegratedData.csv'

    # Check if final file already created, overwrite if wanted
    if overwriteDecisionTree(integratedDataFile, overwrite=overwriteFinal):

        ######################## GRID DATA PREPROCESS ###########################

        # Cluster grid for ml model later 
        clustered_grid_path = dataTransformation.main.clusterGrid(GRID_PATH, overwrite = overwriteGrid)
        # Load grid for spatial joins
        print('Reading grid file')
        grid = gpd.read_file(clustered_grid_path)

        ########################### FORET OUVERTE DATA PREPROCESS ###########################

        # Check if subsets already preprocessed, recreate list
        subsets_to_process = []

        for region in regions_list:
            if os.path.isfile(SUBSETS_OUTPUT_PATH + f'{region}_grid.shp'):
                if overwriteForetOuvert:
                    subsets_to_process.append(region)
                else:
                    pass
            else:
                subsets_to_process.append(region)

        removed_subsets = int(len(regions_list) - len(subsets_to_process))
        print(f'Filtered subsets list after checking if main aggregation is on disk. Removed {removed_subsets}')
        if len(subsets_to_process) > 0:
            print(subsets_to_process)

        # Import ForetOuverte layers and write to disk 

        for region in subsets_to_process:
            # Cleaning
            cleaned_foretOuvert_gdf, perimeter_gdf = dataCleaning.main.cleanForetOuverteData(region, overwrite = overwriteForetOuvert, verbose = False)
            # Transormation & Encoding 
            encoded_foretOuvert_gdf = dataTransformation.main.encodeForetOuverteData(cleaned_foretOuvert_gdf, region, verbose = True)

            # Main integration, aggregating all subset data to grid cell and saving to disk  
            subset_integrated_data_path = dataIntegration.main.aggregateForetOuverteData(encoded_foretOuvert_gdf, perimeter_gdf,grid, region, SUBSETS_OUTPUT_PATH, write = True)

        # Read all integrated data and merge in one to combine with fungi + bioclim
        
        subset_integrated_data_path = SUBSETS_OUTPUT_PATH + 'csv/'
        gdf = dataIntegration.main.combineAllSubsets(subset_integrated_data_path)

        ########################### OCCURENCES DATA PREPROCESS ###########################

        # Cleaning
        cleaned_occ_df = dataCleaning.main.cleanOccurencesData(RAW_OCCURENCES_PATH, CLEANED_OCCURENCES_PATH, overwrite = overwriteOccurences)

        # Spatial join of occurences to grid cells 
        sjoin_occurences_df = dataIntegration.spatialJoinOccurences.main(CLEANED_OCCURENCES_PATH, GRID_PATH, SJOIN_OCCURENCES_PATH, overwrite = overwriteOccurences)

        # Process fungi ecology indexes on sjoined occurences 
        fungi_ecology_gdf = dataIntegration.main.process_fungi_ecology_index(sjoin_occurences_df, grid)

        ########################### BIOCLIM DATA PREPROCESS ###########################
        print('Reading Bioclim data')
        bioclim_gdf = gpd.read_file(SAMPLED_BIOCLIM_PATH)

        ########################### MERGE ALL INTEGRATED DATA ###########################

        dataToMerge = [gdf,fungi_ecology_gdf, bioclim_gdf]

        allData_gdf = dataIntegration.main.mergeAllDataset(grid, dataToMerge, output_path= INTEGRATED_DATA_OUTPUT_PATH, write = overwriteFinal)
        allData_df = utils.gdf_to_df(allData_gdf)

    else:
        print('Processed data on disk reading back')
        allData_df = pd.read_csv(integratedDataFile)

    print(allData_df)


if __name__ == '__main__':

    from mycoMap import utils 

    parser = argparse.ArgumentParser()
    parser.add_argument('--overwriteFinal',required=False,action='store_true')
    parser.add_argument('--overwriteForetOuvert',required=False,action='store_true')
    parser.add_argument('--overwriteOccurences',required=False,action='store_true')
    parser.add_argument('--overwriteGrid',required=False,action='store_true')
    parser.add_argument('--subset', type=tuple, required=False)

    args = parser.parse_args()

    # Data is split in subsets (geographical regions)
    # Setup subset to process     
    if args.subset:
        regions_list = utils.get_regionCodeList(range = args.subset, verbose= True)
    else: 
        regions_list = utils.get_regionCodeList(range = (0,17), verbose= True)

    # If any overwrite other than final is triggered, force overwriteFinal 
    overwriteFinal = args.overwriteFinal
    for arg_name, arg_value in vars(args).items():
        if arg_value == True:
            overwriteFinal = True
        else:
            pass
    
    fullPipeline(regions_list, overwriteFinal,args.overwriteForetOuvert,args.overwriteOccurences,args.overwriteGrid)





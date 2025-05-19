# run main data preprocessing pipeline 
import geopandas as gpd

# Data is split in subsets (geographical regions)
# Setup subset to process 
from mycoMap import utils 
regions_list = utils.get_regionCodeList(range = (0,1), verbose= True)

# Load main moodule & submodules 
from mycoMap.dataPreprocessing import *

RAW_OCCURENCES_PATH = 'data/raw/occurences/allOcurrences.csv'
GRID_PATH = 'data/interim/geodata/vector/geoUtils/0.5km_grid.shp'

CLEANED_OCCURENCES_PATH = 'data/interim/occurences/filteredOcurrences.csv'
SJOIN_OCCURENCES_PATH = 'data/interim/occurences/griddedOccurences.csv'


############ Data Cleaning ###############

# Import ForetOuverte layers and write to disk 

# Foret Ouverte Cleaning
cleaned_foretOuvert_gdfs, perimeter_gdfs = dataCleaning.main.cleanForetOuverteData(regions_list, overwrite = False, verbose = False)

# Occurences Cleaning
cleaned_occ_df = dataCleaning.main.cleanOccurencesData(RAW_OCCURENCES_PATH, CLEANED_OCCURENCES_PATH, overwrite = False)

############ Data Transformation ###############

# Foret Ouverte Encoding
encoded_foretOuvert_gdfs = dataTransformation.main.encodeForetOuverteData(cleaned_foretOuvert_gdfs, verbose = True)

# Cluster grid 
clustered_grid_path = dataTransformation.main.clusterGrid(GRID_PATH, overwrite = False)


############ Data Integration ###############

# Load grid 

grid = gpd.read_file(clustered_grid_path)

# Spatial join of occurences to grid cells 
sjoin_occurences_df = dataIntegration.spatialJoinOccurences.main(CLEANED_OCCURENCES_PATH, GRID_PATH, SJOIN_OCCURENCES_PATH, overwrite = True)

# Process fungi ecology indexes on sjoined occurences 
fungi_ecology_gdf = dataIntegration.main.process_fungi_ecology_index(sjoin_occurences_df, grid)

# Merging all subsets data to aggregate 
merged_subsets = dataIntegration.main.mergeSubsets(encoded_foretOuvert_gdfs, perimeter_gdfs)


# Main integration, aggregating data in one source 

#integrated_data_path = dataIntegration.main.aggregateForetOuverte(merged_subsets, grid)



# integration 

#reduction 





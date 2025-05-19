# run main data preprocessing pipeline 

# Data is split in subsets (geographical regions)

# Setup subset to process 
from mycoMap import utils 
regions_list = utils.get_regionCodeList(range = (0,1), verbose= True)

# Load main moodule & submodules 
from mycoMap.dataPreprocessing import *

RAW_OCCURENCES_PATH = 'data/raw/occurences/allOcurrences.csv'
GRID_PATH = 'data/interim/geodata/vector/geoUtils/0.5km_grid.shp'

cleaned_occurences_path = 'data/interim/occurences/filteredOcurrences.csv'


############ Data Cleaning ###############

# Import ForetOuverte layers and write to disk 

# Foret Ouverte Cleaning
cleaned_foretOuvert_gdfs, perimeter_gdf= dataCleaning.main.cleanForetOuverteData(regions_list, overwrite = False, verbose = False)

# Occurences Cleaning
cleaned_occ_df = dataCleaning.main.cleanOccurencesData(RAW_OCCURENCES_PATH, cleaned_occurences_path, overwrite = False)

############ Data Transformation ###############

# Foret Ouverte Encoding
encoded_foretOuvert_gdfs = dataTransformation.main.encodeForetOuverteData(cleaned_foretOuvert_gdfs, verbose = True)

# Cluster grid 
clustered_grid_path = dataTransformation.main.clusterGrid(GRID_PATH, overwrite = False)


############ Data Integration ###############

# Main integration, aggregating data in one source 

#integrated_data_path = dataIntegration.main.main()



# integration 

#reduction 





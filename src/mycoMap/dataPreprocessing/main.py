# run main data preprocessing pipeline 

# Data is split in subsets (geographical regions)

# Setup subset to process 
from mycoMap import utils 
regions_list = utils.get_regionCodeList(range = (0,1), verbose= True)

# Load main moodule & submodules 
from mycoMap.dataPreprocessing import *

OCCURENCES_CSV_PATH = 'data/raw/occurences/allOcurrences.csv'
GRID_PATH = 'data/interim/geodata/vector/geoUtils/0.5km_grid.shp'

############ Data Cleaning ###############

# Foret Ouverte Cleaning
cleaned_foretOuvert_gdfs = dataCleaning.main.cleanForetOuverteData(regions_list, verbose = False)

# Occurences Cleaning
cleaned_occ_df = dataCleaning.main.cleanOccurencesData(OCCURENCES_CSV_PATH, write = True)

############ Data Transformation ###############

# Foret Ouverte Encoding
encoded_foretOuvert_gdfs = dataTransformation.main.encodeForetOuverteData(cleaned_foretOuvert_gdfs, verbose = True)

# Cluster grid 

clustered_grid_path = dataTransformation.main.clusterGrid(GRID_PATH)


############ Data Integration ###############

# Main integration, aggregating data in one source 



# integration 

#reduction 





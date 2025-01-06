from occurences import searchOccurences, get_download_zip, create_occurences_dataframe
from specie import create_specie
import geodata
from  tools import saveDfToCsv

import pandas as pd
import os

#Readable inaturalist links
pd.set_option('display.max_colwidth', 1000)

# Used to check if occurence file exists
occurences_file = None

specie_query = 'Cantharellus enelensis'

#Create specie object based on query name - Using gbif specie module
specie = create_specie(specie_query, rank = 'Species')


# xxxxxxxxxxxxxx Could be in one main function running from occurences.py and returning dataframe for rest xxxxxxxxxxxx

# Check if occurence download has already been made for specific specie
if 'download_key.txt' not in os.listdir('data/gbifQueries/{}'.format(specie.name)):
    # Create occurence request
    searchOccurences(specie, download = True)

else:
    print('Occurence request already made for {}.'.format(specie.name))
    print('Trying to download request to disk using provided key')
    print('')
    #Download request data to disk
    occurences_file = get_download_zip(specie)
    print(occurences_file)
    print('')

# Create dataframe based on occurences
if occurences_file != None:
    occ_df = create_occurences_dataframe(occurences_file)

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

occ_gdf = geodata.df_to_gdf(occ_df)

occ_gdf = geodata.gpd_assign_region(occ_gdf)
# debug
#loosing some occurences in asign regions ??
# check which by assigning new index collumns and compare with previous gdf
# check if occurence just too far from forest points 

#occ_gdf = occ_gdf.head(1)
occ_gdf = geodata.assign_geodata_to_occurences(occ_gdf)

#debug - could make loading region cv faster, complaining about columns (11,30) datatype 
# -Specify dtype option on import
# Convert back to simple df 
occ_df = geodata.gdf_to_df(occ_gdf)

output_path = occurences_file[:-4] + '_geodata.csv'
f = saveDfToCsv(occ_df, output_path)


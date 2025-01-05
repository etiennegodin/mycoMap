from occurences import searchOccurences, get_download_zip, create_occurences_dataframe
from specie import create_specie
import geodata
import geodata

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
#loosing some occurences in asign regions ??

#occ_gdf = occ_gdf.head(1)
occ_gdf = geodata.find_nearest_point(occ_gdf)

occ_df = geodata.gdf_to_df(occ_gdf)


print(occ_df)
print(type(occ_df))
#occ_df['values'] = occ_df.apply(populate_occurence_data(occ_gdf), axis = 1)
#occ_gdf['values'] = occ_gdf.apply(lambda row: populate_occurence_data(row), axis = 1)


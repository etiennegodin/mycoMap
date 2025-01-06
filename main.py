import occurences  
from specie import create_specie
import geodata
import tools
import occurence_stats


import pandas as pd
import os

#Readable inaturalist links
pd.set_option('display.max_colwidth', 1000)

# Path to story gbif queries
gbif_queries_path = 'data/gbifQueries/'

# Used to check if occurence file exists
occurences_file = None
geo_data_file_path = None
specie_query = 'Amanita muscaria'

#Create specie object based on query name - Using gbif specie module
specie = create_specie(specie_query, rank = 'Species')

# xxxxxxxxxxxxxx Could be in one main function running from occurences.py and returning dataframe for rest xxxxxxxxxxxx

# Check if occurence download has already been made for specific specie
specie_path = gbif_queries_path + specie.name + '/'
download = False

if download == True:

    occurences.searchOccurences(specie, download = True)

    if 'download_key.txt' in os.listdir(specie_path):
        print('Occurence request already made for {}'.format(specie.name))

        print('Trying to download request to disk using provided key')
        print('')
        #Download request data to disk
        occurences_file = occurences.get_download_zip(specie)

        if occurences_file == None:
            pass
        else:
            occ_df = occurences.create_occurences_dataframe(occurences_file)

            # Expected geodata file location
            geo_data_file_path = occurences_file[:-4] + '_geodata.csv'

            if not os.path.exists(geo_data_file_path):
                # Transform df in geopandas using Lat/Long info
                occ_gdf = geodata.df_to_gdf(occ_df)
                # Assign region based on geo coordinate
                occ_gdf = geodata.gpd_assign_region(occ_gdf)
                # Find closest data point and assign geo data to occurence
                occ_gdf = geodata.assign_geodata_to_occurences(occ_gdf)
                # Convert back to standard dataframe
                occ_df = geodata.gdf_to_df(occ_gdf)

                # Interpet mixed rows 
                #occ_df =  geodata.interpet_env_factors()
                
                # Save occurences geodata to file
                tools.saveDfToCsv(occ_df, geo_data_file_path)
                
            else:
                print('Geodata already processed for occurences')
                print(geo_data_file_path)

                # Import geodata as dataframe
                df = pd.read_csv(geo_data_file_path)
                # Convert tree_cover columns to dict (read as string by pd.read_csv)
                df = tools.convert_tree_cover_data_type(df)

                occurence_stats.lnr_reg(df)


                # Perform stats on occurences using geo data 
        



    else:
        pass

        
else: 
    occurences.searchOccurences(specie, download = False)

print(occurences_file)
# Create dataframe based on occurences

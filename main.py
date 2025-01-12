from  occurences import search_occurences, occurences_request, get_occurences_download, create_occurences_dataframe
from specie import create_specie
from  geodata import geo 
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
specie_query = 'Laetiporus sulphureus'

#Create specie object based on query name - Using gbif specie module
specie = create_specie(specie_query, rank = 'Species')

# xxxxxxxxxxxxxx Could be in one main function running from occurences.py and returning dataframe for rest xxxxxxxxxxxx

# Check if occurence download has already been made for specific specie
specie_path = gbif_queries_path + specie.name + '/'
download = True


if download == True:

    # Create folder for species data
    path = tools.create_folder(specie_path)

    # Add path specie instance to re-use later 
    specie.set_path(path)

    # Create a query to gbif to download species occurence
    # Download query key is returned 
    
    download_key_path, download_key  = occurences_request(specie)

    # Add path specie instance to re-use later 
    specie.set_download_key(download_key)

    # Download occurences data requested to disk 
    occurences_file = get_occurences_download(specie, unzip= True)

    # Create dataframe from downloaded occurence data 
    occ_df = create_occurences_dataframe(occurences_file)

    # Assign geodata to occurences 
    occ_df = geo(occ_df, specie)

    # Analysis 


    #occurence_stats.lnr_reg(occ_df)

        
else: 

    search_occurences(specie)


# Create dataframe based on occurences


# Could split in separate scripts

# 0 find species 
#find species with most occurence, create list ( exploaratory in this script)

#1 download data ( first portion of this main.py)
#make iterable if fed list of species from exploratory phase

#2 get data run only when confirmation of gbif , could make fancy trigger, like query email of gbif account 
# include geo data anylissis in get_data script)
#iterable too


#account for fact thta occurens are human and flaws ( only in cities or near centers 
#entropy concept ???



#3 analysis only - could include iterating over acquired species ( by group) 
# list of all dirs in gbifQueries an iterate over to do stats and find multiple ocrelation 
# could help define most influencal factors fro groups of mushroom instaed of juste one specifc
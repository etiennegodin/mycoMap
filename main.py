from  occurences import read_occurence_data, create_occurences_dataframe
from specie import create_specie
from  geodata import geo 
import tools
from data_analysis import prepare_data, exploratory_data_analysis


import pandas as pd
import os

#Readable inaturalist links
pd.set_option('display.max_colwidth', 1000)

# Path to story gbif queries
gbif_queries_path = 'data/gbifQueries/'
species_list_file = 'data/input/species_list.csv'

def create_species_list(species_list_file, length = None):

    df_species = pd.read_csv(species_list_file)

    if length != None:
        df_species = df_species.head(length)

    species_list = list(df_species['Species'])
    print(species_list)

    return species_list

def create_species_instances(species_list):

    species_instances = []
    for specie_name in species_list:
        specie = create_specie(specie_name, rank = 'Species')
        species_instances.append(specie)

    return species_instances

def create_species_data(specie):
    # Define path for specie data
    specie_path = gbif_queries_path + specie.name + '/'

    # Create folder for specie data
    path = tools.create_folder(specie_path)

    # Add path specie instance to re-use later 
    specie.set_path(path)


    # Create occurences data
    occ_df = read_occurence_data(specie)


    # Create dataframe 
    if not occ_df.empty:
        print(' ### Processing geo_data for {}'.format(specie.name))
        # Assign geodata to occurences 
        occ_df = geo(occ_df, specie)
        pass
    
    elif occ_df.empty:
        print(' ### {} occurence data not on file skipping geo_processing '.format(specie.name))
        pass
    





species_list = create_species_list(species_list_file, length = 10)

species_instances = create_species_instances(species_list)

for idx, specie in enumerate(species_instances):
    specie.set_loop_index(idx)
    print(' ############################## {} ############################## '.format(specie.name))
    occ_df = create_species_data(specie)



'''



print(occ_df.head())
df = prepare_data(occ_df)
exploratory_data_analysis(df)

'''




        





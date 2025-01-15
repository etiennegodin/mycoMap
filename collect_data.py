from  data_occurences import read_occurence_data, create_occurences_dataframe
from data_specie import create_specie
from data_prepare import prepare_data
from  data_geo import geo 
import tools
import os
import pandas as pd

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
        return occ_df
    
    elif occ_df.empty:
        print(' ### {} occurence data not on file skipping geo_processing '.format(specie.name))
        pass
    
if __name__ == '__main__':

    species_name_list = create_species_list(species_list_file, length = 15)

    species_instances = []

    meta_occ_df = pd.DataFrame()

    for idx, specie_name in enumerate(species_name_list):

        specie = create_specie(specie_name, rank = 'Species')
        print(' ############################## {} ############################## '.format(specie.name))

        occ_df = None
        specie.set_loop_index(idx)
        species_instances.append(specie)

        geodata_file = gbif_queries_path + '{}/{}_geodata.csv'.format(specie.name, specie.name)

        if not os.path.exists(geodata_file):
            occ_df = create_species_data(specie)
        else:
            occ_df = pd.read_csv(geodata_file)s
        
        meta_occ_df = pd.concat([meta_occ_df, occ_df])


    print(meta_occ_df)
    tools.saveDfToCsv(meta_occ_df, 'data/output/allOccurences.csv')

'''



print(occ_df.head())
df = prepare_data(occ_df)
exploratory_data_analysis(df)

'''




        





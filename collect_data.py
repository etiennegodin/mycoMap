from  data_occurences import read_occurence_data, create_occurences_dataframe
import specie
from gbif import gbif
from data_prepare import prepare_data
from  data_geo import geo 
import utilities
import os
import pandas as pd

#Readable inaturalist links
pd.set_option('display.max_colwidth', 1000)

# Path to story gbif queries
gbif_queries_path = 'data/gbifQueries/'
species_list_file = 'data/input/species_list.csv'

def create_species_name_list(species_list_file, length = None):

    df_species = pd.read_csv(species_list_file)

    if length != None:
        df_species = df_species.head(length)

    species_list = list(df_species['Species'])
    print(species_list)

    return species_list

def create_species_data(specie):

    print('Creating data for {}'.format(specie.name))
    # Define path for specie data
    specie_path = gbif_queries_path + specie.name + '/'

    # Create folder for specie data
    path = utilities.create_folder(specie_path)

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

    # Create species_name list 
    species_name_list = create_species_name_list(species_list_file, length = 30)

    # Create final dataframe to output all species occurences
    meta_occ_df = pd.DataFrame()

    # Create list of species object
    species_instances = specie.create_species(species_name_list)

    # Handle gbif download and get queries 
    gbif(species_instances)




    '''
    idx = 0 
    while idx < len(species_instances):
        for idx, specie_instance in enumerate(species_instances):

            print('Looping through species')
            print('{} with index {}'.format(specie.name, idx))

            geodata_file = gbif_queries_path + '{}/{}_geodata.csv'.format(specie.name, specie.name)

            if not os.path.exists(geodata_file):
                occ_df = create_species_data(specie)
            else:
                print('Data for {} already on file, adding to all occurences'.format(specie.name))
                occ_df = pd.read_csv(geodata_file)
            
            meta_occ_df = pd.concat([meta_occ_df, occ_df])
            idx += 1

            if idx == len(species_instances):
                break
        
        
        


    print(meta_occ_df)
    tools.saveDfToCsv(meta_occ_df, 'data/output/allOccurences.csv')

'''






        





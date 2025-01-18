from  data_occurences import read_occurence_data, create_occurences_dataframe
import specie as sp 
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




if __name__ == '__main__':

    # Create species_name list 
    species_name_list = sp.create_species_name_list(species_list_file, length = 37)

    # Create final dataframe to output all species occurences
    meta_occ_df = pd.DataFrame()

    # Create list of species object
    species_instances = sp.create_species(species_name_list)

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






        





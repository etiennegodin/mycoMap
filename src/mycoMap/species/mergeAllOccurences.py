import pandas as pd 
import os, sys

from . import specie as sp 
from .. import utils 
if __name__ == '__main__':

    species_list_file = 'data/species/output/species_list.csv'

    print(f'Creating species obejct from {species_list_file}')
    species_instances = sp.create_species_instances(species_file= species_list_file)

    allOcurrences_df = pd.DataFrame()
    for specie in species_instances:
        print(specie.occurence_file)
        try:
            ocurrences_df = pd.read_csv(specie.occurence_file, delimiter = '\t')
            ocurrences_df = ocurrences_df[ocurrences_df.countryCode == 'CA']
            ocurrences_df = ocurrences_df[ocurrences_df.stateProvince == 'Québec']
            allOcurrences_df = pd.concat([allOcurrences_df, ocurrences_df])
        except:
            pass
    print(allOcurrences_df)
    utils.saveDfToCsv(allOcurrences_df, 'data/interim/species/allOcurrences.csv')
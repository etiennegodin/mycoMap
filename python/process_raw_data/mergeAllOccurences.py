import pandas as pd 
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from python.species import create_species as sp
import python.utils as utils

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser(prog = 'Geo data procesing',
                                     description= "Assigns environmental variables to specie's occurences"
                                     )
    parser.add_argument('-f', '--file', help = 'Location of species list', type = str, default = 'data/input/table/species_list.csv')
    parser.add_argument('-l', '--length', help = 'Number of species to request from list', type = int, default = 500 )
    parser.add_argument('--range', help = 'Specify species_list range to load ', default = None )       
     
    args = parser.parse_args()

    # Interpret arguments
    if args.range != None:
        print('Using range')
        species_list_range = utils.interpret_args_range(args.range) 
    else: 
        species_list_range = None

    print(f'Species list location : {args.file}')

    print(f'Requesting {args.length} species')
    species_instances = sp.create_species(species_file= args.file,length = args.length, species_list_range = species_list_range)
    print('running main')

    allOcurrences_df = pd.DataFrame()
    for specie in species_instances:
        print(specie.occurence_file)
        try:
            ocurrences_df = pd.read_csv(specie.occurence_file, delimiter = '\t')
            ocurrences_df = ocurrences_df[ocurrences_df.stateProvince == 'Québec']
            allOcurrences_df = pd.concat([allOcurrences_df, ocurrences_df])
        except:
            pass
    print(allOcurrences_df)
    utils.saveDfToCsv(allOcurrences_df, 'data/occurences/allOcurrences.csv')
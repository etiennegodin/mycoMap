import specie as sp
import geodata
import gbif
import asyncio

import utilities
import pandas as pd

#Readable inaturalist links
pd.set_option('display.max_colwidth', 1000)

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser(prog = 'Geo data procesing',
                                     description= "Assigns environmental variables to specie's occurences"
                                     )
    parser.add_argument('-f', '--file', help = 'Location of species list', type = str, default = 'data/input/species_list.csv')
    parser.add_argument('-l', '--length', help = 'Number of species to request from list', type = int, default = 5 )
    parser.add_argument('--dry_run', help = 'Run but do not save the final data', action ='store_true', default = False )  
    parser.add_argument('--range', help = 'Specify species_list range to load ', default = None )       
     
    args = parser.parse_args()

    # Interpret arguments
    if args.range != None:
        print('Using range')
        species_list_range = utilities.interpret_args_range(args.range)
    else: 
        species_list_range = None

    override = not args.dry_run


    print(f'Species list location : {args.file}')

    print(f'Requesting {args.length} species')
    species_instances = sp.create_species(species_file= args.file,length = args.length, species_list_range = species_list_range)
    
    gbif_complete = asyncio.run(gbif.main(species_instances))

    if gbif_complete:
        print(f'Processing occurences data for {args.length} species')

        geodata.main(species_instances,override)


import sys
import get_specie as sp
import get_geodata as get_geodata
import get_gbif as get_gbif
import asyncio
import pandas as pd
import utilities
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
    parser.add_argument('-ow', '--overwrite', help = 'Overwrite final df', action ='store_true', default = True ) 
    parser.add_argument( '--redo_species_geo', help = 'Delete and reprocess each species geodata', action ='store_true', default = False )
    parser.add_argument( '--use_processed_geo_only', help = 'Use already processed geo data only', action ='store_true', default = False ) 

    parser.add_argument('--range', help = 'Specify species_list range to load ', default = None )       
     
    args = parser.parse_args()

    # Interpret arguments
    if args.range != None:
        print('Using range')
        species_list_range = utilities.interpret_args_range(args.range) 
    else: 
        species_list_range = None

    dry_run = args.dry_run
    overwrite = args.overwrite

    print(f'Species list location : {args.file}')

    print(f'Requesting {args.length} species')
    species_instances = sp.create_species(species_file= args.file,length = args.length, species_list_range = species_list_range)
    
    gbif_complete = asyncio.run(get_gbif.main(species_instances))

    if gbif_complete:
        print(f'Processing occurences data for {args.length} species')

        if args.redo_species_geo:
            print('Reprocess geo data argument triggered')
            utilities.delete_files_with_suffix('data/gbifQueries', "geodata.csv", length = args.length, dry_run = False)

        get_geodata.main(species_instances,dry_run, overwrite, args.use_processed_geo_only)
        

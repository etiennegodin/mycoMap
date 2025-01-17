from pygbif import occurrences as occ
import utilities
import json
import os
from zipfile import ZipFile
import pandas as pd
import time

gbif_queries_path = 'data/gbifQueries/'

decimal_longitude = '-79.3439314990000071,-63.9999979090000011'
decimal_latitude = '45.0000682390000009, 50.0000022050000013'


def create_occurences_request(specie):

    request_key_path = specie.path + specie.name + '_request_key.txt'
    
    if not os.path.exists(request_key_path):
            
        #Create json query to send to gbif, also writes json
        query = create_gbif_occurence_query(specie,decimal_longitude,decimal_latitude, specie.path )
        request_key = request_occurences(query)

        try:
            request_key = request_occurences(query)
        except:
            print('Reached max simultaneous downloads, waiting 1mim')
            print('data_occurence, line 36')
            time.sleep(60)
        
        else:
            # Write download key to disk
            with open(request_key_path, mode="w", encoding="utf-8") as write_file:
                    write_file.write(request_key)

            return request_key_path, request_key
    
    elif os.path.exists(request_key_path):
        print(' ## Occurences request already made to gbif')

        with open(request_key_path) as write_file:
            request_key = write_file.read()

        
        return request_key_path, request_key

def create_gbif_occurence_query(*args):

    #unpack certain arguments 
    specie = args[0]
    specie_path = args[3]
    

    # list to receive predicate dict
    predicate_list = []

    #Key from specie.key
    predicates_dict = {"HAS_COORDINATE" : True,
               "HAS_GEOSPATIAL_ISSUE" : False,
               "COUNTRY" : "CA", 
               "TAXON_KEY" : specie.key,
               "DECIMAL_LONGITUDE" : args[1],
               "DECIMAL_LATITUDE" : args[2]
               }
    
    for key, value in predicates_dict.items():
        predicate = { "type" : 'equals',
                     "key" : key,
                     "value" : value
                     }
        
        predicate_list.append(predicate)
    

    query = { "type": "and",
            "predicates": predicate_list
    }
    output_json_file = specie_path + specie.name + '.json'

    with open(output_json_file, mode="w", encoding="utf-8") as write_file:
        json.dump(query, write_file)
    #query = json.dumps(query)
    return query

def request_occurences(query):

    downloadQuery = occ.download(queries= query, format= 'SIMPLE_CSV', user = 'egodin', pwd = '4AWkTW8_4D$8q7.', email = 'etiennegodin@duck.com', pred_type='and')
    key = downloadQuery[0]
    return key

def get_occurences_download(specie, unzip = True):

    occurences_dict = occ.download_get(specie.request_key, path = specie.path)
         # Main command to get zip from occurence request key 
        # returns dict with some infos 
        # ex
        # {'path': 'data/gbifQueries/Cantharellus enelensis//0056321-241126133413365.zip',
        #  'size': 12835,
    #  'key': '0056321-241126133413365'}

    # Option to unzip downloaded file
    if unzip == True:

        print('Unziping file')
        zip_file_path = occurences_dict['path']
        #Unzip file
        unzip_occurence_file(zip_file_path, specie.path )

        csv_to_rename_path = specie.path + "{}.csv".format(specie.request_key)
        renamed_file_path = specie.path + "{}.csv".format(specie.name)

        # Rename file from key.csv to specie's name for better readability
        os.rename(csv_to_rename_path,renamed_file_path)
        print(renamed_file_path)
        return renamed_file_path
    else:
        print('Downloaded zip file to {}'.format(occurences_dict['path']))
        return (occurences_dict['path'])
        
    
def unzip_occurence_file(file_path, specie_path):

    with ZipFile(file_path, 'r') as zObject: 
        # Extracting all the members of the zip  
        # into a specific location. 
        zObject.extractall( 
            path = specie_path)
    


def read_occurence_data(specie):

    occurences_file = specie.path + specie.name + '.csv'

    if not os.path.exists(occurences_file):
        occurences_file = create_specie_occurences_data(specie)
    else:
        print(' ## Reading occurence dataset for {})'.format(specie.name))

    try:
        occ_df = create_occurences_dataframe(occurences_file)
        return occ_df
    except:
        occ_df = pd.DataFrame()
        print("Can't read occurence data")
        print(occurences_file)

        return occ_df

def create_specie_occurences_data(specie):
    print(' ## Creating occurence dataset for {} '.format(specie.name))

    # Check if process already made 
    request_key_path = specie.path + specie.name + '_request_key.txt'
    # Add path specie instance to re-use later 

    # Create a query to gbif to request species occurence
    # Request key is returned 
    request_key_path, request_key  = create_occurences_request(specie)
    
    # Set request key to specie's instance to reuse later
    specie.set_request_key(request_key)

    # Download occurences data requested to disk 
    try:
        occurences_file = get_occurences_download(specie, unzip= True)

        # Create dataframe from downloaded occurence data 
        return occurences_file
    except:
        print(' *** Failed to download {} occurences data to disk, try again later *** '. format(specie.name))
        print('data_occurences, line 216')
        #time.sleep(60)
        return None
        
    

def skip_gbif(specie):

    if os.path.exists(specie.specie_occurence_file):
        print('Specie occurence data already requested and downloaded to disk')
        return True

    else:
        return False
    

def prepare_species_gbif(species_instances):
    for specie in species_instances:
        specie_folder = gbif_queries_path + specie.name + '/'

        # Create folder for specie data, if already created returns path 
        specie_folder = utilities.create_folder(specie_folder)
        specie.set_specie_folder(specie_folder)

        # Check if species occurence aready on file 
        specie_occurence_file = specie.folder + specie.name + '.csv'
        specie.set_specie_occurence_file(specie_occurence_file)


        request_key_path = specie.folder + specie.name + '_request_key.txt'
        specie.set_request_key_path(request_key_path)


def gbif(species_instances):

    species_count = len(species_instances)
    prepare_species_gbif(species_instances)

    print('x')
    species_queried = []
    species_downloaded = []

    print(species_count)
    while (len(species_queried) < species_count) and (len(species_downloaded) < species_count):
        for idx, specie in enumerate(species_instances):
            print(len(species_queried), len(species_downloaded))

            active_queries = []

            if skip_gbif(specie):
                species_queried.append(specie)
                species_downloaded.append(specie)

                continue

            # Check if species occurence aready on file  
            if os.path.exists(specie.request_key_path):

                # Read request key 
                print(' ## Occurences request already made to gbif')
                with open(specie.request_key_path) as write_file:
                    request_key = write_file.read()

                specie.set_request_key(request_key)

                species_queried.append(specie)

                if specie.request_key in active_queries:
                    try:
                        get_occurences_download(specie)
                        active_queries.remove(specie.request_key)
                        species_downloaded.append(specie)
                    except:
                        print('Specie requested already but still active and not downloadable')
                        pass

            
            if len(active_queries) == 3:
                    print('Already 3 actives queries, waiting 1min')
                    time.sleep(5)

            if specie.request_key not in active_queries and not os.path.exists(specie.request_key_path):
        
                print('Creating gbif query for specie')
                #Handle json request formatting
                query = create_gbif_occurence_query(specie,decimal_longitude,decimal_latitude, specie.folder )
                request_key = request_occurences(query)

                # Append request key to active 
                active_queries.append(request_key)

                # Write request key to file
                with open(specie.request_key_path, mode="w", encoding="utf-8") as write_file:
                    write_file.write(request_key)

                # Set request key and path on species object
                specie.set_request_key(request_key)

                # Append specie to queried list 
                species_queried.append(specie)

                pass















    

    # check if species data on file 









        








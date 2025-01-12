from pygbif import occurrences as occ

import json
import os
from zipfile import ZipFile
import pandas as pd

gbif_queries_path = 'data/gbifQueries/'

decimal_longitude = '-79.3439314990000071,-63.9999979090000011'
decimal_latitude = '45.0000682390000009, 50.0000022050000013'

def search_occurences(specie):
    limit = 300 
    occurences = occ.search(taxonKey = specie.key, limit= limit, hasCoordinate=True, hasGeospatialIssue = False, decimalLongitude= decimal_longitude, decimalLatitude=decimal_latitude, country = 'CA')
    if occurences['count'] != 0:
        # Message showing how many ocurences found, with limit input
        print("Found {} available occurences for {} in Canada within provided range".format((occurences['count']), specie.name))
    
    else:
        print('Found no occurences for {}'.format(specie.name))

def occurences_request(specie):

    download_key_path = specie.path + specie.name + '_download_key.txt'
    
    if not os.path.exists(download_key_path):
            

        #Create query to send to gbif, also writes json 
        query = create_gbif_occurence_query(specie,decimal_longitude,decimal_latitude, specie.path )
        download_key = download_occurences(query)

        # Write download key to disk
        with open(download_key_path, mode="w", encoding="utf-8") as write_file:
                write_file.write(download_key)

        return download_key_path, download_key
    
    elif os.path.exists(download_key_path):
        print('Download key already exists')

        with open(download_key_path) as write_file:
            download_key = write_file.read()

        
        return download_key_path, download_key

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
    print(specie_path)
    output_json_file = specie_path + specie.name + '.json'

    with open(output_json_file, mode="w", encoding="utf-8") as write_file:
        json.dump(query, write_file)
    #query = json.dumps(query)
    return query

def download_occurences(query):

    downloadQuery = occ.download(queries= query, format= 'SIMPLE_CSV', user = 'egodin', pwd = '4AWkTW8_4D$8q7.', email = 'etiennegodin@duck.com', pred_type='and')
    key = downloadQuery[0]
    return key

def get_occurences_download(specie, unzip = True):

    occurences_file = specie.path + specie.name + '.csv'

    if not os.path.exists(occurences_file):

        occurences = occ.download_get(specie.download_key, path = specie.path)
         # Main command to get zip from occurence request key 
        # returns dict with some infos 
        # ex
        # {'path': 'data/gbifQueries/Cantharellus enelensis//0056321-241126133413365.zip',
        #  'size': 12835,
        #  'key': '0056321-241126133413365'}



        # Option to unzip downloaded file
        if unzip == True:

            print('Unziping file')
            zip_file_path = occurences['path']
            #Unzip file
            file = unzip_occurence_file(zip_file_path, specie.path )

            csv_to_rename_path = specie.path + "{}.csv".format(specie.download_key)
            renamed_file_path = specie.path + "{}.csv".format(specie.name)

            # Rename file from key.csv to specie's name for better readability
            os.rename(csv_to_rename_path,renamed_file_path)
            print(renamed_file_path)
            return renamed_file_path
        else:
            print('Downloaded zip file to {}'.format(occurences['path']))
            return (occurences['path'])
        
    elif os.path.exists(occurences_file):
        print('Occurence request already downloaded, unziped and renamed at {}'.format(occurences_file))
        print('')
        return occurences_file
    

def unzip_occurence_file(file_path, specie_path):

    with ZipFile(file_path, 'r') as zObject: 
        # Extracting all the members of the zip  
        # into a specific location. 
        zObject.extractall( 
            path = specie_path)
    
def create_occurences_dataframe(occurences_file):

    occ_df = pd.read_csv(occurences_file, sep='\t')
    # Cleaning dataframe with only relevant info from occurence query

    occ_df = occ_df[['gbifID', 
                    'decimalLongitude', 
                    'decimalLatitude', 
                    'eventDate',
                    'year',
                    'stateProvince',
                    'species',
                    'occurrenceID']]
    
    # Removing rows not in quebec

    # Specified Canada only but Lat/ Long might make it in Ontario
    occ_df = occ_df[occ_df.stateProvince == 'Québec']

    # Reseting index from removed rows not in qc
    occ_df = occ_df.reset_index(drop=True)

    # Message printing how many occurences were in quebec
    print('From downloaded occurences {} were in Quebec and kept for analysis'.format(len(occ_df)))
    return occ_df


    
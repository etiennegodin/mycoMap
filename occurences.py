import pandas as pd
import geopandas as gpd
from pygbif import occurrences as occ

import json
import os

gbif_queries_path = 'data/gbifQueries/'



def searchOccurences(specie, limit = 300, download = False):

    decimal_longitude = '-79.3439314990000071,-63.9999979090000011'
    decimal_latitude = '45.0000682390000009, 50.0000022050000013'
    
    occurences = occ.search(taxonKey = specie.key, limit= limit, hasCoordinate=True, hasGeospatialIssue = False, decimalLongitude= decimal_longitude, decimalLatitude=decimal_latitude, country = 'CA')

    # Execute dataframe only if found occurences
    if occurences['count'] != 0:
        # Message showing how many ocurences found, with limit input
        print("Found {} available occurences for {} in Canada within provided range".format((occurences['count']), specie.name))
        
        # Dataframe from occurences results
        occ_df = pd.DataFrame.from_dict(occurences['results'])

        # Cleaning dataframe with only relevant info from occurence query
        occ_df = occ_df[['key', 
                        'decimalLongitude', 
                        'decimalLatitude', 
                        'eventDate',
                        'verbatimLocality',
                        'stateProvince',
                        'species',
                        'occurrenceID']]

        # Removing rows not in quebec

        # Specified Canada only but Lat/ Long might make it in Ontario
        occ_df = occ_df[occ_df.stateProvince == 'Québec']
        occ_df = occ_df.reset_index(drop=True)

        # Message printing how many occurences were in quebec
        #print('From {} checked observations {} were in Quebec and kept for analysis'.format(limit, len(occ_df)))
    
    else:
        print('Found no occurences for {}'.format(specie.name))
        occ_df = None

    if download == True:
        #check if path & download query already made ( will create folder)
        if specie.name in os.listdir(gbif_queries_path):
            print('Query already made and download for {}. ({})'.format(specie.name, gbif_queries_path + specie.name))
        else:
            #Define path to create folder to receive download
            specie_path = gbif_queries_path + specie.name
            # Create folder
            os.makedirs(specie_path)

            specie_path = specie_path + '/'

            #Create query to send to gbif, also writes json 
            query = create_gbif_occurence_query(specie,decimal_longitude,decimal_latitude, specie_path )
            key = download_occurences(query)

            # Write download key to disk
            key_file_path = specie_path + 'download_key.txt'
            with open(key_file_path, mode="w", encoding="utf-8") as write_file:
                write_file.write(key)


            file = get_download_zip(key, specie, specie_path)
        return occ_df

    else:
        print('Disabled download of occurences')

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

def get_download_zip(specie):
    specie_path = gbif_queries_path + specie.name + '/'
    key_file_path = specie_path + 'download_key.txt'
    with open(key_file_path) as write_file:
        key = write_file.read()
    print(key)

    occurences = occ.download_get(key, path = specie_path)
    return (occurences)

def processOccurenceDownload():
    #input file from gbif download
    # Dataframe from occurences results
    pass

#occ.download(['GBIF_USER equals "egodin"', 'taxonKey in ["2387246", "2399391","2364604"]', 'year !Null', "issue !in ['RECORDED_DATE_INVALID', 'TAXON_MATCH_FUZZY', 'TAXON_MATCH_HIGHERRANK']"], "SIMPLE_CSV")




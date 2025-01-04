import pandas as pd
import geopandas as gpd
import os 
from pygbif import occurrences as occ
import json

class Predicate:
    def __init__(self, type, key, value):

        self.dict = { "type" : type,
                     "key" : key,
                     "value" : value
        }

        self.key = key 
        self.type = type
        self.value = value
      
    def __str__(self):
        return self.type


def searchOccurences(specie, limit = 300, download = False):

    decimal_longitude = '-79.3439314990000071,-63.9999979090000011'
    decimal_latitude = '45.0000682390000009, 50.0000022050000013'
    
    occurences = occ.search(taxonKey = specie.key, limit= limit, hasCoordinate=True, hasGeospatialIssue = False, decimalLongitude= decimal_longitude, decimalLatitude=decimal_latitude, country = 'CA')

    # Execute dataframe only if found occurences
    if occurences['count'] != 0:

        # Message showing how many ocurences found, with limit input
        print("Found {} available occurences for {} in Canada, limiting to {}".format((occurences['count']), specie.name, limit))

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
        print('From {} checked observations {} were in Quebec and kept for analysis'.format(limit, len(occ_df)))
    
    else:
        print('Found no occurences for {}'.format(specie.name))

    if download == True:
        query = createGbifDownloadQuery(specie.key,decimal_longitude,decimal_latitude, limit)
        x = downloadOccurences(query)
        pass
    else:
        return occ_df

def createGbifDownloadQuery(*args):

    # list of dict
    predicate_list = []

    predicates_dict = {'HAS_COORDINATE' : True,
               'HAS_GEOSPATIAL_ISSUE' : False,
               'COUNTRY' : 'CA', 
               'TAXON_KEY' : args[0],
               'DECIMAL_LONGITUDE' : args[1],
               'DECIMAL_LATITUDE' : args[2]
               }
    

    for key, value in predicates_dict.items():

        predicate = Predicate('equals', key,value)
        #print(predicate.dict)

        predicate_list.append(predicate.dict)
    
    print(predicate_list)

    predicates = json.dumps(predicate_list)

    query = { "type": "and",
  "predicates": predicates
    }

    return query

def downloadOccurences(query):

    #res = occ.download(user = 'egodin', pwd = '4AWkTW8_4D$8q7.', email = 'etiennegodin@duck.com')

    pass



def processOccurenceDownload():
    #input file from gbif download
    # Dataframe from occurences results
    pass

#occ.download(['GBIF_USER equals "egodin"', 'taxonKey in ["2387246", "2399391","2364604"]', 'year !Null', "issue !in ['RECORDED_DATE_INVALID', 'TAXON_MATCH_FUZZY', 'TAXON_MATCH_HIGHERRANK']"], "SIMPLE_CSV")




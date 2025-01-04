import pandas as pd
import geopandas as gpd
import os 
from pygbif import occurrences


def searchOccurences(specie, limit = 300):

    #quebec geomtry as WKT
    '''
    with open("data/geodata/test2.txt", 'r') as file:
        geometry = file.read()
    '''
    decimal_longitude = '-79.3439314990000071,-63.9999979090000011'
    decimal_latitude = '45.0000682390000009, 50.0000022050000013'
    
    occurences = occurrences.search(taxonKey = specie.key, limit= limit, hasCoordinate=True, hasGeospatialIssue = False, decimalLongitude= decimal_longitude, decimalLatitude=decimal_latitude, country = 'CA')


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
        return(occ_df)
    
    else:
        print('Found no occurences for {}'.format(specie.name))


def downloadOccurences():
    pass

def writeOccurencesToFile(currentSpeciesFolder, overwrite = 1, limit = 2):
    if 'occ.csv' not in os.listdir(currentSpeciesFolder):
        #define species

        #get occurences from species gbif
        print('Collecting occurences for {}'.format(speciesName))
        occurences = searchOccurences(speciesGbifKey, limit = limit)

        #cluster occurences within 1km2

        output_path = pdToCsv(occurences, currentSpeciesFolder)
        
    else:
        print('Occurences already gathered for {}'.format(speciesName))
        overwrite = int(input('Do you want to ovewrite? 0/1 '))
        output_path = currentSpeciesFolder + 'occ.csv'

    if overwrite == 1:
        #get occurences from species gbif
        print('Overwrite mode set to 1')
        print('Overwritting occurences for {}'.format(speciesName))
        occurences = searchOccurences(speciesGbifKey, limit = limit)

        #cluster occurences within 1km2
        
        output_path = pdToCsv(occurences, currentSpeciesFolder)
    
    return(output_path)


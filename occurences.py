import pandas as pd
import geopandas as gpd
import os 
from pygbif import occurrences


def searchOccurences(specie, limit = 2, year = '2024'):

    #quebec geomtry as WKT
    '''
    with open("data/geodata/test2.txt", 'r') as file:
        geometry = file.read()
    '''

    
    decimal_longitude = '-79.3439314990000071,-63.9999979090000011'
    decimal_latitude = '45.0000682390000009, 50.0000022050000013'

    occurences = occurrences.search(taxonKey = specie.key, limit= limit, hasCoordinate=True, hasGeospatialIssue = False, decimalLongitude= decimal_longitude, decimalLatitude=decimal_latitude)

    #print(occurences)

    #info kept from query
    occurenceList = []
    occurenceKey = []
    occurenceLon = []
    occurenceLat = []
    occurenceId = []

    print("Found {} available occurences for {} in Quebec, limiting to {}".format((occurences['count']), specie.name, limit))


############broken writting info from occ object to pd ######################
    #cycling through occurences to keep info
    for index, o in enumerate(occurences["results"]):
        occurenceKey.append(o["key"])
        occurenceLon.append( o['decimalLongitude'])
        occurenceLat.append(o["decimalLatitude"])
        occurenceId.append(o["occurrenceID"])

        dict = {
            "occ_key" : occurenceKey,
            "Latitude" : occurenceLat,
            "Longitude" : occurenceLon,
            "occurenceId": occurenceId
        }
    

    occurences = pd.DataFrame.from_dict(dict)
    return(occurences)

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


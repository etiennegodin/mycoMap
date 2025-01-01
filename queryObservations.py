    
#gbif
def defineSpecies(rank = 'species', limit = 1, skipInput = 1, debug = 1):
    if skipInput == 0:
        speciesName = input("Which species to look for ?  ")
    if debug == 1:
        print('debug mode on, using predefined species')
        speciesName = 'Tsuga Canadensis'
        #speciesName = 'Acer Rubrum'


    #catch if name note with space 
    formatNameTest = speciesName.split(' ')
    if len(formatNameTest) == 1:
        speciesName = input('Please type name with space between Genus and Species   ') 

    speciesObject = sp.name_suggest(q=speciesName, rank = rank, limit = 1)
    speciesGbifKey = speciesObject[0]['key']
    speciesName = speciesObject[0]['species']
    return(speciesGbifKey, speciesName)

def searchOccurences(speciesKey, limit = 2):
    #quebec geomtry as WKT
    with open("C:/Users/manat/OneDrive/Documents/botanique/quebecology/data/geodata/vector/frontiereQuebec.txt", 'r') as file:
        quebecGeometry = file.read()
    #gbif query 
    occurences = occSearch(taxonKey = speciesKey, country='CA', limit= limit, hasCoordinate=True, geometry = quebecGeometry )

    #info kept from query
    occurenceList = []
    occurenceKey = []
    occurenceLon = []
    occurenceLat = []
    occurenceId = []

    print("Found {} available occurences for {} in Quebec, limiting to {}".format((occurences['count']), speciesName, limit))

    #cycling through occurences to keep info
    for index, o in enumerate(occurences["results"]):
        occurenceKey.append(o["key"])
        occurenceLon.append( o['decimalLongitude'])
        occurenceLat.append(o["decimalLatitude"])
        occurenceId.append(o["occurrenceID"])

        dict = {
            "key" : occurenceKey,
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


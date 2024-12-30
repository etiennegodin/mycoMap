import pandas as pd
import re
import os

# Clean raw geo data from Foret Ouverte
# Transform desciption of tree cover percentage from string to dict 
 
rawGeoDataPath = './data/input/rawGeoData/'
cleanGeoDataPath = './data/input/cleanGeoData/'


def treeCoverReformat(code):
    # change tree cover infor from string to dict of percentage
    result = re.findall(r'([A-Z]+)(\d+)', code)
    result = dict(result)
    # value from string to %
    for key in result:
        result[key] = int(result[key]) / 100
    return(result)

def cleanRawGeoData(cleanGeoDataPath = cleanGeoDataPath):
    print('Processing tree cover data')

    #Create list with all input files 
    allRegions = []
    for f in os.listdir(rawGeoDataPath):
        allRegions.append(f)
   
    print('Found {} regions to process'.format(len(allRegions)))

    # Go over every file 
    # Isolate region code based on name
    # Apply treeCoverReformat and create new collumn 
    for index, r in enumerate(allRegions):
        print(str(index) + "/" + str(len(allRegions)))

        #Isolate region code based on naming
        #Ex: "CARTE_ECO_MAJ_21E — etage_maj_21e"
        regionCode = r[14:17]
        print('Processing {}'.format(regionCode))

        #Define file path to export treeCover data
        filecleanGeoDataPath = cleanGeoDataPath + 'CARTE_ECO_MAJ_{}.csv'.format(regionCode)
        #path to export final data
        df = pd.read_csv(rawGeoDataPath + r )
        # Apply main logic converting string to dict with tree percentage
        df['tree_cover'] = df['eta_ess_pc'].apply(treeCoverReformat)
        df.to_csv(filecleanGeoDataPath, index=False) 
        print('writing {}'.format(filecleanGeoDataPath))

    print("Processed all raw geo data inputs")

def processGeoData():
    
    # Pre-process rawGeoData 
    if len(os.listdir(cleanGeoDataPath)) == 0:
        print('Raw Geo data not processed')
        cleanRawGeoData() 
    
    else:
        # Raw Geo data already cleaned
        print('Raw Geo data already cleaned and saved in {}'.format(cleanGeoDataPath))



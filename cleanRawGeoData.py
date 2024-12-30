import pandas as pd
import re
import os

# Clean raw geo data from Foret Ouverte
# Transform desciption of tree cover percentage from string to dict 
 
inputPath = './data/input/rawGeoData/'
outputPath = './data/input/test/'

'''
# Region Code
# Quebec Map split in region code
# Ex 21E
def getRegionCode(filename):
    code = str(filename[-7:-4])
    code = code.upper()
    return(code)
'''

def essencesCodeReformat(code):
    # change essenceCode to percentage
    result = re.findall(r'([A-Z]+)(\d+)', code)
    result = dict(result)
    # value from string to %
    for key in result:
        result[key] = int(result[key]) / 100
    return(result)

def cleanRawGeoData(outputPath = outputPath):
    print('Cleaning raw geo data')

    #Create list with all input files 
    allRegions = []
    for f in os.listdir(inputPath):
        allRegions.append(f)
   
    print('found {} regions to process'.format(len(allRegions)))

    # Go over every file 
    # Isolate region code based on name

    for index, r in enumerate(allRegions):
        print(str(index) + "/" + str(len(allRegions)))
        #Isolate region code based on naming
        #Ex: "CARTE_ECO_MAJ_21E — etage_maj_21e"
        regionCode = r[14:17]
        print('Processing {}'.format(regionCode))

        #Define file path to export essenceInfo data
        fileOutputPath = outputPath + 'CARTE_ECO_MAJ_{}.csv'.format(regionCode)
        #path to export final data
        df = pd.read_csv(inputPath + r )
        # Apply main logic converting string to dict with tree percentage
        df['essencesInfo'] = df['eta_ess_pc'].apply(essencesCodeReformat)
        df.to_csv(fileOutputPath, index=False) 
        print('writing {}'.format(fileOutputPath))

    print("Processed all raw geo data inputs")


# process essenceInfo first, input for next function
if len(os.listdir(outputPath)) == 0:
    print('Raw Geo data not processed')
    cleanRawGeoData() 
    
else:
    # Raw Geo data already cleaned
    print('Raw Geo data already cleaned and saved in {}'.format(outputPath))

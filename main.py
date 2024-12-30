import os
import pandas as pd
import re
import ast

from cleanRawGeoData import treeCoverReformat, cleanRawGeoData, rawGeoDataPath, cleanGeoDataPath


# Pre-process rawGeoData 
if len(os.listdir(cleanGeoDataPath)) == 0:
    print('Raw Geo data not processed')
    cleanRawGeoData() 
    
else:
    # Raw Geo data already cleaned
    print('Raw Geo data already cleaned and saved in {}'.format(cleanGeoDataPath))

# Create list of all exported cleanGeoData files
allRegions = []
for f in os.listdir(cleanGeoDataPath):
    allRegions.append(f)

#testing
allRegions = allRegions[0:1]
print(allRegions)

#Iterate over regions
for region in allRegions:
    dfRegion = pd.read_csv(cleanGeoDataPath + region)
    #Keep only geoc_maj, densite, cl_age, tree_cover data
    dfRegion = dfRegion.iloc[:, [1,4,-3,-1]]

    #Convert treeCover back to dict (bug read from pd.read_csv )
    dfRegion['tree_cover'] = dfRegion['tree_cover'].apply(ast.literal_eval)
    print(dfRegion.head())

    #species 
    #dfRegion['realtive_specie'] = dfRegion.apply(mycoValue function, axis = 1)

# iterate species  
# assign final value per species - fleible function for mycoValue based on species info 
# each species gets a columns
# export one final csv with only polygon an value for each  
'''
for index, f in enumerate(allFiles):
            print(f)
            print(str(index+1) + '/{}'.format(len(allFiles)+1))
            inputPath = essenceInfoPath + f

            dfData = pd.read_csv(inputPath)

            #keep only geoc_maj, age, essence info dict 
            dfData = dfData.iloc[:, [1,-1]]

            #convert string back to dict
            dfData['essencesInfo'] = dfData['essencesInfo'].apply(ast.literal_eval)
            dfData['mRz'] = dfData['essencesInfo'].apply(mycorhizalValue, associations = associations)

            dfData = dfData.iloc[:, [0,-1]]
            print(dfData)
            merged_df = pd.concat([merged_df, dfData], ignore_index=True)

'''
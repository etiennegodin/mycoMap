import os
import pandas as pd
import re
import ast

from cleanRawGeoData import processGeoData, cleanGeoDataPath
from species import populateSpeciesList

# Create a list of all species objects to analyse 
speciesList = populateSpeciesList()

#Process & clean input geo Data 
processGeoData()

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

    ### TESTING 
    dfRegion = dfRegion.head()


    #Convert treeCover back to dict (bug read from pd.read_csv )
    dfRegion['tree_cover'] = dfRegion['tree_cover'].apply(ast.literal_eval)
    
    #print(dfRegion.head())

    for index, specie in enumerate(speciesList):
        #print(index)
        dfRegion[specie.name] = dfRegion.apply(lambda row: specie.set_mycoValue(row), axis = 1)
        #dfRegion[specie.name] = 'xx'

    print(dfRegion.head())


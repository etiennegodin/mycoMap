import os
import pandas as pd
import re
import ast
import datetime

from cleanRawGeoData import processGeoData, cleanGeoDataPath
from species import populateSpeciesList
from csvTools import saveDfToCsv, mergeDfFromCsv

# Load the two CSV files into DataFrames

centroidAllPolygonsPath = 'data/input/centroidAllPolygons.csv'
outputPath = 'data/output/'
allRegionsDfOutputName = 'allRegionsDf.csv'
allRegionsMergedOutputName = 'allRegionsMerged.csv'
# Check if output_file has already been processed:

outputFileList = os.listdir(outputPath)
override = False

if allRegionsDfOutputName in outputFileList:
    path_to_file = outputPath + allRegionsDfOutputName
    
    creation_time = datetime.datetime.fromtimestamp(os.path.getctime(path_to_file))
    print('Found a allRegionsDf already processed on {}'.format(creation_time)
          )
    override = bool(input('Do you want to override {}? Y/N  '.format(path_to_file)))


if allRegionsDfOutputName not in outputFileList or override == True:

    if override == True:
        print('Overriding')
    # Create a list of all species objects to analyse 
    print('Parsing speciesList')
    speciesList = populateSpeciesList()

    #Process & clean input geo Data 
    processGeoData()

    # Create list of all exported cleanGeoData filesn
    allRegions = []

    for f in os.listdir(cleanGeoDataPath):
        allRegions.append(f)

    #testing
    allRegions = allRegions[0:1]
    print(allRegions)

    #empty dataframe for final output
    allRegions_df = pd.DataFrame()

    #Iterate over regions
    for region in allRegions:
        dfRegion = pd.read_csv(cleanGeoDataPath + region)
        #Keep only geoc_maj, densite, cl_age, tree_cover data
        dfRegion = dfRegion.iloc[:, [1,4,-3,-1]]

        ### TESTING 
        dfRegion = dfRegion.head(1000)


        #Convert treeCover back to dict (bug read from pd.read_csv )
        dfRegion['tree_cover'] = dfRegion['tree_cover'].apply(ast.literal_eval)
        
        #print(dfRegion.head())

        for specie in speciesList:
            dfRegion[specie.name] = dfRegion.apply(lambda row: specie.set_mycoValue(row), axis = 1)


        dfRegion= dfRegion.drop(dfRegion.columns[1:4], axis=1)
        allRegions_df = pd.concat([allRegions_df, dfRegion], ignore_index=True)

    saveDfToCsv(allRegions_df,outputPath + allRegionsDfOutputName)


override = False

if allRegionsMergedOutputName in outputFileList:
    path_to_file = outputPath + 'allRegionsMerged.csv'
    
    creation_time = datetime.datetime.fromtimestamp(os.path.getctime(path_to_file))
    print('Found a allRegionsDf already processed on {}'.format(creation_time)
          )
    
    override = bool(input('Do you want to override {}? Y/N  '.format(path_to_file)))

if allRegionsMergedOutputName not in outputFileList or override == True:
    merged_df = mergeDfFromCsv(centroidAllPolygonsPath,outputPath + allRegionsDfOutputName)
    saveDfToCsv(merged_df, outputPath + allRegionsMergedOutputName)
    print(merged_df)
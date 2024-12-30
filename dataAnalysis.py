import pandas as pd
import re
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
import os
import ast

#paths 
dataPath = './data/'
geoDataPath = './geoData/'
qgisExportPath = './data/qgisExport/'
essenceInfoPath = dataPath + 'essenceInfo/'
speciesPath = "./species/"
mycoMapPath = 'mycoMap - '
outputDataPath = dataPath + 'dataOutput/'
#C:\Users\manat\OneDrive\Documents\mycologie\mycoMap\species\mycoMap - cantharellusAssociations.csv
# classes

#mycorhizal species, with associated tree info as .associations
class mycorhizalSpecies:
    def __init__(self, name):
        self.name = name 
        path = speciesPath + mycoMapPath + name + 'Associations.csv'
        df = (pd.read_csv(path))
        associations = dict(zip(df['code'], df['mycoValueEssences']))
        self.associations = associations
        self.mycorhizal = True
    def __str__(self):
        return self.name

#sapotrophic species 
class sapotrophicSpecies:
    def __init__(self, name):
        self.name = name
        self.mycorhizal = False


codeEssence_path = './data/mycoMap - code_essence.csv'
classeAgePath = './data/mycoMap - classe_age.csv'


#________dictionnary pour type essence______

dfCodeEssence = pd.read_csv(codeEssence_path)
pointEssence = dict(zip(dfCodeEssence['code'], dfCodeEssence['mycoValueEssences']))

#________dictionnary pour age ______________

dfAge = pd.read_csv(classeAgePath)
valuesAge = dict(zip(dfAge['code'], dfAge['mycoValueAge']))

#functions 

def getRegionCode(filename):
    code = str(filename[-7:-4])
    code = code.upper()
    return(code)


def essenceCode(code):
    # de-concatene le code d'essence dun polygon
    #essencesInfo = []
    result = re.findall(r'([A-Z]+)(\d+)', code)
    result = dict(result)    #print(len(split_data))
    # value from string to %
    for key in result:
        result[key] = int(result[key]) / 100
    #essencesInfo.append(result)
    return(result)

def essenceInfo(qgisExportPath = qgisExportPath, test = False):

    #process and handles de-concatene function 
    print('Processing essenceInfo')
    allRegions = []
    # List all files in the directory
    for f in os.listdir(qgisExportPath):
        allRegions.append(f)

    if test == True:
        #quicker tests
        allRegions = allRegions[0:2]


    print('found {} regions to process'.format(len(allRegions)))

    for index, r in enumerate(allRegions):
        print(str(index) + "/" + str(len(allRegions)))
        regionCode = r[14:17]
        print('Processing {}'.format(regionCode))

        #file path to export essenceInfo data
        essenceInfoOutput = essenceInfoPath + 'essenceInfo{}.csv'.format(regionCode)
        #path to export final data
        df = pd.read_csv(qgisExportPath + r )
        df['essencesInfo'] = df['eta_ess_pc'].apply(essenceCode)
        df.to_csv(essenceInfoOutput, index=False) 
        print('writing {}'.format(essenceInfoOutput))

def listEssenceInfoFiles(essenceInfoPath = essenceInfoPath):
    allFiles = []
    for f in os.listdir(essenceInfoPath):
        allFiles.append(f)
    return(allFiles)

def richnessIndex(essencesInfo):

    #indice de ricnesse (nb especes)
    n = len(essencesInfo)
    return(n)

def shannonIndex(essencesInfo):
    #indice shannon 
    #creer liste proportions d'essence
    proportions_list = []
    for key in essencesInfo:
        #print(key)
        proportions_list.append(essencesInfo[key])

    #numpy array
    proportions = np.array(proportions_list)

    try:
        # Vérifiez que la somme des proportions est égale à 1 (100%)
        if not np.isclose(np.sum(proportions), 1.0):
            raise ValueError("Les proportions des espèces doivent totaliser 1")
        
        # Calculez l'indice de Shannon
        shannon_index = -np.sum(proportions * np.log(proportions))
        
    except ValueError:
        # En cas d'erreur, attribuez la valeur 0 à l'indice de Shannon
        shannon_index = 0
    
    shannon_index = -np.sum(proportions * np.log(proportions))
    return(shannon_index)

def mycoValueEssences(essencesInfo):
    #indice myco - selon arbres favorable
    indices_essences = []
    for key in essencesInfo:   
        point = pointEssence[key]
        proportion = essencesInfo[key]

        value = point * proportion
        indices_essences.append(value)
        
    mycoValueEssences = np.sum(np.array(indices_essences))
    return(mycoValueEssences)

def mycoValueAge(codeAge):
    #indice age du secteur 
    # assumer que plus vieux = plus de bois mort donc sapotrophes???
    mycoValueAge = valuesAge[codeAge]
    return(mycoValueAge)

def mycoValue(df):
    n = df['n']
    H = df['H']
    mVE = df['mVE']
    mVA = df['mVA']


    nStrength = 2
    HStrength = 2
    mVEStrength = 3
    mVAStrength = 1

    #ponderation egale 
    mV = (n * nStrength) * ( H * HStrength) * ( mVE * mVEStrength) * (mVA * mVAStrength) 
    mV = mV / 100
    #mV = mV / (nStrength + HStrength + mVEStrength + mVAStrength)
    return(mV)

def mycorhizalValue(essencesInfo, associations):
    #indice myco - selon arbres favorable
    valuesList = []
    for essence in essencesInfo:   
        value = associations[essence]
        pourcentage = essencesInfo[essence]
        #value = value * pourcentage
        valuesList.append(value)
    
    mycorhizalValue = np.sum(np.array(valuesList))
    #mycorhizalValue = np.sum(np.array(valuesList)) / len(essencesInfo)
    return(mycorhizalValue)
    



x = 0
# process essenceInfo first, input for next function
if len(os.listdir(essenceInfoPath)) == len(os.listdir(qgisExportPath)): 
    print('Files already processed in essenceInfo')
    #x = int(input('Do you want to overwrite? 0/1? '))
    if x == 1:
        essenceInfo()
else:
    print('EssenceInfo not processed')
    essenceInfo()


#create species to look analyse for 
species = []

cantharellus = mycorhizalSpecies('cantharellus')
print(cantharellus.mycorhizal)
species.append(cantharellus)


genericSapotrophic = sapotrophicSpecies('genericSapotrophic')
#species.append(genericSapotrophic)
print(species)

#mycorhizal 
# looking onyl at specific species no need for n & H & age


for s in species:

    outputSpeciesData = outputDataPath + s.name + '/' 
    merged_df = pd.DataFrame()

    #list all region infos files to loop over
    allFiles = listEssenceInfoFiles()

    #allFiles = allFiles[0:1]

    if not os.path.exists(outputSpeciesData):
        os.mkdir(outputSpeciesData)

    #key species but also n & H for concentration of said species (reverse richness )
    if s.mycorhizal == True:

        associations = s.associations
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





    # sapotrophic 
    # higher n, H & age means more variety of tree, diversity and possible dead wood 
    if s.mycorhizal == False:
        for index, f in enumerate(allFiles):
            print(f)
            print(str(index+1) + '/{}'.format(len(allFiles)+1))
            inputPath = essenceInfoPath + f

            #code = getRegionCode(f)
            #print(code)
            #dynamic output ath with region code 
            #outputFilePath = outputSpeciesData + code + 'data.csv'

            dfData = pd.read_csv(inputPath)

            #keep only geoc_maj, age, essence info dict 
            dfData = dfData.iloc[:, [1,-3,-1]]

            #convert string back to dict
            dfData['essencesInfo'] = dfData['essencesInfo'].apply(ast.literal_eval)

            dfData['n'] = dfData['essencesInfo'].apply(richnessIndex)
            dfData['H'] = dfData['essencesInfo'].apply(shannonIndex)
            dfData['mVA'] = dfData['cl_age_et'].apply(mycoValueAge)

            dfData = dfData.iloc[:, [0,-3,-2,-1]]

            print(dfData)
            merged_df = pd.concat([merged_df, dfData], ignore_index=True)

    # Write merged DataFrame to the CSV file

    outputAllData = outputSpeciesData + '{}_data.csv'.format(s.name)
    merged_df.to_csv(outputAllData, index=False) 
    print('output')










#dataOutputPath = dataPath + 'dataOutput/' + 'data{}.csv'.format(regionCode)


'''
if os.path.exists(essenceInfoPath):
    print('essenceInfo already de-concatenated for {}'.format(regionCode))
    #test if data file is already made 
    if not os.path.exists(dataOutputPath): 
            print("{} doesn't exists, processing essenceInfo".format(dataOutputPath))
            print("loading {} as dfData".format(essenceInfoPath))
            
        
            #data analysis
            
            dfData['mVE'] = dfData['essencesInfo'].apply(mycoValueEssences)
            dfData['mycoValue'] = dfData.apply(mycoValue, axis =1)
        
            dfOutput = dfData.iloc[:, [0, 1, -5, -4, -3, -2, -1]]
            

    if os.path.exists(dataOutputPath): 
        print('final data output already exists for {}'.format(regionCode))

'''
import pandas as pd
from numpy import NaN 

from mycoValueAnalysis import mycoValueAnalysis

speciesListFile = 'data/input/mycoMap - speciesList.csv'
treeAssociationsPath = 'data/input/treeAssociations/'

class Specie:
    def __init__(self, name, ecology, treeAssociations):
        self.name = name 
        self.ecology = ecology
        self.treeAssociations = treeAssociations


    def set_mycoValue(self, row):
        print('----------------------------------')
        mycoFactors = list(row.values)
        mycoFactors = mycoFactors[1:4]
        #print(mycoFactors)
        self.mycoValue = mycoValueAnalysis(*mycoFactors, ecology = self.ecology)

        return self.mycoValue
        
    def __str__(self):
        return self.name


def populateSpeciesList():

    speciesList = []
    df = pd.read_csv(speciesListFile) 
      
    for index, row in df.iterrows():
        name = (row['name'])
        ecology = (row['ecology'])
        #Pre-set treeAssociation to None 
        #Kept as None if not mycorhizal or can't find file 
        treeAssociations = None

        #if Mycorrhizal look for tree associations file to inform 
        if ecology == 'mycorrhizal':
            try:
                treeAssociations = pd.read_csv(treeAssociationsPath + name + '.csv') 
                #Drop first collumns (doubled from csv)    
                treeAssociations = treeAssociations.drop(treeAssociations.columns[0], axis=1)
            except:
                print("Can't find treeAssociation file for {}".format(name))
                treeAssociations = NaN
                


        # specie instantiation
        specie = Specie(name,ecology,treeAssociations)
        speciesList.append(specie)

    
    return speciesList



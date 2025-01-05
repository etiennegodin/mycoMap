import pandas as pd
from numpy import NaN 

from mycoValueAnalysis import mycoValueAnalysis

speciesListFile = 'data/input/mycoMap - speciesList.csv'
treeAssociationsPath = 'data/input/treeAssociations/'

class Specie:
    def __init__(self, name, ecology, treeAssociations):

        x = name.replace(" ", "_")
        print(name)
        print(x)
        self.name = name 
        self.ecology = ecology
        self.treeAssociations = treeAssociations


    def set_mycoValue(self, row):
        mycoFactors = list(row.values)
        mycoFactors = mycoFactors[1:4]
        self.mycoValue = mycoValueAnalysis(self.name, *mycoFactors, ecology = self.ecology, treeAssociations = self.treeAssociations)

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
                treeAssociations = pd.Series(treeAssociations.mycoValueEssences.values,index=treeAssociations.code).to_dict()
            except:
                print("Can't find treeAssociation file for {}".format(name))
                treeAssociations = NaN

        # specie instantiation
        specie = Specie(name,ecology,treeAssociations)
        speciesList.append(specie)

    return speciesList
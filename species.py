import pandas as pd

speciesListFile = 'data/input/mycoMap - speciesList.csv'
treeAssociationsPath = 'data/input/treeAssociations/'

class Specie:
    def __init__(self, *args):
        self.name = name 
        self.ecology = ecology
        self.treeAssociations = treeAssociations


    def mycoValue():

    def __str__(self):
        return self.name


speciesList = []

#dfData['essencesInfo'] = dfData['essencesInfo'].apply(ast.literal_eval)
df = pd.read_csv(speciesListFile)            


for index, row in df.iterrows():
    name = (row['name'])
    ecology = (row['ecology'])

    #if Mycorrhizal look for tree associations file to inform 
    if ecology == 'mycorrhizal':
        try:
            treeAssociations = pd.read_csv(treeAssociationsPath + name + '.csv') 
        except:
            print("Can't find treeAssociation file for {}".format(name))

        #Drop first collumns (doubled from csv)    
        treeAssociations = treeAssociations.drop(treeAssociations.columns[0], axis=1)
        
    specie = Specie(name,ecology,treeAssociations)
    speciesList.append(specie)
    

for specie in speciesList:
    print(specie.name)


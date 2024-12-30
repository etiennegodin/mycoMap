import numpy as np
import pandas as pd 

#n = richnessIndex 
# H = shannonIndex

#Read mycoValueAge.csv' and create dict where code is key and values is mycoValueAge
dfAgeCode = pd.read_csv('data/input/mycoValueAge.csv')
mycoAgeValueDict = pd.Series(dfAgeCode.mycoValueAge.values,index=dfAgeCode.code).to_dict()

def richnessIndex(tree_cover):
    #nb on individual species 
    n = len(tree_cover.keys())
    return(n)

def shannonIndex(tree_cover):
    #indice shannon 

    #creer liste proportions d'essence
    #Ex: [0.3, 0.2, 0.2, 0.2, 0.1]
    proportions_list = []

    for key in tree_cover:
        proportions_list.append(tree_cover[key])

    # Reformat proprtions list in np.array         
    proportions = np.array(proportions_list)

    try:
        # Vérifiez que la somme des proportions est égale à 1 (100%)
        if not np.isclose(np.sum(proportions), 1.0):
            raise ValueError("Can't calculate shannonIndex, total of tree species proprotions do not equal 100%")
        
        # Calculate shannon index
        # https://en.wikipedia.org/wiki/Diversity_index
        shannon_index = -np.sum(proportions * np.log(proportions))
        
    except ValueError:
        # In case of error, assign value of 0 
        shannon_index = 0
    
    shannon_index = round(shannon_index,5)
    
    return(shannon_index)

def mycoValueAge(cl_age_et):
    #indice age du secteur 
    # assumer que plus vieux = plus de bois mort donc sapotrophes???

    mycoValueAge =  mycoAgeValueDict[cl_age_et]
    return(mycoValueAge)

def mycoValueMicorrhizal(treeAssociations,*mycoFactors):
    tree_cover = mycoFactors[-1]
    print(tree_cover)
    
    combined_values = []
    for tree, percentage in tree_cover.items():
        print(tree, percentage)
        print(treeAssociations[tree])
        value = percentage * treeAssociations[tree]
        combined_values.append(value)
        
    #indice myco - selon arbres favorable
    
    mycoValueMicorrhizal = np.sum(np.array(combined_values))
    #mycoValueMicorrhizal = np.sum(np.array(combined_values)) / len(tree_cover.keys())
    return(mycoValueMicorrhizal)
    
def mycoValueSapotrophic(*mycoFactors):
    # sapotrophic 
    tree_cover = mycoFactors[-1]
    cl_age_et = mycoFactors[-2]

    n = richnessIndex(tree_cover)
    H = shannonIndex(tree_cover)
    age = mycoValueAge(cl_age_et)

    # higher n, H & age means more variety of tree, diversity and possible dead wood
    #better method to weight each element
    mycoValue = n * H * age

    return mycoValue

#densite, cl_age_et, tree_cover
def mycoValueAnalysis(name, *mycoFactors, ecology, treeAssociations):
    mycoValue = 0
    if ecology == 'mycorrhizal':
        mycoValue = mycoValueMicorrhizal(treeAssociations,*mycoFactors, )
    #treeCove
    elif ecology == 'sapotrophic':
        mycoValue = mycoValueSapotrophic(*mycoFactors)
    
    elif ecology == 'parasitic':
        mycoValue = 3
    #age 
    return mycoValue


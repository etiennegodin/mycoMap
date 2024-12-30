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

def mycoValueEssences(tree_cover):
    #indice myco - selon arbres favorable
    indices_essences = []
    for key in essencesInfo:   
        point = pointEssence[key]
        proportion = essencesInfo[key]

        value = point * proportion
        indices_essences.append(value)
        
    mycoValueEssences = np.sum(np.array(indices_essences))
    return(mycoValueEssences)

def mycoValueAge(cl_age_et):
    #indice age du secteur 
    # assumer que plus vieux = plus de bois mort donc sapotrophes???

    mycoValueAge =  mycoAgeValueDict[cl_age_et]
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
def mycoValueAnalysis(*mycoFactors, ecology):
    mycoValue = 0
    if ecology == 'mycorrhizal':
        print('-------------------------')
        mycoValue = 1
    #treeCove
    elif ecology == 'sapotrophic':
        mycoValue = mycoValueSapotrophic(*mycoFactors)
        #mycoValue = 2
        
    elif ecology == 'parasitic':
        mycoValue = 3
    #age 
    return mycoValue


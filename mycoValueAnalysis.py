

#n = richnessIndex 
# H = shannonIndex

def richnessIndex(tree_cover):

    #nb on individual species 
    n = len(essencesInfo)
    return(n)

def shannonIndex(tree_cover):
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

def mycoValueAge(cl_age):
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
    

def mycoValueSapotrophic(*args):
    # sapotrophic 
    # higher n, H & age means more variety of tree, diversity and possible dead wood

def mycoValueAnalysis(densite, cl_age_et, tree_cover, ecology):



    print(densite,cl_age_et,tree_cover, ecology)


    #treeCover
    #age 
    pass


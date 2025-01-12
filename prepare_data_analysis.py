import numpy as np 
import pandas as pd

import matplotlib.pyplot as plt
import tools


# Temp 


file = 'data/gbifQueries/Cantharellus_enelensis/Cantharellus_enelensis_geodata.csv'

df = pd.read_csv(file)

df = tools.convert_tree_cover_data_type(df)




def richnessIndex(tree_cover):


    print(tree_cover)
    #indice de ricnesse (nb especes)
    n = len(tree_cover)
    return(n)

def shannonIndex(tree_cover):
    #indice shannon 
    #creer liste proportions d'essence
    proportions_list = []
    for key in tree_cover:
        #print(key)
        proportions_list.append(tree_cover[key])

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

    # Entropy 
    # SUm of surprise for each of elements
    return(shannon_index)


def interpret_tree_cover(df):
    df['richness_index'] = df['tree_cover'].apply(richnessIndex) 
    df['shannon_index'] = df['tree_cover'].apply(shannonIndex)

    return df 

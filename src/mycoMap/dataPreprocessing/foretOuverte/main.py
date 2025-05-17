# prep foretOuverte data in single region.shp
import geopandas as gpd
import pandas as pd 
import numpy as np
import re

from mycoMap import mergeForetOuverteData
from mycoMap import utils 

# Paths
input_gpkg_path = 'data/raw/geodata/foretOuverte/PEE_MAJ_PROV/gpkg' 
output_path = 'data/interim/geodata/vector/CARTE_ECO/'

# Global vars 
ordinal_columns = ['ty_couv_et','cl_dens','cl_haut','cl_age_et','etagement','cl_pent','hauteur']
categorical_columns = ['dep_sur','cl_drai', 'eta_ess_pc']
gdf_columns = ['geoc_maj', 'geometry']
all_columns = ordinal_columns + categorical_columns + gdf_columns

encoding_dictionnary = {
                        'cl_age_et': 
                        {
                            '10' : 10,
                            '30' : 30,
                            '50' : 50,
                            '70' : 70,
                            '90' : 90,
                            '110' : 110,
                            '120' : 120,
                            '130' : 130,
                            'VIN' : 40, # 30 a 50
                            'JIN' : 95 # 70 a 120
                        },
}

def dep_sur_map(value):
    """
    remap sub-categories of depot surface values to main categories of soil
    """
    value = str(value)
    if value.startswith('1'):
        return 'Depot Glaciaire'
    elif value.startswith('2'):
        return 'Depot fluvio-glaciaire'
    elif value.startswith('3'):
        return 'Depot fluviatile'
    elif value.startswith('4'):
        return 'Depot lacustre'
    elif value.startswith('5'):
        return 'Depot marin'
    elif value.startswith('6'):
        return 'Depot litoral marin'
    elif value.startswith('7'):
        return 'Depot organique'
    elif value.startswith('8'):
        return 'Depot de pente'
    elif value.startswith('9'):
        return 'Depot eolien'
    elif value.startswith('R'):
        return 'Rocheux'
    else:
        return 'Autre depot'

def encode_vector_fields(gdf, encoding_dict = None):

    for series_name, series in gdf.items():
        try:
            gdf[series_name] = gdf[series_name].map(encoding_dict[series_name])
            print(f'Encoded {series_name}')
        except Exception as e:
            print(e)

    return gdf

def encode_dep_sur(gdf):
    #remap sub-categories of depot surface values to main categories of soil
    gdf['dep_sur'] = gdf['dep_sur'].apply(dep_sur_map)
    print("Encoded 'dep_sur;")
    return gdf

def encode_tree_cover(gdf):
    gdf['tree_cover'] = gdf['eta_ess_pc'].apply(decode_eta_ess_pc)
    print("Encoded 'dep_sur;")
    return gdf

def decode_eta_ess_pc(code):

    # change tree cover infor from string to dict of percentage
    result = re.findall(r'([A-Z]+)(\d+)', code)

    result = dict(result)
    # value from string to %
    for key in result:
        result[key] = int(result[key]) / 100
    return(result)

# Derive new data from existing columns
def richnessIndex(tree_cover):
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

def processs_forest_ecology_indexes(gdf):
    # Convert tree cover string to dictS
    #utils.convert_string_to_numeral(gdf, collumn='tree_cover')

    gdf['tree_diversity_index'] = gdf['tree_cover'].apply(richnessIndex) 
    gdf['tree_shannon_index'] = gdf['tree_cover'].apply(shannonIndex)

    return gdf

def main(region):    

        gdf, perimeter_gdf = mergeForetOuverteData.merge_region_gpkg(region)

        #keep only relevant columns
        gdf = gdf[all_columns]

        #encode field to aggregate 
        gdf = encode_vector_fields(gdf, encoding_dictionnary)
        gdf = encode_dep_sur(gdf)
        gdf = encode_tree_cover(gdf)
        gdf = processs_forest_ecology_indexes(gdf)

        gdf.to_file(output_path + f'CARTE_ECO_{region}.shp')

if __name__ == '__main__':
    regions_list = utils.get_regionCodeList()
    for region in regions_list:
        main(region)

                                        

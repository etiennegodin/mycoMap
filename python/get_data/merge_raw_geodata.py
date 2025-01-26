import os
import pandas as pd 
import utilities

# Merge two datasets in one 

# Merge region based geodata from 2 different datasets
# CARTE ECO_MAJ + 


env_factors_path = 'data/raw/region_env_factors/CARTE_ECO_MAJ_'
region_data_path = 'data/raw/regions_data'

regions_list = os.listdir('data/raw/regions_data')

output_path = 'data/input/geodata/forest_composition'
regions_data_cols = ['geoc_maj', #id
                'cl_pent', # classe de pente
                'dep_sur',# depot surface
                 'cl_age', # classe d'age 
                'cl_drai', # classe drainage
                'cl_haut', # classe hauteur
                 'type_couv', #ype couvert
                'origine', # Perturbation d'origine
                'an_origine', # annee pertrubation
                'perturb', # Perturbation partielle
                'an_perturb', # Année de la perturbation partielle
                'X',
                'Y']

env_factors_cols = ['geoc_maj',
                     'ty_couv_et',
                     'densite',
                     'cl_age_et',
                     'tree_cover',
                     'hauteur',
                     ]

for region in regions_list:

    regions_data_df = pd.read_csv(f'{region_data_path}/{region}/{region}.csv', usecols= regions_data_cols)

    env_factors_df = pd.read_csv(f'{env_factors_path}{region}.csv', usecols= env_factors_cols)

    merged_df = pd.merge(regions_data_df, env_factors_df, on='geoc_maj')

    utilities.saveDfToCsv(merged_df, f'{output_path}/{region}.csv')

    print(merged_df.head())
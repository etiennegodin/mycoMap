from occurences import searchOccurences
from specie import create_specie

import pandas as pd

pd.set_option('display.max_colwidth', 1000)

specie_name = 'Cantharellus enelensis'
specie = create_specie(specie_name, rank = 'Species')
print(specie.name)


'''
user_input_download = None
user_input_download = str.upper(input("Do you want to download data Y/N? "))

if user_input_download == 'Y':
    download = True
elif user_input_download == 'N':
    download = False
else:
    download = False
'''
    
occ_df = searchOccurences(specie, download = True)
#print(occ_df.head(50))


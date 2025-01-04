from occurences import searchOccurences
from specie import create_specie

import pandas as pd

pd.set_option('display.max_colwidth', 1000)

specie_name = 'Cantharellus'
specie = create_specie(specie_name, rank = 'Genus')
print(specie.name)



occ_df = searchOccurences(specie, limit = 5, download = True)
#print(occ_df.head(50))

from occurences import searchOccurences
from specie import create_specie

import pandas as pd

pd.set_option('display.max_colwidth', 1000)

specie_name = 'Cantharellus'
specie = create_specie(specie_name, rank = 'Genus')
print(specie.__dict__)



occ_df = searchOccurences(specie, limit = 300)
print(occ_df.head(50))

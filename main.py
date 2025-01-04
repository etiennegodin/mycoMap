from occurences import searchOccurences, get_download_zip, processOccurenceDownload
from specie import create_specie

import pandas as pd
import os

#Readable inaturalist links
pd.set_option('display.max_colwidth', 1000)

occurences_file = None

specie_name = 'Cantharellus enelensis'
specie = create_specie(specie_name, rank = 'Species')

# Check if occurence download has already been made
if 'download_key.txt' not in os.listdir('data/gbifQueries/{}'.format(specie.name)):
    occ_df = searchOccurences(specie, download = True)

else:
    print('Occurence request already made for {}.'.format(specie.name))
    print('Trying to download request to disk using provided key')
    print('')
    #Download request data to disk
    occurences_file = get_download_zip(specie)
    #print(occ_df.head(50))
    print(occurences_file)

if occurences_file != None:
    processOccurenceDownload(occurences_file)




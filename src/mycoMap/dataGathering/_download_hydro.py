import pandas as pd
import requests    
from zipfile import ZipFile
import os

output_folder = 'data/geodata/raw/hydro/'

urls = pd.read_csv('data/geodata/raw/hydro/Index_GRHQ.csv')


def unzip__file(zipfile, output_path):

    with ZipFile(zipfile, 'r') as zObject: 
        # Extracting all the members of the zip  
        # into a specific location. 
        zObject.extractall( 
            path = output_path)

filtered_urls = {}

for row in urls.iterrows():
    bloc = row[1]['Bloc']
    url = row[1]['FGDB']
    filtered_urls[bloc] = url



for idx, (key, url) in enumerate(filtered_urls.items()):
    zipfile = f'{key}.zip'
    output_path = f'{output_folder}/{key}.tif'

    if not os.path.exists(f'{output_folder}/zip/{zipfile}'):
        print(idx+1 ,'/', len(filtered_urls))
        print(key)
        print(url)
        r = requests.get(url, allow_redirects=True)
        open(f'{output_folder}/zip/{zipfile}', 'wb').write(r.content)
        print(f'{zipfile} downloaded')
    else:
        with ZipFile(f'{output_folder}/zip/{zipfile}', 'r') as zObject: 
        # Extracting all the members of the zip  
        # into a specific location. 
            zObject.extractall( 
                path = output_path)



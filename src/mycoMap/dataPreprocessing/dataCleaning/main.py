import pandas as pd 
import os 

from mycoMap.dataPreprocessing.dataCleaning import mergeForetOuverteData

# Global vars 
ordinal_columns = ['ty_couv_et','cl_dens','cl_haut','cl_age_et','etagement','cl_pent','hauteur']
categorical_columns = ['dep_sur','cl_drai', 'eta_ess_pc']
gdf_columns = ['geoc_maj', 'geometry']
all_columns = ordinal_columns + categorical_columns + gdf_columns

def cleanForetOuverteData(regions_list, overwrite = False, verbose = False):
    """
    Input : Takes in a list of region subsets, reads and cleans them
    
    Output: Dict of {region : gdf}
    """
    print(f'#{__name__}.cleanForetOuverteData')
    cleaned_foretOuvert_gdfs = {}
    perimeter_gdfs = {}
    for i, region in enumerate(regions_list):

        gdf, perimeter_gdf = mergeForetOuverteData.importForetOuvertLayers(region, overwrite = overwrite, verbose = verbose )
        print(f'Cleaning {region} ({i+1}/{len(regions_list)})')
        #keep only relevant columns
        gdf = gdf[all_columns]
        cleaned_foretOuvert_gdfs[region] = gdf
        perimeter_gdfs[region] = perimeter_gdf

    print(cleaned_foretOuvert_gdfs == None)
    print(perimeter_gdfs == None)
    if not cleaned_foretOuvert_gdfs == None and not perimeter_gdfs  == None:
        return (cleaned_foretOuvert_gdfs, perimeter_gdfs)

def cleanOccurencesData(csv_occurences_path,cleaned_occurences_path, overwrite = False ):
    """
    Input : Takes in a csv path of occurences, reads and cleans it
    Output: Dict {path : Dataframe of cleaned occurences}
    """

    print(f'#{__name__}.cleanOccurencesData')

    def process():
        # read csv
        df = pd.read_csv(csv_occurences_path)

        # keep only canada & quebec
        df = df[df.countryCode == 'CA']
        df = df[df.stateProvince == 'Québec']

        # remove occurences with same latLong values (preserved specimens from older sources)
        df = df.drop_duplicates(subset=['decimalLatitude'], keep = 'last')
        df = df.drop_duplicates(subset=['decimalLongitude'],keep = 'last')

        # remove before 2000
        df = df[df.year >= 2000]

        df.to_csv(cleaned_occurences_path, index = False)
        print('Writting cleaned occurences to:')
        print(cleaned_occurences_path)

        output = {cleaned_occurences_path :df}
        return output
    
    def read():
        df = pd.read_csv(csv_occurences_path)
        output = {cleaned_occurences_path : df}
        return output

    if os.path.isfile(cleaned_occurences_path):
        print(f'Cleaned occurences already on file')
        if overwrite:
            print('Overwritting')
            output = process()
        else:
            # Written, not overriding, just reading it back to create dict and df 
            output = read()
    else:
        output = process
    
    return output

if __name__ == '__main__':
    print('Running dataCleaning module only')

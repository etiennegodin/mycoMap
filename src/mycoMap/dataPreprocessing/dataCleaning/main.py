import pandas as pd 
import os 

from mycoMap.dataPreprocessing.dataCleaning import mergeForetOuverteData

# Global vars 
ordinal_columns = ['ty_couv_et','cl_dens','cl_haut','cl_age_et','etagement','cl_pent','hauteur']
categorical_columns = ['dep_sur','cl_drai', 'eta_ess_pc']
gdf_columns = ['geoc_maj', 'geometry']
all_columns = ordinal_columns + categorical_columns + gdf_columns



def cleanForetOuverteData(region, overwrite = False, verbose = False):
    """
    Input : Takes in a region subsets, reads and cleans it
    
    Output: Cleaned gdf, region perimeter gdf
    """
    print(f'#{__name__}.cleanForetOuverteData')

    gdf, perimeter_gdf = mergeForetOuverteData.importForetOuvertLayers(region, overwrite = overwrite, verbose = verbose )
    #keep only relevant columns
    gdf = gdf[all_columns]

    return (gdf, perimeter_gdf)

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
    from mycoMap import utils 
    regions_list = utils.get_regionCodeList(range = (-2,17), verbose= True)
    cleaned_foretOuvert_gdfs, perimeter_gdfs = cleanForetOuverteData(regions_list)

    print(cleaned_foretOuvert_gdfs)
    print(perimeter_gdfs)


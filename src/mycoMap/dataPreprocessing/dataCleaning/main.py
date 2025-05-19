import pandas as pd 

from mycoMap.dataPreprocessing.dataIntegration import mergeForetOuverteData

# Global vars 
ordinal_columns = ['ty_couv_et','cl_dens','cl_haut','cl_age_et','etagement','cl_pent','hauteur']
categorical_columns = ['dep_sur','cl_drai', 'eta_ess_pc']
gdf_columns = ['geoc_maj', 'geometry']
all_columns = ordinal_columns + categorical_columns + gdf_columns

def cleanForetOuverteData(regions_list, verbose = False):

    print('Running')
    print(f'#{__name__}.cleanForetOuverteData')
    cleaned_foretOuvert_gdfs = []
    for i, region in enumerate(regions_list):
        print(f'Cleaning {region} ({i+1}/{len(regions_list)})')
        gdf, perimeter_gdf = mergeForetOuverteData.merge_region_gpkg(region, verbose = verbose )
            #keep only relevant columns
        gdf = gdf[all_columns]
        cleaned_foretOuvert_gdfs.append(gdf)
    
    return cleaned_foretOuvert_gdfs

def cleanOccurencesData(csv_occurences_path, write = False):
    print('#Running')
    print(f'#{__name__}.cleanOccurencesData')
    # read csv s
    df = pd.read_csv(csv_occurences_path)

    # keep only canada & quebec
    df = df[df.countryCode == 'CA']
    df = df[df.stateProvince == 'Québec']

    # remove occurences with same latLong values (preserved specimens from older sources)
    df = df.drop_duplicates(subset=['decimalLatitude'], keep = 'last')
    df = df.drop_duplicates(subset=['decimalLongitude'],keep = 'last')

    # remove before 2000
    cleaned_occ_df = df[df.year >= 2000]

    print('Cleaned occurence data')

    if write:
        output_path = 'data/interim/occurences/filteredOcurrences.csv'
        cleaned_occ_df.to_csv(output_path, index = False)
        print('Writting cleaned occurences to:')
        print(output_path)

    return cleaned_occ_df

if __name__ == '__main__':
    print('Running dataCleaning module only')

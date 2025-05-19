import geopandas as gpd
import pandas as pd
import os

from mycoMap import utils 

def main(cleaned_occurences_path, grid_path, sjoin_occurence_path, overwrite = False):
    print('Running')
    print(f'#{__name__}.main')
    
    def process():
        # load grid 
        grid = gpd.read_file(grid_path)

        #load occurences
        df = pd.read_csv(cleaned_occurences_path)
        print(df.shape)
        gdf = utils.df_to_gdf(df, xy = ['decimalLongitude','decimalLatitude'])
        print(gdf.shape)
        #spatial join
        joined_gdf = gpd.sjoin(gdf, grid, how ='inner', predicate= 'intersects')
        joined_gdf = joined_gdf.drop(['index_right'], axis = 1)
        print(joined_gdf.shape)

        df = utils.gdf_to_df(joined_gdf)
        df.to_csv(sjoin_occurence_path, index  = False)
        return df 

    def read():
        df = pd.read_csv(sjoin_occurence_path)
        return df 
    
    if os.path.isfile(sjoin_occurence_path):
        if overwrite:
            print('Occurences already spatialy joined, ### overwritting ###')
            df = process()
        else:
            print('Occurences already spatialy joined, reading')
            df = read()
    else:
        print('Occurences not spatialy joined, processing')
        df = process()

    return df 
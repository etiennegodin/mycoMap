import os
import geopandas as gpd
import pandas as pd
import itertools
import numpy as np
import gc

from mycoMap import utils
from mycoMap import geoUtils

cell_agg_dict = { 'ty_couv_et': lambda x : x.mode()[0] if not x.mode().empty else np.nan,
                        'cl_dens' : lambda x : x.mode()[0] if not x.mode().empty else np.nan,
                        'cl_haut' : lambda x : x.mode()[0] if not x.mode().empty else np.nan,
                        'cl_age_et' : 'mean',
                        'etagement' : lambda x : x.mode()[0] if not x.mode().empty else np.nan,
                        'cl_pent' : lambda x : x.mode()[0] if not x.mode().empty else np.nan,
                        'hauteur' : 'mean',
                        'dep_sur' : lambda x : x.mode()[0] if not x.mode().empty else np.nan,
                        'cl_drai' : lambda x : x.mode()[0] if not x.mode().empty else np.nan,
                        'tree_cover' : lambda dicts : len(set(itertools.chain.from_iterable(d.keys() for d in dicts))),
                        'tree_shannon_index' : 'mean'
}

def aggregateForetOuverteData(encoded_foretOuvert_gdf: gpd.GeoDataFrame, 
                            perimeter_gdf: gpd.GeoDataFrame,
                            grid: gpd.GeoDataFrame,
                            region : str,
                            subset_output_path : str,
                            write = True, verbose = False):
    print(f'#{__name__}.aggregateForetOuverte')
    print(f'Aggregating data for {region}')

    #Convert all to WSG84
    grid = grid.to_crs(4326)
    foretOuverte_gdf = encoded_foretOuvert_gdf.to_crs(4326)
    perimeter_gdf = perimeter_gdf.to_crs(4326)

    #Check if main gdf loaded correctly 
    print(foretOuverte_gdf.head())

    # Clip full grid by perimeter 
    clipped_grid = geoUtils.clip_grid_per_region(perimeter_gdf,grid, debug= True, keep_cols= ['FID', 'geometry', 'block_id'])

    # Foret ouvert gdf spatial join with clipped grid 
    # Assign each vector shape of foret ouverte a value of grid id 
    joined_gdf = gpd.sjoin(foretOuverte_gdf, clipped_grid, how ='inner', predicate= 'intersects')
    joined_gdf = joined_gdf.drop(['index_right'], axis = 1)
    
    #Aggregate field values grouped by cell id based on dict 
    try:
        aggregated_gdf = joined_gdf.groupby('FID').agg(cell_agg_dict).reset_index()
        #Performed tree richness based on tree cover column, rename 
        aggregated_gdf = aggregated_gdf.rename(columns= {'tree_cover' : 'tree_diver' })
    except Exception as e:
        print(e)

    result_gdf = clipped_grid.merge(aggregated_gdf, on = 'FID',how = 'left')
    if write:
        output_file = subset_output_path + f'{region}_grid.shp'
    try: 
        result_gdf.to_file(output_file, driver='ESRI Shapefile')
        print(f'Saved {output_file}')
    except Exception as e:
        print("Failed to export shp")
        print(e)

            #export as csv
    output_csv = subset_output_path + f'csv/{region}_grid.csv'
    df = utils.gdf_to_df(result_gdf)
    try:
        df.to_csv(output_csv, index = False)
    except Exception as e:
        print("Failed to export csv")
        print(e)

    #Delete after saved 
    del result_gdf
    del df
    gc.collect()

        
def process_fungi_ecology_index(sjoin_occurences_df: pd.DataFrame,
                                grid : gpd.GeoDataFrame):
    print(f'#{__name__}.process_fungi_ecology_index')

    df = sjoin_occurences_df
    joined_gdf = utils.df_to_gdf(df, xy = ['decimalLongitude','decimalLatitude'])

    #aggregate field values grouped by cell id 
    try:
        richness_gdf = joined_gdf.groupby('FID')['species'].nunique().reset_index(name='fungi_richness')
        shannon_gdf = joined_gdf.groupby('FID')['species'].agg(utils.shannonIndex).reset_index(name='fungi_shannon')
    except Exception as e:
            print(e)

    result_gdf = grid.merge(richness_gdf, on = 'FID',how = 'left')
    fungi_ecology_gdf = result_gdf.merge(shannon_gdf, on = 'FID',how = 'left')
    fungi_ecology_gdf = fungi_ecology_gdf.drop(['geometry', 'block_id'], axis = 1)
    fungi_ecology_gdf = fungi_ecology_gdf.fillna(0)
    return fungi_ecology_gdf

def mergeAllDataset(grid: gpd.GeoDataFrame, gdfs :list, output_path: str = None, write =True):
    print(f'#{__name__}.mergeAllDataset')

    shp_output_path = output_path + 'allIntegratedData.shp'
    csv_output_path = output_path + 'allIntegratedData.csv'

    final_gdf = grid

    for i, gdf in enumerate(gdfs):
        # Removing geometry columns in data to merge 
        if 'geometry' in gdf.columns:
            try:
                gdf.drop(['geometry'], axis = 1, inplace = True)
            except Exception as e:
                print('Failed to remove geometry column')

        # Removing block id from clusterng in columns in data to merge 
        if 'block_id' in gdf.columns:
            try:
                gdf.drop(['block_id'], axis = 1, inplace = True)
            except Exception as e:
                print('Failed to remove block_id column')

        # Merge data in final gdf 
        try:
            final_gdf = final_gdf.merge(gdf, on = 'FID',how = 'left')
        except Exception as e:
            print('Failed to merge data')
            print(e)

    print(final_gdf.shape)
    print('#'*100)


    # Removing all grid cells without value
    # (Mainly explained from grid covering whole area and foretOuverte data only in forested areas and in Qc boundaries )
    # 'cl_dens' used as 
    final_gdf = final_gdf.dropna(subset=['cl_dens'])
    print(final_gdf.shape)

    if write and output_path:
        final_gdf.to_file(shp_output_path, driver='ESRI Shapefile')
        final_gdf.to_csv(csv_output_path)
    
    return final_gdf


def combineAllSubsets(dir_path : str):
    print(f'#{__name__}.combineAllSubsets')

    subsets_list = os.listdir(dir_path)
    df = pd.DataFrame()

    for i, subset in enumerate(subsets_list):
        print(f'Combining {subset} ({i+1}/{len(subsets_list)})')
        df_temp = pd.read_csv(dir_path + subset)
        df = pd.concat([df,df_temp])
    
    print('#Combined all subsets#')

    return df
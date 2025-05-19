import geopandas as gpd
from mycoMap import utils
from mycoMap import geoUtils
import itertools
import numpy as np

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

def aggregateForetOuverteData(merged_subsets, grid, subset_output_path, write = True, verbose = False):

    print(f'#{__name__}.aggregateForetOuverte')

    #Convert grid to WSG84
    grid = grid.to_crs(4326)

    for region, gdfs in merged_subsets.items():

        foretOuverte_gdf = gdfs[0]
        perimeter_gdf = gdfs[1]

        foretOuverte_gdf = foretOuverte_gdf.to_crs(4326)
        print(foretOuverte_gdf.head())
        perimeter_gdf = perimeter_gdf.to_crs(4326)
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


def process_fungi_ecology_index(sjoin_occurences_df, grid):
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


def mergeSubsets(*args):
    """
    Create list of merged dicts for aggregation
    """

    print(f'#{__name__}.mergeSubsets')

    merged = {}
    for d in args:
        for key, value in d.items():
            merged.setdefault(key, []).append(value)

    return merged
    
def mergeBioClimData(bioclim_path, gdf):
    bioclim_gdf = gpd.read_file(bioclim_path )
    result_gdf = gdf.merge(bioclim_gdf, on = 'FID',how = 'left')

    return result_gdf

def mergeAllData():
    pass
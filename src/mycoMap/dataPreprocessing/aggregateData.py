import pandas as pd 
import geopandas as gpd
import numpy as np
import rasterio
import importlib
import itertools

from mycoMap import utils 
from mycoMap import geoUtils

importlib.reload(geoUtils)

#paths 
foretOuverte_path = 'data/interim/geodata/vector/CARTE_ECO/'
output_shp_path = 'data/interim/geodata/vector/sampled_grid/'
output_csv_path = 'data/interim/geodata/vector/sampled_grid/csv/'

gridded_occurences_path = 'data/interim/occurences/griddedOccurences.csv'

bioclim_path = 'data/raw/geodata/bioclim/'
perimeter_path = 'data/interim/geodata/vector/region_perimeter/'
grid_path = 'data/interim/geodata/vector/geoUtils/clustered_0.5km_grid.shp'
sampled_bioclim_path = 'data/interim/geodata/vector/sampledBioclim/'

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
                        'tree_shann' : 'mean'
}

tree_diversity_agg = {'tree_cover' : lambda dicts : len(set(itertools.chain.from_iterable(d.keys() for d in dicts))),}

def sample_bioclim_to_grid(gdf):
    # 19 bioclim layers
    biolcim_layers = range(1,20)

    # create coordinate list for occurences 
    coord_list = [(x,y) for x,y in zip(gdf['geometry'].x, gdf['geometry'].y)]

    for layer in biolcim_layers:
        layer = str(layer)
        layer = layer.zfill(2)
        print(f'Sampling {layer}')
        raster= rasterio.open(f'{bioclim_path}/QC_bio_{layer}.tif')
        samples = list(raster.sample(coord_list))
        gdf[f'bioclim_{layer}'] = [sample[0] if sample else None for sample in samples]

    gdf = gdf.drop(['geometry'], axis = 1)
    return gdf

def process_fungi_ecology_index(gridded_occurences_path, grid):

    df = pd.read_csv(gridded_occurences_path)
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

def encode_vector_fields(gdf, encoding_dict = None):

    for series_name, series in gdf.items():
        try:
            gdf[series_name] = gdf[series_name].map(encoding_dict[series_name])
            print(f'Encoded {series_name}')
        except Exception as e:
            print(e)

    return gdf

def create_occurences_gdf(occurences_path):

    col_to_keep = ['gbifID', 'order','family', 'genus','species','decimalLatitude','decimalLongitude','eventDate']
    # Load occurences 
    df = pd.read_csv(occurences_path)
    df = df[col_to_keep]
    gdf = utils.df_to_gdf(df, xy = ['decimalLongitude','decimalLatitude'])
    return gdf 


def main(grid_size = 1, debug = False, range = (0,17)):

    regions_list = utils.get_regionCodeList()
    #regions_list = regions_list[10:]
    print(regions_list)
    grid = gpd.read_file(grid_path)
    print(grid.shape)

    for i, region in enumerate(regions_list):

        #Load foret ouverte region vector data 
        gdf = gpd.read_file(foretOuverte_path + f'CARTE_ECO_{region}.shp') 
        print('Foret Ouvert gdf')
        print(gdf.head())
        gdf = gdf.to_crs(4326)

        # Convert tree cover string to dict of species percentage
        gdf = utils.convert_string_to_numeral(gdf, collumn='tree_cover')

        # Load perimeter gdf 
        perimeter_gdf = gpd.read_file(perimeter_path+f'{region}_perimeter.shp')
        
        # Clip full grid by perimeter 
        clipped_grid = geoUtils.clip_grid_per_region(perimeter_gdf,grid, debug= True, keep_cols= ['FID', 'geometry', 'block_id'])

        # foret ouvert gdf spatial join with clipped grid 
        joined_gdf = gpd.sjoin(gdf, clipped_grid, how ='inner', predicate= 'intersects')
        joined_gdf = joined_gdf.drop(['index_right'], axis = 1)

        if debug:
            print('Joined gdf')
            print(joined_gdf.head())

        #aggregate field values grouped by cell id 
        try:
            aggregated_gdf = joined_gdf.groupby('FID').agg(cell_agg_dict).reset_index()
            aggregated_gdf = aggregated_gdf.rename(columns= {'tree_cover' : 'tree_diver' })
        except Exception as e:
            print(e)

        #re-encode gdf after aggregate on categorical values to get ordinal values for raster
        #aggregated_gdf = encode_vector_fields(aggregated_gdf, encoding_dictionnary)

        if debug:
            print('Agg gdf')
            print(aggregated_gdf.head())
     
        #count how many vector items per cell 
        counts = (joined_gdf.groupby('FID').size().reset_index(name='item_count'))  
        counts = counts.astype({"item_count": 'int'})
        if debug:
            print('-'*100)
            print('Counts vector items')
            print(counts.head())

        #process fungi_ecology indexes with spatially joined occurences
        fungi_ecology_gdf = process_fungi_ecology_index(gridded_occurences_path, clipped_grid)

        if debug:
            print('-'*100)
            print('Fungi_ecology_gdf')
            print(fungi_ecology_gdf.head())

        # Grid sampled bioclims only vectorised in 0.5km grid
        if grid_size == 0.5:
            # read sampled rasters
            bioclim_gdf = gpd.read_file(sampled_bioclim_path + f'{grid_size}km_bioclim.shp')
            if not bioclim_gdf.empty:
                bioclim_gdf = geoUtils.clip_grid_per_region(perimeter_gdf,bioclim_gdf, debug= True, keep_cols= True)

            if not bioclim_gdf.empty:
                bioclim_gdf = bioclim_gdf.drop(['geometry'], axis = 1)

        if debug:
            print('-'*100)
            print('Bioclim gdf')
            print(bioclim_gdf.head())

        #merge back aggregated values in grid gdf
        result_gdf = clipped_grid.merge(aggregated_gdf, on = 'FID',how = 'left')
        result_gdf = result_gdf.merge(counts, on = 'FID',how = 'left')
        result_gdf = result_gdf.merge(fungi_ecology_gdf, on = 'FID',how = 'left')


        # check if bioclim gdf is available 
        if not bioclim_gdf.empty:
            result_gdf = result_gdf.merge(bioclim_gdf, on = 'FID',how = 'left')

        print('Final gdf')
        print(result_gdf.head())

        output_file = output_shp_path + f'{region}_grid.shp'

        try: 
            result_gdf.to_file(output_file, driver='ESRI Shapefile')
            print(f'Saved {output_file}')
            print('#'*50, f'{i+1}/{len(regions_list)}', '#'*50)
        except Exception as e:
            print("Failed to export shp")
            print(e)

        #export as csv
        output_csv = output_csv_path + f'{region}_grid.csv'
        df = utils.gdf_to_df(result_gdf)
        try:
            df.to_csv(output_csv, index = False)
        except Exception as e:
            print("Failed to export csv")
            print(e)
            
if __name__ == '__main__':
    main(grid_size = 0.5, debug = True)
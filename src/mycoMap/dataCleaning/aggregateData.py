import geopandas as gpd
import numpy as np
import rasterio
import importlib
import itertools

from .. import utils 
from .. import geoUtils

importlib.reload(geoUtils)

#paths 
foretOuverte_path = 'data/interim/geodata/vector/CARTE_ECO/'
output_path = 'data/interim/geodata/vector/sampled_grid/'
bioclim_path = 'data/raw/geodata/bioclim/'
perimeter_path = 'data/interim/geodata/vector/region_perimeter/'
geoUtils_path = 'data/interim/geodata/vector/geoUtils/'
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

def sampleOccurences_to_grid(grid, occurences_gdf):
    pass

def process_fungi_ecology_index():
    pass

def main(grid_size = 1, debug = False, range = (0,17)):

    regions_list = utils.get_regionCodeList()
    regions_list = regions_list[-1:]
    print(regions_list)
    grid = gpd.read_file(geoUtils_path + f'{grid_size}km_grid.shp')
    print(grid.shape)

    for i, region in enumerate(regions_list):

        perimeter_gdf = gpd.read_file(perimeter_path+f'{region}_perimeter.shp')
        gdf = gpd.read_file(foretOuverte_path + f'CARTE_ECO_{region}.shp') 
        print('Foret Ouvert gdf')
        print(gdf.head())
        #gdf = gpd.GeoDataFrame()
        gdf = gdf.to_crs(4326)

        gdf = utils.convert_string_to_numeral(gdf, collumn='tree_cover')

        clipped_grid = geoUtils.clip_grid_per_region(perimeter_gdf,grid, debug= True)

        if grid_size == 0.5:
            # read sampled rasters 
            bioclim_gdf = gpd.read_file(sampled_bioclim_path + f'{grid_size}km_bioclim.shp')
            if not bioclim_gdf.empty:
                bioclim_gdf = geoUtils.clip_grid_per_region(perimeter_gdf,bioclim_gdf, debug= True, keep_cols= True)

            if bioclim_gdf:
                bioclim_gdf = bioclim_gdf.drop(['geometry'], axis = 1)

        if debug:
            print('-'*100)
            print('Bioclim gdf')
            print(bioclim_gdf.head())

        # spatial join with grid 
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



        #spatial join occurences 
        #sampleOccurences_to_grid()

        #process fungi_ecology indexes
        #process_fungi_ecology_index()

        #merge back aggregated values in grid gdf
        result_gdf = clipped_grid.merge(aggregated_gdf, on = 'FID',how = 'left')
        result_gdf = result_gdf.merge(counts, on = 'FID',how = 'left')

        if not bioclim_gdf.empty:
            result_gdf = result_gdf.merge(bioclim_gdf, on = 'FID',how = 'left')

        print('Final gdf')
        print(result_gdf.head())

        output_file = output_path + f'{region}_grid.shp'

        try: 
            result_gdf.to_file(output_file, driver='ESRI Shapefile')
            print(f'Saved {output_file}')
            print('#'*50, f'{i+1}/{len(regions_list)}', '#'*50)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main(grid_size = 0.5, debug = True)
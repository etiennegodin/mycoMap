import geopandas as gpd
import pandas as pd 
import numpy as np

#Spatial Relationship Analysis

#grid 
#spatial join 
#summarize fields 
    #aggregates per field tpye 

regions_df = pd.read_csv('data/inputs/qc_regions.csv')
regions_list = []

files_path = 'data/interim/geodata/vector/CARTE_ECO/'
input_gpkg_path = 'data/raw/geodata/foretOuverte/PEE_MAJ_PROV/gpkg' 

output_path = 'data/interim/geodata/vector/aggregated'

ordinal_columns = ['ty_couv_et','cl_dens','cl_haut','cl_age_et','etagement','cl_pent','hauteur']
categorical_columns = ['dep_sur','cl_drai', 'eta_ess_pc']
gdf_columns = ['geoc_maj', 'geometry']
all_columns = ordinal_columns + categorical_columns + gdf_columns

aggregate_dict = { 'ty_couv_et': lambda x : x.mode()[0] if not x.mode().empty else np.nan,
                        'cl_dens' : lambda x : x.mode()[0] if not x.mode().empty else np.nan,
                        'cl_haut' : lambda x : x.mode()[0] if not x.mode().empty else np.nan,
                        'cl_age_et' : 'mean',
                        'etagement' : lambda x : x.mode()[0] if not x.mode().empty else np.nan,
                        'cl_pent' : lambda x : x.mode()[0] if not x.mode().empty else np.nan,
                        'hauteur' : 'mean',
                        'dep_sur' : lambda x : x.mode()[0] if not x.mode().empty else np.nan,
                        'cl_drai' : lambda x : x.mode()[0] if not x.mode().empty else np.nan,

}

pre_aggregate_encoding_dict = {
                        'cl_age_et': 
                        {
                            '10' : 10,
                            '30' : 30,
                            '50' : 50,
                            '70' : 70,
                            '90' : 90,
                            '110' : 110,
                            '120' : 120,
                            '130' : 130,
                            'VIN' : 40, # 30 a 50
                            'JIN' : 95 # 70 a 120
                        },
}

encoding_dictionnary = { 'ty_couv_et': 
                        {
                            'F' : 1,
                            'MF' : 2,
                            'MM' : 3,
                            'MR' : 4,
                            'R' : 5
                        },

                        'cl_dens':
                        {
                            'A' : 4,
                            'B' : 3,
                            'C' : 2,
                            'D' : 1,
                        },

                        'cl_haut':
                        {
                            '1' : 7,
                            '2' : 6,
                            '3' : 5,
                            '4' : 4,
                            '5' : 3,
                            '6' : 2,
                            '7' : 1,
                        },
                        'etagement': 
                        {
                            'BI' : 2,
                            'MO' : 1,
                            'MU' : 3,

                        },
                        'cl_pent':
                        {
                            'A' : 1,
                            'B' : 2,
                            'C' : 3,
                            'D' : 4,
                            'E' : 5,
                            'F' : 6,
                            'S' : 7
                        }
}


def dep_sur_dict(value):
    """
    remap sub-categories of depot surface values to main categories of soil
    """
    value = str(value)
    if value.startswith('1'):
        return 'Depot Glaciaire'
    elif value.startswith('2'):
        return 'Depot fluvio-glaciaire'
    elif value.startswith('3'):
        return 'Depot fluviatile'
    elif value.startswith('4'):
        return 'Depot lacustre'
    elif value.startswith('5'):
        return 'Depot marin'
    elif value.startswith('6'):
        return 'Depot litoral marin'
    elif value.startswith('7'):
        return 'Depot organique'
    elif value.startswith('8'):
        return 'Depot de pente'
    elif value.startswith('9'):
        return 'Depot eolien'
    elif value.startswith('R'):
        return 'Rocheux'
    else:
        return 'Autre depot'

def encode_vector_fields(gdf, encoding_dict = None):

    for series_name, series in gdf.items():
        try:
            gdf[series_name] = gdf[series_name].map(encoding_dict[series_name])
            print(f'Encoded {series_name}')
        except Exception as e:
            print(e)

    return gdf

def encode_dep_sur(gdf):
    #remap sub-categories of depot surface values to main categories of soil
    gdf['dep_sur'] = gdf['dep_sur'].apply(dep_sur_dict)
    print("Encoded 'dep_sur;")
    return gdf
if __name__ == '__main__':

    grid = gpd.read_file('data/interim/geodata/vector/grid/0.5km_grid.shp')
    #print(grid.head())
    print(grid.shape)
    for region in regions_list:

        perimeter_gdf = gpd.read_file(f'data/interim/geodata/vector/region_perimeter/{region}_perimeter.shp')
        #reproject to WSG84
        perimeter_gdf = perimeter_gdf.to_crs('EPSG:4326')
        perimeter_gdf = perimeter_gdf[['geometry']]
        
        # keep cells only in region
        grid_join = gpd.sjoin(grid,perimeter_gdf, how ='inner')
        grid_in_region = grid_join[['FID','geometry']]
        print('-'*100)
        print('Grid gdf')
        print(grid_in_region.head())

        #load foret ouverte data
        file = files_path + f'CARTE_ECO_{region}.shp'
        gdf = gpd.read_file(file)
        #gdf = gpd.read_file(file, rows = 100)
        print('-'*100)
        print('Initial vector gdf')
        print(gdf.head())

        gdf = gdf.to_crs('EPSG:4326')  #reproject to WSG84
        
        #keep only relevant columns
        gdf = gdf[all_columns]

        #encode field to aggregate 
        gdf = encode_vector_fields(gdf, pre_aggregate_encoding_dict)
        print('-'*100)
        print('Encoded gdf')
        print(gdf.head())

        # spatial join with grid 
        joined_gdf = gpd.sjoin(gdf, grid_in_region, how ='inner', predicate= 'intersects')
        joined_gdf = joined_gdf.drop(['index_right'], axis = 1)
        print('Joined gdf')
        print(joined_gdf.head())

        #aggregate field values grouped by cell id 
        aggregated_gdf = joined_gdf.groupby('FID').agg(aggregate_dict).reset_index()

        #re-encode gdf after aggregate on categorical values to get ordinal values for raster
        #aggregated_gdf = encode_vector_fields(aggregated_gdf, encoding_dictionnary)

        print('-'*100)
        print('Agg gdf')
        print(aggregated_gdf.head())

        #count how many vector items per cell 
        counts = (joined_gdf.groupby('FID').size().reset_index(name='item_count'))  
        counts = counts.astype({"item_count": 'int'})
                      
        print('-'*100)
        print('Counts vector items')
        print(counts.head())

        #merge back aggregated values in grid gdf
        result_gdf = grid_in_region.merge(aggregated_gdf, on = 'FID',how = 'left')
        result_gdf = result_gdf.merge(counts, on = 'FID',how = 'left')
        print('Final gdf')
        print(result_gdf.head())
        output_file = output_path + f'/agg_grid_{region}.shp'

        try: 
            result_gdf.to_file(output_file, driver='ESRI Shapefile')
        except Exception as e:
            print(e)

        





import pandas as pd 
import geopandas as gpd
import numpy as np
import rasterio
import utils


# Utils
def get_regionCodeList():

    regionCodes = 'data/input/table/qc_regions.csv'

    regionCodeList = []
    regionCodeDict = pd.read_csv(regionCodes).to_dict()
    regionCodeDict = regionCodeDict['region']
    for key, region in regionCodeDict.items():
        regionCodeList.append(region)
    print(regionCodeList)
    return regionCodeList

def df_to_gdf(df, xy = ['X', 'Y']):

    # Creates goepandas from dataframe with lat/long columns
    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df[xy[0]], df[xy[1]]), crs="EPSG:4326"
    )
    return gdf

def gdf_to_df(gdf):
    df = pd.DataFrame(gdf.drop(columns='geometry'))
    return df

# Clean existing data 
def stack_CARTE_ECO_MAJ(df):

    columns = [
            'ty_couv_et',
            'densite',
            'hauteur',
            'cl_age_et',
            'tree_cover']
    for col in columns:
        pattern = fr'^CARTE_ECO_MAJ_\w+_{col}$'
        for column in df.filter(regex=pattern).columns:
            #print(f"\nProcessing column: {column}")

            # Example operation: You can merge them or perform other operations
            # Here, we are stacking the selected columns and keeping the first non-null value for each row
            df[col] = df.filter(regex=pattern).stack().groupby(level=0).first()
            #df.drop(columns=df.filter(regex=pattern).columns, inplace=True)

    return df

def cleanOccurences(df):

    df = df.dropna(subset=['densite'])
    df = df.rename(columns={'HubDist': 'roadDist'})    
    df = df.drop_duplicates()
    # removes columns with less than 20% rows with data
    df = df.dropna(thresh=df.shape[0]*0.20, axis=1)

    return df

def filterColumns(df):

    occurences_cols = ['X','Y','gbifID','occurrence','kingdom','phylum','class','order','family','genus','species','eventDate','speciesKey']
    geodata_cols = ['id','HubDist', 'pop_densit','et_domi','type_couv','gr_ess','cl_dens','cl_haut','cl_age','cl_pent','dep_sur','cl_drai','type_eco','ty_couv_et','densite','hauteur','cl_age_et','tree_cover']
    df_occ = df[occurences_cols]
    df_geo = df[geodata_cols]
    
    out_df = pd.DataFrame.merge(df_occ, df_geo, left_index= True, right_index= True)
    return out_df

# Sampling new data
def sample_bioclim(gdf):
    # 19 bioclim layers
    biolcim_layers = range(1,20)
    # create coordinate list for occurences
    coord_list = [(x,y) for x,y in zip(gdf['geometry'].x, gdf['geometry'].y)]

    for layer in biolcim_layers:
        layer = str(layer)
        layer = layer.zfill(2)
        print(f'Sampling {layer}')
        raster= rasterio.open(f'data/geodata/raw/bioclim/QC_bio_{layer}.tif')

        samples = list(raster.sample(coord_list))
        gdf[f'bioclim_{layer}'] = [sample[0] if sample else None for sample in samples]

    return gdf

def sample_TWI(gdf_all, regionCodeList):

    twi_files = 'data/geodata/processed/TWI/'

    gdf_out = gpd.GeoDataFrame()

    for region in regionCodeList:

        gdf = gdf_all[gdf_all['region_code'] == region]
        #print(gdf.head())
        coord_list = [(x,y) for x,y in zip(gdf['geometry'].x, gdf['geometry'].y)]
        twi_file = f'{twi_files}{region}_merged_twi.tif'
        print(f'Sampling {region}')

        raster= rasterio.open(twi_file)
        samples = list(raster.sample(coord_list))
        gdf['twi'] = [sample[0] if sample else None for sample in samples]
        gdf_out = pd.concat([gdf_out, gdf])

    print(gdf_out)
    return gdf_out

def sample_regionCode(occ_gdf):

    regions_perimetre_file = 'data/geodata/processed/regions_perimetre/regions_perimetre.shp'

    # Creat gdf from regions perimetre
    regions_gdf = gpd.read_file(regions_perimetre_file)

    # Join two geodataframe (naturally skips points not within bounds of perimetre)
    occ_gdf = gpd.sjoin(occ_gdf, regions_gdf, predicate='within')

    # Remove unecessary collumns
    occ_gdf = occ_gdf.drop(['index_right'],axis=1)

    # Rename region_code collumn
    occ_gdf = occ_gdf.rename(columns={'idx_no_dec': 'region_code'})

    return occ_gdf

# Derive new data from existing columns
def richnessIndex(tree_cover):
    #indice de ricnesse (nb especes)
    n = len(tree_cover)
    return(n)

def shannonIndex(tree_cover):
    #indice shannon 
    #creer liste proportions d'essence
    proportions_list = []
    for key in tree_cover:
        #print(key)
        proportions_list.append(tree_cover[key])

    #numpy array
    proportions = np.array(proportions_list)

    try:
        # Vérifiez que la somme des proportions est égale à 1 (100%)
        if not np.isclose(np.sum(proportions), 1.0):
            raise ValueError("Les proportions des espèces doivent totaliser 1")
        
        # Calculez l'indice de Shannon
        shannon_index = -np.sum(proportions * np.log(proportions))
        
    except ValueError:
        # En cas d'erreur, attribuez la valeur 0 à l'indice de Shannon
        shannon_index = 0
        
    shannon_index = -np.sum(proportions * np.log(proportions))

    # Entropy 
    # SUm of surprise for each of elements
    return(shannon_index)

def processs_forest_ecology_indexes(df):

    # Convert tree cover string to dictS
    utils.convert_string_to_numeral(df)

    df['tree_diversity_index'] = df['tree_cover'].apply(richnessIndex) 
    df['tree_shannon_index'] = df['tree_cover'].apply(shannonIndex)

    return df

# Geo 
def spatial_filtering(df, count = 1):

    #from group check if worse occurence than other 
    # in a lake, bad valeus sampled, etc 


    # Keep one random row per group using a fixed seed
    df_random = df.groupby('id', group_keys=False).apply(lambda g: g.sample(n=min(len(g), count)))

    return df_random   

# Prepare data 

def encode_categoricalData(df):
        
    #geodata_dictionnary = pd.read_csv('data/geodata_dictionnary.csv', header = 0 )

    encoding_dictionnary = { 'cl_pent':
                            {
                                'A' : 6,
                                'B' : 5,
                                'C' : 4,
                                'D' : 3,
                                'E' : 2,
                                'F' : 1,
                                'S' : 10
                            },

                            'cl_drai' : 10,
                            'densite' : 10,
                            'cl_haut' : {
                                    1 : 7,
                                    2 : 6,
                                    3 : 5,
                                    4 : 4,
                                    5 : 3,
                                    6 : 2,
                                    7 : 1},
    
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
                            'cl_age': 
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
                            }

    }

    # Encode ordinal data 
    for series_name, series in df.items():
        try:
            df[series_name] = df[series_name].map(encoding_dictionnary[series_name])
        except:
            pass

    # Describe depot surface categorical data
    df['dep_sur'] = df['dep_sur'].apply(dep_sur_map_category)

    # Chnage datatypes from floats to int 
    df = df.astype({"cl_drai": 'int',
                    'densite' : 'int',
                    'speciesKey' : 'int',
                    
                     })
    
    return df

def dep_sur_map_category(value):
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

if __name__ == '__main__':

    occurences = 'data/occurences/processed/AllOccurencesInStudyAreaSample_02.csv'
    output_path = 'data/occurences/processedOccurences.csv'
    
    regionCodeList = get_regionCodeList()
    seed_value = 42  
    np.random.seed(seed_value)

    ###

    df = pd.read_csv(occurences)
    print(df.shape)

    # Merge CARTE_ECO_MAJ columns in one 
    df = stack_CARTE_ECO_MAJ(df)

    df = filterColumns(df)

    df = cleanOccurences(df)

    df = processs_forest_ecology_indexes(df)

    df = encode_categoricalData(df)

    gdf = df_to_gdf(df)

    gdf = sample_regionCode(gdf)

    gdf = sample_bioclim(gdf)

    gdf = sample_TWI(gdf, regionCodeList)

    #convert back to simple df
    df = gdf_to_df(gdf)

    df = spatial_filtering(df, count = 1)

    print(df.shape)
    print(df.columns)
    print(df.describe())

    print(df)
    
    utils.saveDfToCsv(df, output_path )
    

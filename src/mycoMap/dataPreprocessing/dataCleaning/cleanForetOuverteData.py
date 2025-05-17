import geopandas as gpd
from mycoMap.dataPreprocessing.dataIntegration import mergeForetOuverteData

# Global vars 
ordinal_columns = ['ty_couv_et','cl_dens','cl_haut','cl_age_et','etagement','cl_pent','hauteur']
categorical_columns = ['dep_sur','cl_drai', 'eta_ess_pc']
gdf_columns = ['geoc_maj', 'geometry']
all_columns = ordinal_columns + categorical_columns + gdf_columns

def main(regions_list, verbose = False):
    cleaned_foretOuvert_gdfs = []
    for region in regions_list:
        gdf, perimeter_gdf = mergeForetOuverteData.merge_region_gpkg(region)
            #keep only relevant columns
        gdf = gdf[all_columns]
        cleaned_foretOuvert_gdfs.append(gdf)

    return cleaned_foretOuvert_gdfs
import geopandas as gpd

def aggregateAllData(encoded_foretOuvert_gdfs,     verbose = False):

    for gdf in encoded_foretOuvert_gdfs:
        
        #Convert to WSG84
        gdf = gdf.to_crs(4326)

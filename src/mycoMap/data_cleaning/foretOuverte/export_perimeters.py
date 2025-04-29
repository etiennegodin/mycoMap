# run to only exprot perimeter from combineDataSourceScript
from combineDataSource import *


for r in regions_list:
    gpkg_file = input_gpkg_path + f'/CARTE_ECO_MAJ_{r}.gpkg'

    layers = find_gpkg_layers(gpkg_file)

    
    perimeter_output_path = 'data/interim/geodata/vector/region_perimeter' + f'/{r}_perimeter.shp'
    perimeter_gdf = combine_gpkg_layers(gpkg_file, layers = [layers[0]])
    write_gdf(perimeter_gdf, perimeter_output_path)
             
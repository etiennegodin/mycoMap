
input_gpkg_path = 'data/raw/geodata/foretOuverte/PEE_MAJ_PROV/CARTE_ECO_MAJ_21E_GPKG/CARTE_ECO_MAJ_21E.gpkg' 
output_shp_path = 'data/interim/geodata/vector/CARTE_ECO/CARTE_ECO_MAJ_21E.shp'



import geopandas as gpd 
import fiona

layer_name = None

try:
    print(f"Layers available in '{input_gpkg_path}':")
    print(fiona.listlayers(input_gpkg_path))
except Exception as e:
    print(f"Could not list layers (maybe file doesn't exist?): {e}")
    # Decide if you want to exit or continue assuming the default layer

    # exit()

layer_name = 'pee_maj_21e'

# --- Read the GeoPackage Layer ---
try:
    print(f"Reading layer '{layer_name if layer_name else 'default'}' from GeoPackage: {input_gpkg_path}...")
    gdf = gpd.read_file(input_gpkg_path, layer=layer_name)
    print(f"Read {len(gdf)} features.")

except Exception as e:
    print(f"Error reading GeoPackage file: {e}")
    print("Please check the file path and ensure the layer name (if specified) is correct.")
    exit() # Exit if reading fails

# --- Write to Shapefile ---
try:
    print(f"Writing GeoDataFrame to Shapefile: {output_shp_path}...")
    # The driver is usually inferred from the extension,
    # but specifying it is robust.
    gdf.to_file(output_shp_path, driver='ESRI Shapefile')
    print("Conversion successful!")

except Exception as e:
    print(f"Error writing Shapefile: {e}")
    # Common Shapefile errors relate to long field names or mixed geometry typ
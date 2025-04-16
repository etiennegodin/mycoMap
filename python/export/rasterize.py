import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
import numpy as np
import rasterio
from rasterio.transform import from_origin
from rasterio.features import rasterize
import os 


def rasterise_csv_points(region, field_name = 'fungi_diversity_index', pixel_size = 0.001, buffer_size = 0.00125 ):

    # Load CSV
    csv_file = f"data/output/regions/derivedRegion{region}.csv"  # Replace with your CSV file
    df = pd.read_csv(csv_file)

    # Convert to GeoDataFrame
    geometry = [Point(xy) for xy in zip(df['X'], df['Y'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")  # Adjust CRS if necessary

    buffer_size = buffer_size  # Example buffer size in degrees
    gdf['geometry'] = gdf.geometry.buffer(buffer_size)



    # Define rasterization parameters
    pixel_size = pixel_size  # Pixel size in degrees (adjust based on your data)
    x_min, y_min, x_max, y_max = gdf.total_bounds
    width = int((x_max - x_min) / pixel_size)
    height = int((y_max - y_min) / pixel_size)

    print(width,height)

    # Create transformation
    transform = from_origin(x_min, y_max, pixel_size, pixel_size)

    # Prepare shapes for rasterization
    field_name = field_name  # Replace with the field to rasterize
    shapes = ((geom, value) for geom, value in zip(gdf.geometry, gdf[field_name]))

    # Rasterize
    raster = rasterize(
        shapes,
        out_shape=(height, width),
        transform=transform,
        fill=-9999,  # No-data value
        dtype="float32",
    )

    # Save raster to file
    output_raster = f"data/output/rasters/{field_name}_{region}.tif"
    with rasterio.open(
        output_raster,
        "w",
        driver="GTiff",
        height=height,
        width=width,
        count=1,
        dtype="float32",
        crs=gdf.crs,
        transform=transform,
    ) as dst:
        dst.write(raster, 1)

    print(f"Raster saved to {output_raster}")


if __name__ == '__main__':


    regions_list = os.listdir('data/geodata/regions_data')

    for region in regions_list:
        print(f'Region : {region}')
        rasterise_csv_points(region, field_name= 'shannon_index_fungi')
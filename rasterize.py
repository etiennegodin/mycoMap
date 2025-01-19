import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
import numpy as np
import rasterio
from rasterio.transform import from_origin
from rasterio.features import rasterize

# Load your data
csv_file = "data/output/regions/derivedRegion21E.csv.csv"  # Replace with your CSV file
df = pd.read_csv(csv_file)
geometry = [Point(xy) for xy in zip(df['X'], df['Y'])]
gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

# Define rasterization parameters
pixel_size = 0.001  # Adjust based on your data
x_min, y_min, x_max, y_max = gdf.total_bounds
width = int((x_max - x_min) / pixel_size)
height = int((y_max - y_min) / pixel_size)
transform = from_origin(x_min, y_max, pixel_size, pixel_size)

# Create an empty raster
raster = np.zeros((height, width), dtype=np.float32)
counts = np.zeros((height, width), dtype=np.float32)

# Map each point to the raster grid
for _, row in gdf.iterrows():
    col = int((row.geometry.x - x_min) / pixel_size)
    row_ = int((y_max - row.geometry.y) / pixel_size)
    if 0 <= row_ < height and 0 <= col < width:
        raster[row_, col] += row["shannon_index_fungi"]  # Sum values
        counts[row_, col] += 1  # Count occurrences

# Calculate the average for overlapping points
raster = np.where(counts > 0, raster / counts, 0)  # Replace nodata with -9999

# Save the raster
output_raster = "blended_raster.tif"
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

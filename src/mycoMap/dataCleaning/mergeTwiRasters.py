import rasterio
from rasterio.merge import merge
from rasterio.enums import Resampling
from rasterio.warp import calculate_default_transform, reproject

import os
import pandas as pd
from mycoMap.utils import get_regionCodeList


def resample_raster(src, scale_factor):
    """Resample raster to lower resolution before reprojection."""
    # Calculate new dimensions
    new_width = src.width // scale_factor
    new_height = src.height // scale_factor

    # Resample raster data
    new_data = src.read(
        out_shape=(src.count, new_height, new_width),
        resampling=Resampling.average  # Options: nearest, bilinear, cubic
    )

    # Update transform
    new_transform = src.transform * src.transform.scale(
        (src.width / new_width), (src.height / new_height)
    )

    # Update metadata
    new_meta = src.meta.copy()
    new_meta.update({"height": new_height, "width": new_width, "transform": new_transform})

    return new_data, new_meta

def reproject_raster(src, target_crs, temp_filename="temp_reprojected.tif"):
    """Reproject raster to target CRS and ensure the file is closed."""
    src_crs = src.crs
    transform, width, height = calculate_default_transform(
        src_crs, target_crs, src.width, src.height, *src.bounds
    )

    new_meta = src.meta.copy()
    new_meta.update({"crs": target_crs, "transform": transform, "width": width, "height": height})

    # Write reprojected data to a temporary file
    with rasterio.open(temp_filename, "w", **new_meta) as dst:
        for i in range(1, src.count + 1):
            reproject(
                source=rasterio.band(src, i),
                destination=rasterio.band(dst, i),
                src_transform=src.transform,
                src_crs=src_crs,
                dst_transform=transform,
                dst_crs=target_crs,
                resampling=Resampling.bilinear
            )

    # Open the file AFTER closing the write process
    reprojected_src = rasterio.open(temp_filename)
    return reprojected_src


def merge_twi_rasters(regionCodeList, scale_factor):
    
    twi_files = 'data/raw/geodata/raster/twi'
    target_crs = "EPSG:4326"

    for idx, region in enumerate(regionCodeList):
        print(region)
        print(f'{idx +1} / {len(regionCodeList)}')
        output_path = f'data/interim/geodata/raster/twi{region}_merged_twi.tif'

        if os.path.exists(output_path):
            print(f'{output_path} already exists, skipping')
        else:
            regionFiles = []

            for file in os.listdir(twi_files):
                if str(file).startswith(region):
                    regionFiles.append(twi_files + file)
                else:
                    pass
            print(len(regionFiles), 'files')

            processed_rasters = []

            for idx, raster in enumerate(regionFiles):
                try:
                    with rasterio.open(raster) as src:
                    # Step 1: Resample first (downscale)
                        new_data, new_meta = resample_raster(src, scale_factor)

                        # Save temporary resampled raster
                        temp_resampled = f"temp_resampled_{os.path.basename(raster)}"
                        with rasterio.open(temp_resampled, "w", **new_meta) as dst:
                            dst.write(new_data)

                        #print('Resample')
                        # Step 2: Reproject the resampled raster
                        with rasterio.open(temp_resampled) as resampled_src:
                            reprojected_src = reproject_raster(resampled_src, target_crs, temp_filename = f'temp_reprojected_{idx}.tif')
                            processed_rasters.append(reprojected_src)
                            #reprojected_src.close()
                        #print('Reproj')
                except:
                    pass


            print('processed rasters')
            # Merge all processed rasters
            mosaic, mosaic_transform = merge(processed_rasters)

            # Update metadata based on mosaic output
            meta = processed_rasters[0].meta.copy()
            meta.update(
                {"driver": "GTiff", "height": mosaic.shape[1], "width": mosaic.shape[2], "transform": mosaic_transform}
            )

            # Save the lower-resolution mosaic
            with rasterio.open(output_path, "w", **meta) as dst:
                dst.write(mosaic)
            print(f'Saving merged {region} twi raster')

            # Close raster files
            for src in processed_rasters:
                src.close()

if __name__ == '__main__':

    regionCodeList = get_regionCodeList()

    merge_twi_rasters(regionCodeList, scale_factor = 20)
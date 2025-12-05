"""Goal: reproject CLC2018 landcover and align to irradiance 4.4 km grid (nearest neighbor).
Inputs: source raster data/raw/U2018_CLC2018_V2020_20u1.tif, template data/interim/irradiance_reproj.tif.
Output: aligned landcover raster data/interim/landcover_resampled_to_irradiance.tif."""

from pathlib import Path

import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling

SRC = Path("data/raw/U2018_CLC2018_V2020_20u1.tif")
TEMPLATE = Path("data/interim/irradiance_reproj.tif")
OUT = Path("data/interim/landcover_resampled_to_irradiance.tif")


def main():
    with rasterio.open(TEMPLATE) as tgt:  # open target raster, get shape/transform/CRS
        tgt_meta = tgt.profile
        tgt_shape = tgt.shape
        tgt_transform = tgt.transform
        tgt_crs = tgt.crs
        tgt_mask = tgt.read(1, masked=True).mask  # align to irradiance mask

    with rasterio.open(SRC) as src:
        src_data = src.read(1)
        src_meta = src.meta.copy()

    dest = np.full(tgt_shape, src_meta.get("nodata", 0), dtype=src_data.dtype)
    reproject(  # nearest-neighbor reprojection/resample
        source=src_data,
        destination=dest,
        src_transform=src.transform,
        src_crs=src.crs,
        dst_transform=tgt_transform,
        dst_crs=tgt_crs,
        resampling=Resampling.nearest,
    )
    dest = np.ma.array(dest, mask=tgt_mask)  # apply irradiance mask

    tgt_meta.update(dtype=src_meta["dtype"], nodata=src_meta.get("nodata"), compress="lzw")
    with rasterio.open(OUT, "w", **tgt_meta) as dst:
        dst.write(dest.filled(src_meta.get("nodata", 0)), 1)  # write aligned landcover


if __name__ == "__main__":
    main()

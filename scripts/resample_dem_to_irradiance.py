"""Resample DEM to the irradiance grid (~4.4 km)."""

from pathlib import Path
import sys

import rasterio
from rasterio.warp import Resampling, reproject

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # allow importing src modules

DEM_SRC = Path("data/interim/dem_clipped.tif")
IRR_REF = Path("data/interim/irradiance_reproj.tif")
DEM_OUT = Path("data/interim/dem_resampled_to_irradiance.tif")


if __name__ == "__main__":
    with rasterio.open(IRR_REF) as ref, rasterio.open(DEM_SRC) as src:
        profile = ref.profile.copy()  # target grid shape/transform/crs matches irradiance
        profile.update(dtype=src.dtypes[0], nodata=src.nodata)
        DEM_OUT.parent.mkdir(parents=True, exist_ok=True)
        with rasterio.open(DEM_OUT, "w", **profile) as dst:
            reproject(
                source=rasterio.band(src, 1),          # DEM source band
                destination=rasterio.band(dst, 1),     # write onto irradiance grid
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=ref.transform,
                dst_crs=ref.crs,
                resampling=Resampling.bilinear,        # bilinear for continuous data
            )
    print(f"Saved resampled DEM to: {DEM_OUT}")

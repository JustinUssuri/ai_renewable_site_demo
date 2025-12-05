"""Tiny step: load DEM resampled to the irradiance grid with unified defaults and masking.
Input: data/interim/dem_resampled_to_irradiance.tif by default (custom path optional).
Output: masked array (numpy.ma.MaskedArray) and rasterio profile."""

from pathlib import Path

import rasterio

from src.config import INTERIM_DIR

DEM_PATH = INTERIM_DIR / "dem_resampled_to_irradiance.tif"


def load_dem(path: str | Path | None = None):
    """Load DEM aligned to irradiance grid; return masked array and profile."""
    dem_path = Path(path) if path else DEM_PATH  # prefer provided path, else default
    if not dem_path.exists():
        raise FileNotFoundError(f"DEM file not found: {dem_path}")

    with rasterio.open(dem_path) as ds:  # open DEM raster
        data = ds.read(1, masked=True)   # masked array, nodata auto-masked
        profile = ds.profile             # keep metadata for alignment/output

    return data, profile

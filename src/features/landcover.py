"""Tiny step: load landcover raster with unified defaults and masking.
Input: data/interim/landcover_resampled_to_irradiance.tif by default (custom path optional).
Output: masked array (numpy.ma.MaskedArray) and rasterio profile."""

from pathlib import Path

import rasterio

from src.config import INTERIM_DIR, ROOT_DIR

LANDCOVER_RESAMPLED = INTERIM_DIR / "landcover_resampled_to_irradiance.tif"
LANDCOVER_CLIPPED = INTERIM_DIR / "landcover_clipped.tif"  # fallback: clipped-only version


def load_landcover(path: str | Path | None = None):
    """Load landcover raster; return masked array and profile."""
    if path:
        lc_path = Path(path)  # use provided path
        if not lc_path.is_absolute():
            lc_path = ROOT_DIR / lc_path  # resolve relative to project root
    else:
        lc_path = LANDCOVER_RESAMPLED  # default to resampled/aligned file
    if not lc_path.exists():  # if missing, try fallback
        fallback = LANDCOVER_CLIPPED
        if fallback.exists():
            lc_path = fallback
        else:
            raise FileNotFoundError(f"Landcover file not found: {lc_path}")

    with rasterio.open(lc_path) as ds:     # open landcover raster
        data = ds.read(1, masked=True)     # masked array, nodata auto-masked
        profile = ds.profile               # keep metadata for alignment/output

    return data, profile

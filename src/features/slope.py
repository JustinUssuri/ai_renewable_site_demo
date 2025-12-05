"""Tiny step: load slope raster for reuse in feature engineering.
Input: data/interim/slope_resampled_to_irradiance.tif by default (custom path optional).
Output: masked array (numpy.ma.MaskedArray) and rasterio profile."""

from pathlib import Path

import rasterio

from src.config import INTERIM_DIR

SLOPE_PATH = INTERIM_DIR / "slope_resampled_to_irradiance.tif"


def load_slope(path: str | Path | None = None):
    """Load slope raster aligned to irradiance grid; return masked array and profile."""
    slope_path = Path(path) if path else SLOPE_PATH  # prefer provided path, else default
    if not slope_path.exists():
        raise FileNotFoundError(f"Slope file not found: {slope_path}")

    with rasterio.open(slope_path) as ds:  # open slope raster
        data = ds.read(1, masked=True)     # masked array, nodata auto-masked
        profile = ds.profile               # keep metadata for writing/QA

    return data, profile

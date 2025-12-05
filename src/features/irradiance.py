"""Tiny step: load irradiance raster with unified defaults and masking.
Input: data/interim/irradiance_reproj.tif by default (custom path optional).
Output: masked array (numpy.ma.MaskedArray) and rasterio profile."""

from pathlib import Path

import rasterio

from src.config import INTERIM_DIR

IRRADIANCE_PATH = INTERIM_DIR / "irradiance_reproj.tif"


def load_irradiance(path: str | Path | None = None):
    """Load irradiance raster aligned to study area; return masked array and profile."""
    irr_path = Path(path) if path else IRRADIANCE_PATH  # prefer provided path, else default
    if not irr_path.exists():
        raise FileNotFoundError(f"Irradiance file not found: {irr_path}")

    with rasterio.open(irr_path) as ds:   # open irradiance raster
        data = ds.read(1, masked=True)    # masked array, nodata auto-masked
        profile = ds.profile              # keep metadata for alignment/output

    return data, profile

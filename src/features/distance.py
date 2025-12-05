"""Tiny step: load road/powerline distance rasters with unified defaults and masking.
Input: data/interim/dist_roads.tif and data/interim/dist_grid.tif by default (custom path optional).
Output: masked array (numpy.ma.MaskedArray) and rasterio profile."""

from pathlib import Path

import rasterio

from src.config import INTERIM_DIR

DIST_ROADS = INTERIM_DIR / "dist_roads.tif"
DIST_GRID = INTERIM_DIR / "dist_grid.tif"


def load_dist_roads(path: str | Path | None = None):
    """Load road distance raster; return masked array and profile."""
    dist_path = Path(path) if path else DIST_ROADS  # prefer provided path, else default
    if not dist_path.exists():
        raise FileNotFoundError(f"Road distance file not found: {dist_path}")

    with rasterio.open(dist_path) as ds:  # open road distance raster
        data = ds.read(1, masked=True)    # masked array, nodata auto-masked
        profile = ds.profile              # keep metadata for alignment/output

    return data, profile


def load_dist_grid(path: str | Path | None = None):
    """Load powerline distance raster; return masked array and profile."""
    dist_path = Path(path) if path else DIST_GRID  # prefer provided path, else default
    if not dist_path.exists():
        raise FileNotFoundError(f"Powerline distance file not found: {dist_path}")

    with rasterio.open(dist_path) as ds:  # open powerline distance raster
        data = ds.read(1, masked=True)    # masked array, nodata auto-masked
        profile = ds.profile              # keep metadata for alignment/output

    return data, profile

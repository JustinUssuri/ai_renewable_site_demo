"""Reproject irradiance raster to target CRS (EPSG:2157)."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # allow importing src modules

from src.data.preprocess import reproject_raster


# Use clipped WGS84 irradiance subset as input
SRC = Path("data/interim/irradiance_clipped.tif")
DST = Path("data/interim/irradiance_reproj.tif")


if __name__ == "__main__":
    if not SRC.exists():
        raise SystemExit(f"Irradiance source not found: {SRC}")
    reproject_raster(SRC, DST)  # reproject to target CRS (default EPSG:2157)
    print(f"Saved reprojected irradiance to: {DST}")

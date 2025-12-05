"""Quick QA script for DEM raster metadata."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # ensure src modules importable

from src.data.qa import print_raster_summary


DEM_PATH = Path("data/interim/dem_clipped.tif")


if __name__ == "__main__":
    if not DEM_PATH.exists():
        raise SystemExit(f"DEM file not found: {DEM_PATH}")
    print_raster_summary(DEM_PATH)

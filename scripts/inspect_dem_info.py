"""Quickly inspect raw DEM metadata."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # ensure src modules importable

from src.data.qa import print_raster_summary

DEM_PATH = Path("data/raw/ireland_dsm_30m.tif")


if __name__ == "__main__":
    if not DEM_PATH.exists():
        raise FileNotFoundError(f"DEM not found: {DEM_PATH}")
    print_raster_summary(DEM_PATH)

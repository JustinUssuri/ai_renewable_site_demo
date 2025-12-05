import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))  # ensure src importable

from src.config import INTERIM_DIR, RAW_DIR
from src.data.preprocess import reproject_raster


def main() -> None:
    src_raster = RAW_DIR / "ireland_dsm_30m.tif"
    dst_raster = INTERIM_DIR / "dem_reproj.tif"
    if not src_raster.exists():
        raise FileNotFoundError(f"DEM not found: {src_raster}")
    reproject_raster(src_raster, dst_raster)  # call common reprojection helper
    print(f"Reprojected DEM written to {dst_raster}")


if __name__ == "__main__":
    main()

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))  # ensure src modules importable

from src.config import INTERIM_DIR
from src.data.preprocess import clip_raster_to_boundary, load_region_boundary


def main() -> None:
    src_raster = INTERIM_DIR / "dem_reproj.tif"
    dst_raster = INTERIM_DIR / "dem_clipped.tif"
    if not src_raster.exists():
        raise FileNotFoundError(f"DEM not found: {src_raster}")
    boundary_gdf = load_region_boundary()  # read study boundary
    clip_raster_to_boundary(src_raster, dst_raster, boundary_gdf)  # perform clip
    print(f"Clipped DEM written to {dst_raster}")


if __name__ == "__main__":
    main()

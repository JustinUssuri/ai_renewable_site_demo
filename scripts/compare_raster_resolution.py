"""Compare CRS/resolution/bounds of DEM and irradiance rasters."""

from pathlib import Path
import sys

import rasterio

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # allow importing src modules

DEM_PATH = Path("data/interim/dem_clipped.tif")
IRR_PATH = Path("data/interim/irradiance_reproj.tif")


def summarize(path: Path):
    """Return (crs, res, bounds)."""

    with rasterio.open(path) as ds:
        return ds.crs, ds.res, ds.bounds


if __name__ == "__main__":
    dem_crs, dem_res, dem_bounds = summarize(DEM_PATH)
    irr_crs, irr_res, irr_bounds = summarize(IRR_PATH)

    print("DEM CRS:", dem_crs)
    print("DEM res (m):", dem_res)
    print("DEM bounds:", dem_bounds)
    print("Irradiance CRS:", irr_crs)
    print("Irradiance res (m):", irr_res)
    print("Irradiance bounds:", irr_bounds)
    ratio_x = irr_res[0] / dem_res[0]
    ratio_y = irr_res[1] / dem_res[1]
    print(f"Resolution ratio (irr/dem): {ratio_x:.1f}x, {ratio_y:.1f}x")  # irradiance pixels vs DEM

"""Compute slope from high-res DEM and aggregate to irradiance grid (~4.4 km)."""

from pathlib import Path
import sys

import numpy as np
import rasterio
from rasterio.warp import Resampling, reproject

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # 允许导入 src 模块

DEM_SRC = ROOT / "data/interim/dem_clipped.tif"
IRR_REF = ROOT / "data/interim/irradiance_reproj.tif"
SLOPE_OUT = ROOT / "data/interim/slope_resampled_to_irradiance.tif"


def compute_slope_deg(dem_array: np.ma.MaskedArray, transform, nodata: float | None) -> tuple[np.ndarray, float]:
    """Calculate slope in degrees using central differences."""
    pixel_x = transform.a
    pixel_y = abs(transform.e)  # transform.e is negative for north-up rasters

    dem_filled = dem_array.filled(np.nan).astype("float32")
    grad_y, grad_x = np.gradient(dem_filled, pixel_y, pixel_x)  # y first, then x
    slope_rad = np.arctan(np.sqrt(grad_x**2 + grad_y**2))
    slope_deg = np.degrees(slope_rad)

    nodata_value = nodata if nodata is not None else -9999.0
    slope_deg = np.where(np.isnan(dem_filled), np.nan, slope_deg)
    slope_deg = np.where(np.isfinite(slope_deg), slope_deg, nodata_value).astype("float32")
    return slope_deg, float(nodata_value)


if __name__ == "__main__":
    if not DEM_SRC.exists():
        raise FileNotFoundError(f"DEM not found: {DEM_SRC}")
    if not IRR_REF.exists():
        raise FileNotFoundError(f"Irradiance reference not found: {IRR_REF}")

    with rasterio.open(DEM_SRC) as dem_ds, rasterio.open(IRR_REF) as ref_ds:
        dem_data = dem_ds.read(1, masked=True)
        slope_deg, nodata_value = compute_slope_deg(dem_data, dem_ds.transform, dem_ds.nodata)

        dst_profile = ref_ds.profile.copy()
        dst_profile.update(dtype="float32", nodata=nodata_value, count=1)

        destination = np.full((ref_ds.height, ref_ds.width), nodata_value, dtype="float32")
        reproject(
            source=slope_deg,
            destination=destination,
            src_transform=dem_ds.transform,
            src_crs=dem_ds.crs,
            dst_transform=ref_ds.transform,
            dst_crs=ref_ds.crs,
            src_nodata=nodata_value,
            dst_nodata=nodata_value,
            resampling=Resampling.average,  # aggregate high-res slope to 4.4 km grid
        )

        # 对齐辐照度掩膜：辐照度 nodata 的地方，坡度也设为 nodata
        irr_arr = ref_ds.read(1)
        destination[irr_arr == ref_ds.nodata] = nodata_value

    SLOPE_OUT.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(SLOPE_OUT, "w", **dst_profile) as dst:
        dst.write(destination, 1)

    valid = destination[destination != nodata_value]
    if valid.size:
        print(
            f"Saved slope raster aligned to irradiance grid: {SLOPE_OUT}\n"
            f"Valid cells: {valid.size}, min={valid.min():.2f}, max={valid.max():.2f}, mean={valid.mean():.2f}"
        )
    else:
        print(f"Saved slope raster aligned to irradiance grid (no valid cells found): {SLOPE_OUT}")

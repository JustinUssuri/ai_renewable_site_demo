"""Clip irradiance raster to Ireland boundary (keep WGS84)."""

from pathlib import Path
import sys

import rasterio
from rasterio.features import geometry_mask
from rasterio.windows import from_bounds

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # ensure src modules importable

from src.data.preprocess import load_region_boundary


SRC = Path("data/raw/gh_0_year_sarah2.tif")
DST = Path("data/interim/irradiance_clipped.tif")


if __name__ == "__main__":
    boundary = load_region_boundary(target_crs="EPSG:4326")  # boundary in WGS84
    with rasterio.open(SRC) as src:
        bbox = boundary.total_bounds  # lon_min, lat_min, lon_max, lat_max
        window = from_bounds(*bbox, transform=src.transform)  # compute window
        data = src.read(1, window=window, masked=False)  # read window, ignore mask
        out_transform = src.window_transform(window)  # updated transform
        mask_geom = boundary.geometry.values  # polygons
        geom_mask = geometry_mask(mask_geom, transform=out_transform, invert=True, out_shape=data.shape)  # True inside region
        data[~geom_mask] = src.nodata or -9999  # nodata outside region
        profile = src.profile.copy()
        profile.update(
            height=data.shape[0],
            width=data.shape[1],
            transform=out_transform,
        )
    DST.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(DST, "w", **profile) as dst:
        dst.write(data, 1)  # write clipped raster
    print(f"Saved clipped irradiance to: {DST}")

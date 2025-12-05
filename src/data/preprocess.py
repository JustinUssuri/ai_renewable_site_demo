"""Data preprocessing helpers."""

import os
from pathlib import Path

import geopandas as gpd
import rasterio
from rasterio.mask import mask
from rasterio.warp import Resampling, calculate_default_transform, reproject

from src.config import RAW_DIR, TARGET_CRS


def load_region_boundary(
    boundary_path: Path | None = None,
    target_crs: str = TARGET_CRS,
) -> gpd.GeoDataFrame:
    """Load study area boundary and normalize CRS."""
    os.environ.setdefault("OGR_GEOJSON_MAX_OBJ_SIZE", "0")  # allow large GeoJSON
    path = boundary_path or RAW_DIR / "region_boundary.geojson"
    if not path.exists():
        raise FileNotFoundError(f"Boundary file not found: {path}")

    boundary_gdf = gpd.read_file(path)        # dissolved national boundary
    if boundary_gdf.crs is None:
        raise ValueError(f"{path} missing CRS")
    boundary_gdf = boundary_gdf.to_crs(target_crs)  # reproject to target CRS
    return boundary_gdf


def reproject_raster(
    src_path: str | Path,
    dst_path: str | Path,
    target_crs: str = TARGET_CRS,
) -> Path:
    """Reproject a single raster to target CRS."""
    src_path = Path(src_path)
    dst_path = Path(dst_path)
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(src_path) as src:  # open source raster
        if src.crs is None:
            raise ValueError(f"{src_path} missing CRS")
        transform, width, height = calculate_default_transform(
            src.crs, target_crs, src.width, src.height, *src.bounds
        )
        profile = src.profile.copy()
        profile.update(
            {"crs": target_crs, "transform": transform, "width": width, "height": height}
        )
        with rasterio.open(dst_path, "w", **profile) as dst:
            for band in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, band),              # read source band
                    destination=rasterio.band(dst, band),         # write to target
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=target_crs,
                    resampling=Resampling.bilinear,               # bilinear for continuous data
                )
    return dst_path


def clip_raster_to_boundary(
    src_path: str | Path,
    dst_path: str | Path,
    boundary_gdf: gpd.GeoDataFrame,
) -> Path:
    """Clip raster to a given boundary."""
    src_path = Path(src_path)
    dst_path = Path(dst_path)
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(src_path) as src:
        geoms = boundary_gdf.to_crs(src.crs).geometry  # align boundary CRS to raster
        out_image, out_transform = mask(src, geoms, crop=True)
        profile = src.profile.copy()
        profile.update(
            {
                "height": out_image.shape[1],
                "width": out_image.shape[2],
                "transform": out_transform,
                "nodata": src.nodata,
            }
        )
    with rasterio.open(dst_path, "w", **profile) as dst:
        dst.write(out_image)  # write clipped raster
    return dst_path

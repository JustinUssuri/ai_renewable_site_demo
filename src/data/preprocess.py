"""数据预处理工具函数。"""

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
    """读取研究区域边界并统一 CRS。"""
    os.environ.setdefault("OGR_GEOJSON_MAX_OBJ_SIZE", "0")  # 允许读取大型 GeoJSON
    path = boundary_path or RAW_DIR / "region_boundary.geojson"
    if not path.exists():
        raise FileNotFoundError(f"找不到边界文件：{path}")

    boundary_gdf = gpd.read_file(path)        # 读取 dissolve 后的全国边界
    if boundary_gdf.crs is None:
        raise ValueError(f"{path} 缺少 CRS 信息")
    boundary_gdf = boundary_gdf.to_crs(target_crs)  # 转到目标坐标系
    return boundary_gdf


def reproject_raster(
    src_path: str | Path,
    dst_path: str | Path,
    target_crs: str = TARGET_CRS,
) -> Path:
    """将单个栅格重投影到目标坐标系。"""
    src_path = Path(src_path)
    dst_path = Path(dst_path)
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(src_path) as src:  # 打开源 DEM 栅格
        if src.crs is None:
            raise ValueError(f"{src_path} 缺少 CRS 信息")
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
                    source=rasterio.band(src, band),              # 逐波段读取源栅格
                    destination=rasterio.band(dst, band),         # 写入目标栅格
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=target_crs,
                    resampling=Resampling.bilinear,               # 用双线性 resample 保证连续性
                )
    return dst_path


def clip_raster_to_boundary(
    src_path: str | Path,
    dst_path: str | Path,
    boundary_gdf: gpd.GeoDataFrame,
) -> Path:
    """裁剪栅格到既有边界范围。"""
    src_path = Path(src_path)
    dst_path = Path(dst_path)
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(src_path) as src:
        geoms = boundary_gdf.to_crs(src.crs).geometry  # 边界统一到栅格的坐标系
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
        dst.write(out_image)  # 将裁剪结果写入磁盘
    return dst_path

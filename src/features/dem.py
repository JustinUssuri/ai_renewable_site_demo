"""小步目标：封装 DEM（重采样到辐照度网格）加载函数，统一默认路径与掩膜处理。
输入：默认读取 data/interim/dem_resampled_to_irradiance.tif，可选自定义路径。
输出：返回掩膜数组（numpy.ma.MaskedArray）与 rasterio profile 元数据。"""

from pathlib import Path

import rasterio

from src.config import INTERIM_DIR

DEM_PATH = INTERIM_DIR / "dem_resampled_to_irradiance.tif"


def load_dem(path: str | Path | None = None):
    """加载对齐辐照度网格的 DEM 栅格，返回掩膜数组与 profile。"""
    dem_path = Path(path) if path else DEM_PATH  # 传入路径优先，否则用默认
    if not dem_path.exists():
        raise FileNotFoundError(f"DEM 文件不存在：{dem_path}")

    with rasterio.open(dem_path) as ds:  # 打开 DEM 栅格
        data = ds.read(1, masked=True)   # 读取为掩膜数组，nodata 自动 masked
        profile = ds.profile             # 保留元数据，便于对齐与写出

    return data, profile

"""小步目标：封装土地利用栅格加载函数，统一默认路径与掩膜处理。
输入：默认读取 data/interim/landcover_resampled_to_irradiance.tif，可选自定义路径。
输出：返回掩膜数组（numpy.ma.MaskedArray）与 rasterio profile 元数据。"""

from pathlib import Path

import rasterio

from src.config import INTERIM_DIR, ROOT_DIR

LANDCOVER_RESAMPLED = INTERIM_DIR / "landcover_resampled_to_irradiance.tif"
LANDCOVER_CLIPPED = INTERIM_DIR / "landcover_clipped.tif"  # 备用：仅裁剪未重采样


def load_landcover(path: str | Path | None = None):
    """加载土地利用栅格，返回掩膜数组与 profile。"""
    if path:
        lc_path = Path(path)  # 使用传入路径
        if not lc_path.is_absolute():
            lc_path = ROOT_DIR / lc_path  # 相对路径改为相对项目根目录
    else:
        lc_path = LANDCOVER_RESAMPLED  # 默认用对齐辐照度的重采样文件
    if not lc_path.exists():  # 如果默认文件不存在，尝试备用裁剪文件
        fallback = LANDCOVER_CLIPPED
        if fallback.exists():
            lc_path = fallback
        else:
            raise FileNotFoundError(f"土地利用文件不存在：{lc_path}")

    with rasterio.open(lc_path) as ds:     # 打开土地利用栅格
        data = ds.read(1, masked=True)     # 读取为掩膜数组，nodata 自动 masked
        profile = ds.profile               # 保留元数据，便于对齐与写出

    return data, profile

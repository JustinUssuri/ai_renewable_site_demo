"""小步目标：封装坡度加载函数，便于后续特征工程复用。
输入：默认读取 data/interim/slope_resampled_to_irradiance.tif，可选自定义路径。
输出：返回掩膜数组（numpy.ma.MaskedArray）与 rasterio profile 元数据。"""

from pathlib import Path

import rasterio

from src.config import INTERIM_DIR

SLOPE_PATH = INTERIM_DIR / "slope_resampled_to_irradiance.tif"


def load_slope(path: str | Path | None = None):
    """加载对齐辐照度网格的坡度栅格，返回掩膜数组与 profile。"""
    slope_path = Path(path) if path else SLOPE_PATH  # 传入路径优先，否则用默认
    if not slope_path.exists():
        raise FileNotFoundError(f"坡度文件不存在：{slope_path}")

    with rasterio.open(slope_path) as ds:  # 打开坡度栅格
        data = ds.read(1, masked=True)     # 读取为掩膜数组，nodata 自动 masked
        profile = ds.profile               # 保留元数据，便于后续写出或 QA

    return data, profile

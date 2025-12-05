"""小步目标：封装辐照度栅格加载函数，统一默认路径与掩膜处理。
输入：默认读取 data/interim/irradiance_reproj.tif，可选自定义路径。
输出：返回掩膜数组（numpy.ma.MaskedArray）与 rasterio profile 元数据。"""

from pathlib import Path

import rasterio

from src.config import INTERIM_DIR

IRRADIANCE_PATH = INTERIM_DIR / "irradiance_reproj.tif"


def load_irradiance(path: str | Path | None = None):
    """加载对齐研究区的辐照度栅格，返回掩膜数组与 profile。"""
    irr_path = Path(path) if path else IRRADIANCE_PATH  # 传入路径优先，否则用默认
    if not irr_path.exists():
        raise FileNotFoundError(f"辐照度文件不存在：{irr_path}")

    with rasterio.open(irr_path) as ds:   # 打开辐照度栅格
        data = ds.read(1, masked=True)    # 读取为掩膜数组，nodata 自动 masked
        profile = ds.profile              # 保留元数据，便于对齐与写出

    return data, profile

"""小步目标：封装道路/电力线距离栅格的加载函数，统一默认路径与掩膜处理。
输入：默认读取 data/interim/dist_roads.tif 与 data/interim/dist_grid.tif，可选自定义路径。
输出：返回掩膜数组（numpy.ma.MaskedArray）与 rasterio profile 元数据。"""

from pathlib import Path

import rasterio

from src.config import INTERIM_DIR

DIST_ROADS = INTERIM_DIR / "dist_roads.tif"
DIST_GRID = INTERIM_DIR / "dist_grid.tif"


def load_dist_roads(path: str | Path | None = None):
    """加载道路距离栅格，返回掩膜数组与 profile。"""
    dist_path = Path(path) if path else DIST_ROADS  # 传入路径优先，否则用默认
    if not dist_path.exists():
        raise FileNotFoundError(f"道路距离文件不存在：{dist_path}")

    with rasterio.open(dist_path) as ds:  # 打开道路距离栅格
        data = ds.read(1, masked=True)    # 读取为掩膜数组，nodata 自动 masked
        profile = ds.profile              # 保留元数据，便于对齐与写出

    return data, profile


def load_dist_grid(path: str | Path | None = None):
    """加载电力线距离栅格，返回掩膜数组与 profile。"""
    dist_path = Path(path) if path else DIST_GRID  # 传入路径优先，否则用默认
    if not dist_path.exists():
        raise FileNotFoundError(f"电力线距离文件不存在：{dist_path}")

    with rasterio.open(dist_path) as ds:  # 打开电力线距离栅格
        data = ds.read(1, masked=True)    # 读取为掩膜数组，nodata 自动 masked
        profile = ds.profile              # 保留元数据，便于对齐与写出

    return data, profile

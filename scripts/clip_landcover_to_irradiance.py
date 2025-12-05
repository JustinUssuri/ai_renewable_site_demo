"""小步目标：将 CLC2018 土地利用重投影并对齐到辐照度 4.4km 网格（最近邻）。
输入：源栅格 data/raw/U2018_CLC2018_V2020_20u1.tif，目标模板 data/interim/irradiance_reproj.tif。
输出：对齐后的土地利用栅格 data/interim/landcover_resampled_to_irradiance.tif。"""

from pathlib import Path

import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling

SRC = Path("data/raw/U2018_CLC2018_V2020_20u1.tif")
TEMPLATE = Path("data/interim/irradiance_reproj.tif")
OUT = Path("data/interim/landcover_resampled_to_irradiance.tif")


def main():
    with rasterio.open(TEMPLATE) as tgt:  # 打开目标栅格，获取形状/变换/CRS
        tgt_meta = tgt.profile
        tgt_shape = tgt.shape
        tgt_transform = tgt.transform
        tgt_crs = tgt.crs
        tgt_mask = tgt.read(1, masked=True).mask  # 用辐照度掩膜对齐

    with rasterio.open(SRC) as src:
        src_data = src.read(1)
        src_meta = src.meta.copy()

    dest = np.full(tgt_shape, src_meta.get("nodata", 0), dtype=src_data.dtype)
    reproject(  # 最近邻重投影+重采样
        source=src_data,
        destination=dest,
        src_transform=src.transform,
        src_crs=src.crs,
        dst_transform=tgt_transform,
        dst_crs=tgt_crs,
        resampling=Resampling.nearest,
    )
    dest = np.ma.array(dest, mask=tgt_mask)  # 套用辐照度掩膜

    tgt_meta.update(dtype=src_meta["dtype"], nodata=src_meta.get("nodata"), compress="lzw")
    with rasterio.open(OUT, "w", **tgt_meta) as dst:
        dst.write(dest.filled(src_meta.get("nodata", 0)), 1)  # 写出对齐的土地利用


if __name__ == "__main__":
    main()

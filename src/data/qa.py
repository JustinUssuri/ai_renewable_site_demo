"""Raster QA helpers."""

from pathlib import Path

import numpy as np
import rasterio


def print_raster_summary(path: Path) -> None:
    """Print CRS/resolution/bounds/dtype and basic stats for a single-band raster."""

    with rasterio.open(path) as ds:
        data = ds.read(1, masked=True)  # 读取单波段并保留 nodata 掩膜
        res_x, res_y = ds.res  # 像元大小
        print(f"File: {path}")
        print(f"CRS: {ds.crs}")
        print(f"Resolution: {res_x:.2f} x {res_y:.2f} m")
        print(f"Bounds: {ds.bounds}")
        print(f"Dtype: {ds.dtypes[0]}")
        if np.ma.is_masked(data):
            data = np.ma.compressed(data)  # 去掉 nodata 的值
        print(
            "Stats (min/mean/max):",
            float(data.min()),
            float(data.mean()),
            float(data.max()),
        )

"""裁剪辐照度栅格到爱尔兰边界（保持 WGS84）。"""

from pathlib import Path
import sys

import rasterio
from rasterio.features import geometry_mask
from rasterio.windows import from_bounds

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # 确保可以导入 src 模块

from src.data.preprocess import load_region_boundary


SRC = Path("data/raw/gh_0_year_sarah2.tif")
DST = Path("data/interim/irradiance_clipped.tif")


if __name__ == "__main__":
    boundary = load_region_boundary(target_crs="EPSG:4326")  # 边界转到 WGS84
    with rasterio.open(SRC) as src:
        bbox = boundary.total_bounds  # lon_min, lat_min, lon_max, lat_max
        window = from_bounds(*bbox, transform=src.transform)  # 计算裁剪窗口
        data = src.read(1, window=window, masked=False)  # 读取窗口内数据，忽略原掩膜
        out_transform = src.window_transform(window)  # 更新裁剪后的仿射变换
        mask_geom = boundary.geometry.values  # 获取多边形
        geom_mask = geometry_mask(mask_geom, transform=out_transform, invert=True, out_shape=data.shape)  # True 表示在区域内
        data[~geom_mask] = src.nodata or -9999  # 区域外写入 nodata
        profile = src.profile.copy()
        profile.update(
            height=data.shape[0],
            width=data.shape[1],
            transform=out_transform,
        )
    DST.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(DST, "w", **profile) as dst:
        dst.write(data, 1)  # 写出裁剪后的栅格
    print(f"Saved clipped irradiance to: {DST}")

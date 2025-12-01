"""Reproject irradiance raster to target CRS (EPSG:2157)."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # 允许导入 src 模块

from src.data.preprocess import reproject_raster


# 使用已裁剪的 WGS84 辐照度子集作为输入
SRC = Path("data/interim/irradiance_clipped.tif")
DST = Path("data/interim/irradiance_reproj.tif")


if __name__ == "__main__":
    if not SRC.exists():
        raise SystemExit(f"Irradiance source not found: {SRC}")
    reproject_raster(SRC, DST)  # 重投影到目标 CRS（默认 EPSG:2157）
    print(f"Saved reprojected irradiance to: {DST}")

"""QA for irradiance raster (SARAH annual GHI)."""

from pathlib import Path
import sys

import numpy as np
import rasterio

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # 确保可以导入 src 模块

from src.data.qa import print_raster_summary


IRR_PATH = Path("data/raw/gh_0_year_sarah2.tif")


if __name__ == "__main__":
    if not IRR_PATH.exists():
        raise SystemExit(f"Irradiance file not found: {IRR_PATH}")
    print_raster_summary(IRR_PATH)

    # 读取原始值，查看 nodata 并手动过滤
    with rasterio.open(IRR_PATH) as ds:
        raw = ds.read(1)  # 不使用 mask，直接读取原始栅格
        nodata = ds.nodata
    print(f"Nodata value: {nodata}")
    print(
        "Raw stats (incl nodata):",
        float(np.nanmin(raw)),
        float(np.nanmean(raw)),
        float(np.nanmax(raw)),
    )
    if nodata is not None:
        mask = raw != nodata  # 过滤 nodata
        print(
            "Valid stats (exclude nodata):",
            float(np.nanmin(raw[mask])),
            float(np.nanmean(raw[mask])),
            float(np.nanmax(raw[mask])),
        )

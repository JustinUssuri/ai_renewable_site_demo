"""小步目标：从 OSM PBF/道路 Shapefile 生成道路与电力线距离栅格（对齐辐照度网格）。
输入：data/raw/osm_ireland.osm.pbf、data/raw/osm_ireland_shp/gis_osm_roads_free_1.shp、data/interim/irradiance_reproj.tif。
输出：data/raw/power_lines.gpkg、data/interim/dist_roads.tif、data/interim/dist_grid.tif（单位米）。"""

from pathlib import Path

import geopandas as gpd  # 读取矢量并重投影
import numpy as np
import rasterio
import subprocess
from rasterio.features import rasterize
from scipy.ndimage import distance_transform_edt

base = Path("data/interim/irradiance_reproj.tif")
pbf = Path("data/raw/osm_ireland.osm.pbf")
gpkg = Path("data/raw/power_lines.gpkg")
roads = Path("data/raw/osm_ireland_shp/gis_osm_roads_free_1.shp")
dist_targets = [
    (roads, None, Path("data/interim/dist_roads.tif")),  # 道路线 → 距离栅格
    (gpkg, "power_lines", Path("data/interim/dist_grid.tif")),  # 电力线 → 距离栅格
]

if not gpkg.exists():  # 若尚未提取电力线，则用 ogr2ogr 从 PBF 过滤 power=*
    sql = (
        "SELECT * FROM lines WHERE "
        "other_tags LIKE '%\"power\"=>\"line\"%' OR "
        "other_tags LIKE '%\"power\"=>\"minor_line\"%' OR "
        "other_tags LIKE '%\"power\"=>\"cable\"%'"
    )
    cmd = [
        "ogr2ogr",
        "-f",
        "GPKG",
        "-overwrite",
        "-nln",
        "power_lines",
        str(gpkg),
        str(pbf),
        "-dialect",
        "SQLite",
        "-sql",
        sql,
    ]
    subprocess.run(cmd, check=True)  # 调用 GDAL 生成电力线 GPKG

with rasterio.open(base) as src:  # 打开基准栅格获取形状与变换
    profile = src.profile
    base_mask = src.read(1, masked=True).mask
    transform = src.transform
    shape = src.shape

for vec, layer, out in dist_targets:  # 逐个矢量生成对应距离栅格
    gdf = gpd.read_file(vec, layer=layer) if layer else gpd.read_file(vec)
    gdf = gdf.to_crs(profile["crs"])  # 重投影到栅格 CRS
    shapes = [(geom, 1) for geom in gdf.geometry if not geom.is_empty]
    ras = rasterize(shapes, out_shape=shape, transform=transform, fill=0, dtype="uint8")
    dist = distance_transform_edt(
        ras == 0, sampling=(abs(transform.e), abs(transform.a))
    ).astype("float32")  # 欧氏距离，采样间距用像元分辨率
    dist[base_mask] = np.nan  # 掩膜区域设为 NaN
    profile.update(dtype="float32", nodata=np.nan, compress="lzw")
    with rasterio.open(out, "w", **profile) as dst:
        dst.write(dist, 1)  # 写出距离栅格

"""Tiny step: build road and powerline distance rasters aligned to irradiance grid.
Input: data/raw/osm_ireland.osm.pbf, data/raw/osm_ireland_shp/gis_osm_roads_free_1.shp, data/interim/irradiance_reproj.tif.
Output: data/raw/power_lines.gpkg, data/interim/dist_roads.tif, data/interim/dist_grid.tif (meters)."""

from pathlib import Path

import geopandas as gpd  # read vectors and reproject
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
    (roads, None, Path("data/interim/dist_roads.tif")),  # roads → distance raster
    (gpkg, "power_lines", Path("data/interim/dist_grid.tif")),  # power lines → distance raster
]

if not gpkg.exists():  # if power lines not extracted yet, filter from PBF via ogr2ogr
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
    subprocess.run(cmd, check=True)  # GDAL extracts power lines to GPKG

with rasterio.open(base) as src:  # open reference raster for shape/transform
    profile = src.profile
    base_mask = src.read(1, masked=True).mask
    transform = src.transform
    shape = src.shape

for vec, layer, out in dist_targets:  # generate distance raster per vector source
    gdf = gpd.read_file(vec, layer=layer) if layer else gpd.read_file(vec)
    gdf = gdf.to_crs(profile["crs"])  # reproject to raster CRS
    shapes = [(geom, 1) for geom in gdf.geometry if not geom.is_empty]
    ras = rasterize(shapes, out_shape=shape, transform=transform, fill=0, dtype="uint8")
    dist = distance_transform_edt(
        ras == 0, sampling=(abs(transform.e), abs(transform.a))
    ).astype("float32")  # Euclidean distance; sampling uses pixel size
    dist[base_mask] = np.nan  # apply reference mask
    profile.update(dtype="float32", nodata=np.nan, compress="lzw")
    with rasterio.open(out, "w", **profile) as dst:
        dst.write(dist, 1)  # write distance raster

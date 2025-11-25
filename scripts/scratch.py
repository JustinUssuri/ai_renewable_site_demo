from pathlib import Path
import geopandas as gpd

print(">>> scratch.py started")

path = Path("data/raw/ireland_counties_2019.geojson")
print("file exists?", path.exists(), "->", path)

gdf = gpd.read_file(path)
print("rows:", len(gdf))
print("columns:", list(gdf.columns))
print("crs:", gdf.crs)

print("head:")
print(gdf.head())

print(">>> scratch.py finished")

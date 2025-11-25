from pathlib import Path

import geopandas as gpd

from src.config import RAW_DIR, TARGET_CRS


def main() -> None:
    counties_path = RAW_DIR / "ireland_counties_2019.geojson"
    out_path = RAW_DIR / "region_boundary.geojson"

    print(">>> make_region_boundary.py started")
    print("counties_path:", counties_path)

    if not counties_path.exists():
        raise FileNotFoundError(f"Counties file not found: {counties_path}")

    gdf = gpd.read_file(counties_path)
    print("rows:", len(gdf), "columns:", list(gdf.columns))
    print("source CRS:", gdf.crs)

    # 投影到统一 CRS（方便后面做距离）
    gdf = gdf.to_crs(TARGET_CRS)

    # dissolve：把所有 county 融成一个多边形
    # 如果有 county 名字段，比如 "COUNTY" / "COUNTY_NA" 等，不用分组，直接 dissolve()
    country = gdf.dissolve()  # 所有行合并成 1 行
    country = country.reset_index(drop=True)

    print("after dissolve, rows:", len(country))
    print(country.head())

    out_path.parent.mkdir(parents=True, exist_ok=True)
    country.to_file(out_path, driver="GeoJSON")
    print("saved region boundary to:", out_path)

    print(">>> make_region_boundary.py finished")


if __name__ == "__main__":
    main()

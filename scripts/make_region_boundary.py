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

    # Reproject to target CRS (for distance calculations later)
    gdf = gdf.to_crs(TARGET_CRS)

    # dissolve all counties into a single polygon
    country = gdf.dissolve()  # combine all rows into one
    country = country.reset_index(drop=True)

    print("after dissolve, rows:", len(country))
    print(country.head())

    out_path.parent.mkdir(parents=True, exist_ok=True)
    country.to_file(out_path, driver="GeoJSON")
    print("saved region boundary to:", out_path)

    print(">>> make_region_boundary.py finished")


if __name__ == "__main__":
    main()

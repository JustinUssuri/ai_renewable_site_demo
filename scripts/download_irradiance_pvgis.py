"""Download Ireland irradiance raster (PVGIS SARAH) as GeoTIFF."""

from pathlib import Path
import requests


OUT_PATH = Path("data/raw/irradiance_ireland.tif")
BASE_URL = "https://re.jrc.ec.europa.eu/api/v5_2/seriescalc"
PARAMS = {
    "bbox": "-11,51.4,-5.3,55.5",  # Ireland bounding box lon_min,lat_min,lon_max,lat_max
    "outputformat": "geotiff",
    "raddatabase": "PVGIS-SARAH",
}


def main() -> None:
    # Call PVGIS API to get irradiance GeoTIFF
    resp = requests.get(BASE_URL, params=PARAMS, timeout=60)
    resp.raise_for_status()  # raise if request failed

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_bytes(resp.content)  # write GeoTIFF bytes
    print(f"Saved irradiance raster to: {OUT_PATH}")


if __name__ == "__main__":
    main()

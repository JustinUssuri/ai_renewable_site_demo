"""Download Ireland irradiance raster (PVGIS SARAH) as GeoTIFF."""

from pathlib import Path
import requests


OUT_PATH = Path("data/raw/irradiance_ireland.tif")
BASE_URL = "https://re.jrc.ec.europa.eu/api/v5_2/seriescalc"
PARAMS = {
    "bbox": "-11,51.4,-5.3,55.5",  # 爱尔兰外包框 lon_min,lat_min,lon_max,lat_max
    "outputformat": "geotiff",
    "raddatabase": "PVGIS-SARAH",
}


def main() -> None:
    # 调用 PVGIS API 获取辐照度 GeoTIFF
    resp = requests.get(BASE_URL, params=PARAMS, timeout=60)
    resp.raise_for_status()  # 如果请求失败则抛出异常

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_bytes(resp.content)  # 直接写入 GeoTIFF
    print(f"Saved irradiance raster to: {OUT_PATH}")


if __name__ == "__main__":
    main()

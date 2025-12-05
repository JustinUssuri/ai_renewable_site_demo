"""Quickly visualize irradiance and resampled DEM (with boundary overlay)."""

# Goal: draw two plots comparing irradiance and aligned DEM; inputs: irradiance_reproj,
# dem_resampled_to_irradiance, region_boundary; output: on-screen plots (can be saved).

from pathlib import Path
import sys

import numpy as np
import matplotlib.pyplot as plt
import rasterio

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # import src modules

IRR = Path("data/interim/irradiance_reproj.tif")
DEM = Path("data/interim/dem_resampled_to_irradiance.tif")
BOUNDARY = Path("data/raw/region_boundary.geojson")


if __name__ == "__main__":
    from src.data.preprocess import load_region_boundary

    boundary = load_region_boundary(BOUNDARY, target_crs="EPSG:2157")  # use helper to load/transform boundary
    with rasterio.open(IRR) as irr, rasterio.open(DEM) as dem:
        irr_data = np.ma.masked_equal(irr.read(1), irr.nodata)  # mask nodata
        dem_data = np.ma.masked_equal(dem.read(1), dem.nodata)
        irr_vmin, irr_vmax = np.nanpercentile(irr_data.compressed(), (2, 98))  # stretch colors 2–98 percentile
        dem_vmin, dem_vmax = np.nanpercentile(dem_data.compressed(), (2, 98))
        fig, axes = plt.subplots(1, 2, figsize=(10, 5))
        for ax, data, vmin, vmax, title in (
            (axes[0], irr_data, irr_vmin, irr_vmax, "Irradiance (kWh/m²)"),
            (axes[1], dem_data, dem_vmin, dem_vmax, "DEM resampled (m)"),
        ):
            im = ax.imshow(
                data,
                extent=[irr.bounds.left, irr.bounds.right, irr.bounds.bottom, irr.bounds.top],
                vmin=vmin,
                vmax=vmax,
                cmap="inferno",
            )
            boundary.boundary.plot(ax=ax, color="red", linewidth=0.5)  # overlay boundary
            ax.set_title(title)
            fig.colorbar(im, ax=ax, shrink=0.8)
    plt.tight_layout()
    plt.show()

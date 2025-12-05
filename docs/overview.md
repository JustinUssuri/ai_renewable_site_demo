# AI + Renewable Siting Demo · Overview

> Goal: build a minimal AI + PV siting demo (start with Ireland) that:
> - runs locally with one command,
> - shows clear map visualizations,
> - showcases GIS + weather + energy investment thinking.

## 1. Concept
Create a PV siting scoring system for investors/developers:
- Raster-based scoring over the study area (e.g., Ireland national or counties).
- Outputs:
  - Score heatmap raster.
  - Top N candidate sites (points or small areas) with metrics and score.
  - Interactive web page to tweak weights/thresholds and refresh the map.
Scope: early-stage screening + explainability, not full financial modeling.

## 2. MVP scope and assumptions
### Factors (v0)
- **Resource (R)**: annual solar irradiance / PV potential (e.g., PVGIS).
- **Terrain (T)**: slope (flatter is better), optional aspect preference.
- **Grid access (G)**: distance to transmission lines/substations (OSM or simplified grid).
- **Land use (L)**: farmland/grassland preferred; water/protected/urban are excluded or low score.

### Not included (later versions)
- Tariffs, subsidies, capacity limits, queueing for interconnection.
- Full cashflow/NPV/IRR models.
- Complex wind-solar synergy or power system constraints.

### Outputs
1) Score raster: 0–100 composite per cell.  
2) Top N candidates: lat/lon, score, R/G/T/L metrics, constraints info.  
3) Interactive demo (Streamlit): weights/threshold sliders + map (heatmap + Top N).

## 3. Stack and data
### Stack
- Python 3.11; conda (`environment.yml`).
- Geo: `geopandas`, `shapely` (vector); `rasterio`, `rioxarray`, `rasterstats` (raster).
- Numerics/viz: `numpy`, `pandas`, `matplotlib`, `folium`.
- Web: `streamlit`.

### Typical data (Ireland)
- Solar/PV potential: PVGIS (EC JRC).
- DEM: Copernicus DEM / EU-DEM (≈30m).
- Land cover: CORINE CLC 2018 or national datasets.
- Grid/roads: OpenStreetMap (`power=line/substation`, main roads).

Raw data under `data/raw/`; processed outputs in `data/interim/` and `data/processed/`.

## 4. Project structure
```text
ai_renewable_site_demo/
├── README.md
├── environment.yml
├── data/
│   ├── raw/           # raw downloads (append-only)
│   ├── interim/       # reprojection / clip / resample intermediates
│   └── processed/     # final features & scores (score, top_sites)
├── notebooks/
│   ├── 01_explore_data.ipynb        # DEM + irradiance exploration
│   ├── 02_feature_engineering.ipynb # feature distributions & thresholds
│   └── 03_scoring_and_maps.ipynb    # scoring + map visualization
├── src/
│   ├── config.py            # paths, CRS, defaults
│   ├── data/preprocess.py   # boundary ingest, reprojection, clipping
│   ├── features/            # feature loaders/builders
│   └── viz/                 # map helpers
├── app/app.py               # Streamlit entrypoint
└── scripts/                 # data/feature processing scripts
```

# Spatial PV Siting Workflow (Ireland)
Early-stage, grid-aligned feature engineering for PV siting and energy-system modelling.

## Overview
This workflow assembles renewable siting inputs for Ireland so system-level models can reference consistent, geospatially aligned rasters instead of ad hoc layers. It targets early-phase screening for PV by preparing terrain and accessibility features on a single grid that downstream optimisation or dispatch models can query.

A unified grid (baseline: PVGIS SARAH GHI resampled/reprojected to EPSG:2157) keeps slope, irradiance, and proximity metrics comparable and ready for aggregation to coarser model nodes. Distances to infrastructure and terrain suitability become structured inputs that can feed frameworks such as ETHOS or other power-system planning tools.

The repository is a work-in-progress research prototype: scripts are intentionally simple, data must be sourced separately, and outputs are primarily for experimentation rather than production siting decisions.

## Data & Inputs
- **Digital Elevation Model (DEM):** Copernicus/EU-DEM (~30 m) clipped to Ireland.
- **Solar resource:** PVGIS SARAH global horizontal irradiance (annual), baseline ~4.4 km grid.
- **Infrastructure & access:** OpenStreetMap roads and power lines (transmission/substations extracted from PBF).
- **Boundary:** National boundary polygon (Ireland) used for clipping/masking.

## Pipeline at a Glance
- Ingest national boundary and set target CRS/resolution mask.
- Reproject and clip PVGIS irradiance; reproject DEM to the same grid; derive slope.
- Extract OSM roads and power lines, rasterize to the reference grid, and compute Euclidean distance rasters.
- (Optional) Align land-cover rasters for later constraint layers.
- Run quick QA/summary scripts or notebooks to inspect coverage and statistics.

## Repository structure
- `src/`: configuration, preprocessing helpers, and feature loaders (`features/irradiance.py`, `features/dem.py`, `features/slope.py`, `features/distance.py`).
- `scripts/`: stepwise processing (boundary creation, reprojection/resampling, slope derivation, OSM distance rasters, QA checks).
- `notebooks/`: exploratory analyses of irradiance/DEM alignment, feature distributions, and preliminary scoring ideas.
- `docs/`: architecture notes, work plan, and prompts.
- `app/`: early Streamlit stub for interactive map/weight tuning.
- `data/`: `raw/` (user-supplied), `interim/` (aligned rasters), `processed/` (future scoring outputs); not versioned.

## How to reproduce (minimal)
- Create a Python 3.11 environment (e.g., `conda` with `environment.yml`) and activate it.
- Place source data under `data/raw/`: PVGIS SARAH GHI raster, DEM tiles, OSM PBF for Ireland, and a boundary polygon.
- Run the preprocessing scripts in `scripts/` to align to the reference grid: boundary → irradiance reprojection → DEM reprojection/resampling → slope derivation → OSM extraction and distance rasters; use the QA scripts/notebooks to verify statistics and visual checks.
- Open the notebooks in `notebooks/` or launch the Streamlit app to inspect intermediate layers once rasters are generated.

## Status & future work
- Implemented: baseline grid built from PVGIS SARAH (~4.4 km) in EPSG:2157, DEM resampled to match, slope derived, and OSM-based distance-to-road and distance-to-grid rasters produced (see `data/interim/` outputs); exploratory notebooks and QA scripts for coverage checks.
- Next steps: add land-cover exclusions/preferences, compute a transparent siting score across features, move to finer-resolution irradiance where available, and couple outputs to system-level models (e.g., ETHOS or other capacity-expansion workflows).

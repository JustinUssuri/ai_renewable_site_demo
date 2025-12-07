# AI + Renewable Siting Demo (Ireland) · Work Plan

> Goal: deliver a PV siting demo in ~4 weeks, each phase runnable with visuals.

## 0. Timeline
- Phase 0: Environment & skeleton (~1 day)
- Phase 1: Boundary + base rasters (DEM & irradiance) (~1 week)
- Phase 2: Feature engineering (slope / distance / landcover) (~1 week)
- Phase 3: Scoring & TopN (~3–4 days)
- Phase 4: Web demo & docs (~3–4 days)

## Snapshot (done)
- ✅ Conda env `ai_renewable` usable; geopandas/rasterio/streamlit import OK.
- ✅ Boundary: `data/raw/region_boundary.geojson`; `load_region_boundary()` ready.
- ✅ DEM: reproject + clip → `data/interim/dem_clipped.tif`.
- ✅ Irradiance: clip + reproject → `data/interim/irradiance_reproj.tif`; DEM resampled to 4.4 km → `dem_resampled_to_irradiance.tif`.
- ✅ Slope: `scripts/compute_slope_resampled.py` produces `data/interim/slope_resampled_to_irradiance.tif` (valid 3,588; mean ≈4.3°).
- ✅ Notebook refactor: `notebooks/01_explore_data.ipynb` aligned imports/paths; includes DEM/irradiance/slope QA and visuals.
- ✅ Reviewer polish: top-level `README.md` rewritten with scope, caveats, current functionality, next steps, and embedded example map.
- ✅ Figures exported: `figures/score_placeholder.png` and `figures/suitable_mask.png` generated from the scoring notebook for documentation.

## Phase 0: Environment & skeleton (done)
**Done when**: one command activates env and imports key libs; structure matches overview.

## Phase 1: Boundary + base rasters (done)
**Done when**: `01_explore_data.ipynb` runs fully; outputs DEM+boundary and irradiance+boundary plots with summary text.

## Phase 2: Feature engineering (in progress)
**Goal**: compute features on 4.4 km grid and inspect distributions.

### Task 0: Load helpers
- [x] Wrap irradiance/slope/DEM: `load_irradiance` / `load_slope` / `load_dem`.
- [x] Wrap landcover: `load_landcover` (defaults to resampled grid).
- [x] Wrap distance rasters: `load_dist_roads` / `load_dist_grid`.

### Task 1: Slope
- [x] Generate slope raster (4.4 km, aligned to irradiance): `slope_resampled_to_irradiance.tif`.
- [x] Provide loader for reuse.

### Task 2: Landcover
- [x] Download CLC2018 100m → `data/raw/U2018_CLC2018_V2020_20u1.tif`.
- [x] Reproject/resample to irradiance grid → `landcover_resampled_to_irradiance.tif`; histogram `landcover_class_hist.png`.

### Task 3: Road & grid distance (deferred high-res recompute)
- [x] Collect vectors: Geofabrik roads; OSM PBF filtered power lines → `data/raw/power_lines.gpkg`.
- [x] Placeholder distance rasters → `dist_grid.tif`, `dist_roads.tif` (computed directly at 4.4 km; zero-heavy; high-res recompute deferred to next phase).

### Task 4: Feature QA notebook
- [x] `02_feature_engineering.ipynb` shows slope/distance/landcover distributions; includes sys.path fix. Distance plots are skewed due to coarse placeholder; update after recompute.

**Phase 2 Done when**: files exist under `data/interim/` (`slope_resampled_to_irradiance.tif`, `dist_grid.tif`, `dist_roads.tif`, `landcover_clipped.*`); `02_feature_engineering.ipynb` shows distributions with noted thresholds/limitations.

## Phase 3: Scoring & TopN (started)
- Define masks (slope threshold, landcover whitelist; distance optional later), normalize features, compute `score.tif`.
- Extract TopN (`top_sites.geojson/csv`) with coordinates and feature values.
- Notebook `03_scoring_and_maps.ipynb`: heatmap + TopN visualization, metric breakdown.
- Placeholder scoring plan drafted (`docs/scoring_placeholder.md`): irradiance min-max, slope mask at 8°, landcover whitelist {211, 231, 242, 243, 311, 312}, distance weight = 0 until recompute; target output `data/processed/score_placeholder.tif` with notebook skeleton steps.
- Placeholder score generated with NaN masking and current weights → `data/processed/score_placeholder.tif` (min ≈0.076, max ≈0.741, mean ≈0.424); notebook `03_scoring_and_maps.ipynb` created with stepwise cells and later polished.
- Notebook refreshed for reviewers: English narrative up front, per-block explanations, QA tables (min/max/percentiles), consistent histograms, spatial score map with region boundary overlay, binary suitable mask (threshold 0.55), figure exports, and interpretation notes; `SCORING_PARAMS` dict centralizes tunable thresholds/weights.

## Phase 4: Web demo & docs (not started)
- Streamlit map, TopN points, metric breakdown.
- Docs: data sources, processing flow, run guide.

## Next priorities
1) Calibrate land-cover classes/weights and slope thresholds with domain input; revisit distance layers once recomputed at finer resolution and reflect in `SCORING_PARAMS`.
2) Add a lightweight TopN/summary export (geojson/csv) from the composite score to prep for Phase 4 map/app integration.
3) Extend docs with a short “scenario tuning” note showing how to adjust parameters and re-export figures/rasters; keep README/example maps refreshed after changes.

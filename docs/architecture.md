# Architecture Overview

Docs are small, so concept and implementation live together here; we can split later if Web/App diverges.

## Concept (business flow)
```mermaid
flowchart LR
    A[Raw data\nDEM / irradiance / landcover / OSM grid] --> B[Unified boundary\nregion_boundary.geojson]
    B --> C[Raster prep\nreproject + clip]
    C --> D[Feature engineering\nslope / distance / landcover rasters]
    D --> E[Scoring\nnormalization + weights]
    E --> F[Outputs\nscore.tif + TopN]
    F --> G[Visualization & Demo\nNotebook + Streamlit]
```

## Implementation (code & files)
```mermaid
flowchart TB
    subgraph Data Prep
        S1[scripts/make_region_boundary.py]
        P1[src/data/preprocess.py]
        S2[scripts/inspect_dem_info.py]
    end
    subgraph Features
        F1[src/features/build_features.py]
    end
    subgraph Scoring
        F2[src/features/compute_scores.py]
    end
    subgraph Outputs
        N1[notebooks/01_02_03_*.ipynb]
        V1[src/viz/make_maps.py]
        A1[app/app.py]
    end

    raw[(data/raw/*)] --> S1 --> P1
    raw --> S2 --> P1
    P1 --> F1 --> F2 --> processed[(data/processed/*)]
    processed --> V1 --> A1
    processed --> N1
```

**Notes**:
- `scripts/*` handle one-off prep (e.g., dissolve boundary, inspect DEM).
- `src/data/preprocess.py` offers reusable helpers (load boundary, reproject, clip) for notebooks/pipelines.
- `src/features/*` consume preprocessed rasters to produce features and scores.
- `notebooks`, `src/viz`, `app/app.py` visualize and interact with scoring outputs.

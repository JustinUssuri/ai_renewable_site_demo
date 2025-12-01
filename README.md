# AI + Renewable Siting Demo

AI-assisted **solar site suitability mapping** for Ireland using open GIS and climate data.

Status: 🚧 Working in progress (Week 1 - Phase 1)。当前以辐照度 4.4km 网格为基准：
- 辐照度（PVGIS SARAH）重投影至 EPSG:2157，像元 ~4.4 km → `data/interim/irradiance_reproj.tif`
- DEM 原始 23m，仅用于高精度参考；对齐使用 `data/interim/dem_resampled_to_irradiance.tif`
- 如需精细站址需获取更高分的辐照度源，不建议上采样现有栅格。

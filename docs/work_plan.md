# AI + 新能源选址 Demo · Work Plan

> 目标：**4 周内完成一个光伏选址 Demo（爱尔兰）**，每个阶段都能跑通并有可视结果。

---

## 0. 总体节奏
- Phase 0：环境 & 骨架（~1 天）
- Phase 1：区域边界 + 基础栅格（DEM & 辐照度）（~1 周）
- Phase 2：特征工程（坡度 / 距离 / 土地利用）（~1 周）
- Phase 3：评分 & TopN（~3–4 天）
- Phase 4：Web Demo & 文档包装（~3–4 天）

---

## 进度快照（已完成）
- ✅ Conda 环境 `ai_renewable` 可用，核心依赖 geopandas/rasterio/streamlit 可导入。
- ✅ 区域边界：`data/raw/region_boundary.geojson`（dissolve，全国边界），`load_region_boundary()` 就绪。
- ✅ DEM：重投影 + 裁剪完成，`data/interim/dem_clipped.tif`。
- ✅ 辐照度：裁剪+重投影完成，`data/interim/irradiance_reproj.tif`；DEM 已重采样到 4.4km，`dem_resampled_to_irradiance.tif`。
- ✅ 坡度：`scripts/compute_slope_resampled.py` 先算高分坡度再聚合到 4.4km，并与辐照度掩膜对齐，输出 `data/interim/slope_resampled_to_irradiance.tif`（有效 3,588，mean≈4.3°）。
- ✅ Notebook 重构：`notebooks/01_explore_data.ipynb` 统一导入/路径，含 DEM/辐照度对比、坡度 QA 与可视化、文字小结。

---

## Phase 0：环境 & 骨架（完成）
**Done 标准**：一条命令激活环境并成功 import 关键库；目录结构与 overview 一致。
- [x] Git 仓库与目录结构搭建（data/raw, data/interim, data/processed, notebooks, src, app, scripts, docs）。
- [x] `README.md`、`environment.yml` 创建；`conda env create -f environment.yml` 成功。

---

## Phase 1：区域边界 + 基础栅格（完成）
**目标**：在 notebook 中可视化区域边界 + DEM + 辐照度，并有基础统计。
- [x] 区域边界：生成 `region_boundary.geojson`，`load_region_boundary()` 可用。
- [x] DEM：重投影+裁剪 → `dem_clipped.tif`。
- [x] 辐照度：裁剪+重投影 → `irradiance_reproj.tif`；DEM 对齐辐照度网格 → `dem_resampled_to_irradiance.tif`。
- [x] 探索 notebook：`01_explore_data.ipynb` 跑通，含边界/DEM/辐照度/坡度的统计与可视化，导出预览图。
**Done 标准**：`01_explore_data.ipynb` 全部单元可运行；至少输出 DEM+边界、辐照度+边界的图，附文字小结。

---

## Phase 2：特征工程（进行中）
**目标**：为每个 4.4km 栅格计算特征，并检查分布。

### 任务 1：坡度
- [x] 生成坡度栅格（4.4km，对齐辐照度）：`data/interim/slope_resampled_to_irradiance.tif`（脚本：`scripts/compute_slope_resampled.py`）。
- [ ] 在 `src/features/` 中封装加载/复用坡度的接口（便于评分与后续特征计算）。

### 任务 2：土地利用
- [ ] 下载土地利用数据（如 CLC2018 / 国家土地覆盖）→ `data/raw/landcover.*`
- [ ] 重投影并裁剪到研究区 → `landcover_clipped.*`

### 任务 3：电网与道路距离
- [ ] 收集电网/道路矢量数据 → `data/raw/power_lines.*`, `data/raw/roads.*`
- [ ] 计算距离栅格并与辐照度网格对齐 → `dist_grid.tif`, `dist_roads.tif`

### 任务 4：特征检查 notebook
- [ ] 在 `notebooks/02_feature_engineering.ipynb` 展示坡度/距离/土地利用/辐照度分布，做直方图与候选阈值备注。

**Done 标准**：`data/interim/` 下存在 `slope_resampled_to_irradiance.tif`、`dist_grid.tif`、`dist_roads.tif`、`landcover_clipped.*`；`02_feature_engineering.ipynb` 展示分布并记录阈值。

---

## Phase 3：评分 & TopN（未开始）
**目标**：输出综合评分栅格与 TopN 候选点。

### 任务
- [ ] 标准化特征并构建可用性掩膜（坡度阈值、土地利用过滤、距离上限等）。
- [ ] 综合评分公式：`Score = 100 * (w_R*R_norm + w_G*G_norm + w_T*T_norm + w_L*L_norm)`；`Score_final = Score * mask_available`，写出 `data/processed/score.tif`。
- [ ] TopN：从评分栅格提取可用像元，按分数排序取 N，输出 `top_sites.geojson` / `top_sites.csv`（含经纬度与特征值）。
- [ ] Notebook `03_scoring_and_maps.ipynb`：热力图 + TopN 点可视化，典型点指标构成。

**Done 标准**：`score.tif` 数值在 [0,100]；TopN 文件存在且包含指标字段。

---

## Phase 4：Web Demo & 文档（未开始）
- [ ] Streamlit Web Demo 展示地图、TopN 点、指标拆解。
- [ ] 补充 README/docs，描述数据源、处理流程、运行指南。

---

## 下一步优先级
1) 跑通 `01_explore_data.ipynb`（含坡度单元），确认 PNG 预览输出 OK。  
2) 在 `src/features/` 中加上坡度加载入口，准备 Phase 2 评分。  
3) 规划土地利用与电网/道路数据源，确定下载/预处理脚本清单。  
4) 文档补充分辨率/掩膜约束（以辐照度 4.4km 为基准）。 

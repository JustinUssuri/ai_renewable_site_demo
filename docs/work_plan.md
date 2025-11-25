# AI + 新能源选址 Demo · Work Plan（work_plan）

> 本文件描述从 0 到一个可运行 Demo 的分阶段工作计划。  
> 默认目标：**4 周内完成一个光伏选址 Demo（以爱尔兰为例）**。

---

## 0. 总体节奏

- **Phase 0**：环境 & 骨架（~1 天）
- **Phase 1**：区域边界 + 基础栅格（DEM & 辐照度）（~1 周）
- **Phase 2**：特征工程（坡度 / 距离 / 土地利用）（~1 周）
- **Phase 3**：评分 & TopN（~3–4 天）
- **Phase 4**：Web Demo & 文档包装（~3–4 天）

每个阶段结束时，仓库都要保持「能跑通、能看见东西」。

---

## Phase 0：环境 & 项目骨架

**目标**：有一个能 import 所有依赖的 conda 环境，以及清晰的项目目录。

### 任务清单

- [ ] 新建 Git 仓库 `ai_renewable_site_demo`，clone 到本地
- [ ] 创建基础目录结构：
  - [ ] `data/raw`, `data/interim`, `data/processed`
  - [ ] `notebooks`, `src/data`, `src/features`, `src/viz`, `app`, `scripts`, `docs`
- [ ] 在根目录创建文件：
  - [ ] `README.md`（简单介绍 + TODO 占位）
  - [ ] `environment.yml`（复制 overview 中示例依赖）
- [ ] 创建 conda 环境：
  - [ ] `conda env create -f environment.yml`
  - [ ] `conda activate ai_renewable`
  - [ ] `python -c "import geopandas, rasterio, streamlit; print('ok')"` 通过

**Done 标准**

- 一条命令可以激活环境并成功 import 关键库
- 目录树与 `docs/overview.md` 中一致

---

## Phase 1：区域边界 + 基础栅格（DEM & 辐照度）

**目标**：在 notebook 里能画出「研究区域 + DEM + 辐照度」三张基础图。

### 任务 1：区域边界

- [ ] 选定研究区域：
  - 方案 A：爱尔兰全境（推荐）
  - 方案 B：爱尔兰中东/南部若干 county
- [ ] 下载或裁剪出研究区域边界（county / national boundary）
- [ ] 导出为 `data/raw/region_boundary.geojson`
- [ ] 在 `src/data/preprocess.py` 中实现：
  - [ ] `load_region_boundary()`：读取并重投影到 `TARGET_CRS`

### 任务 2：DEM（地形）

- [ ] 从 Copernicus DEM / EU-DEM 下载覆盖爱尔兰的 DEM → `data/raw/dem_ireland.tif`
- [ ] 在 `preprocess.py` 中实现：
  - [ ] `reproject_raster(dem_raw → dem_reproj, res=GRID_RES_M)`
  - [ ] `clip_raster_to_region(dem_reproj → dem_clipped)`
- [ ] 输出：
  - [ ] `data/interim/dem_reproj.tif`
  - [ ] `data/interim/dem_clipped.tif`

### 任务 3：太阳辐照度

- [ ] 从 PVGIS 或类似数据源下载长期平均辐照度 → `data/raw/irradiance_ireland.tif`
- [ ] 在 `preprocess.py` 中复用同样流程：
  - [ ] `irradiance_reproj.tif`
  - [ ] `irradiance_clipped.tif`（裁剪到 region）

### 任务 4：探索 notebook

在 `notebooks/01_explore_data.ipynb` 中：

- [ ] 读取 `region_boundary.geojson` 并绘制边界
- [ ] 可视化 `dem_clipped.tif` + 边界线
- [ ] 可视化 `irradiance_clipped.tif` + 边界线
- [ ] 打印基本统计（min / max / mean）  
- [ ] 简短文字小结：该区域地形 & 资源大概情况

**Done 标准**

- `01_explore_data.ipynb` 能从头跑完
- 输出至少两张图：
  - DEM + 边界
  - 太阳辐照度 + 边界

---

## Phase 2：特征工程（坡度 / 距离 / 土地利用）

**目标**：为每个栅格单元计算关键特征，并理解其分布。

### 任务 1：坡度

在 `src/features/build_features.py` 中：

- [ ] 从 `dem_clipped.tif` 计算坡度栅格：
  - [ ] `slope.tif`（单位：度）
- [ ] 保证与其他栅格共享同一 CRS 和分辨率

### 任务 2：土地利用

- [ ] 下载土地利用数据：
  - CLC2018 或爱尔兰国家土地覆盖图 → `data/raw/landcover.*`
- [ ] 在 `preprocess.py` 中：
  - [ ] 重投影到 `TARGET_CRS`
  - [ ] 裁剪到 region → `landcover_clipped.*`

### 任务 3：电网与道路距离

- [ ] 从 OSM / 其它源准备：
  - [ ] 输电线路 & 变电站 → `data/raw/power_lines.*`
  - [ ] 主干道路 → `data/raw/roads.*`
- [ ] 在 `build_features.py` 中：
  - [ ] rasterize 或基于矢量计算距离：
    - [ ] `dist_grid.tif`（到最近电力线/变电站的距离，m）
    - [ ] `dist_roads.tif`（到最近主干道路的距离，m）
  - [ ] 与 DEM / 辐照度栅格对齐

### 任务 4：特征检查 notebook

在 `notebooks/02_feature_engineering.ipynb` 中：

- [ ] 显示以下栅格的分布：
  - `slope.tif`
  - `dist_grid.tif`
  - `dist_roads.tif`
  - `irradiance_clipped.tif`
  - `landcover_clipped.*`（类别统计）
- [ ] 为每个特征画直方图 / 统计数值
- [ ] 根据分布粗略设定阈值：
  - [ ] 最大坡度（如 15°）
  - [ ] 最大电网距离（如 50km）
  - [ ] 允许/禁止的土地利用类别

**Done 标准**

- `data/interim/` 下存在：
  - `slope.tif`
  - `dist_grid.tif`
  - `dist_roads.tif`
  - `landcover_clipped.*`
- `02_feature_engineering.ipynb` 能展示这些特征的分布，并写下一些「候选阈值」

---

## Phase 3：评分 & Top N 候选点

**目标**：得到一个综合评分栅格 + TopN 候选点（含经纬度和指标）。

### 任务 1：归一化与 Mask

在 `src/features/compute_scores.py` 中实现：

- [ ] 加载标准化后的特征栅格：
  - 资源：辐照度
  - 地形：坡度
  - 电网/道路距离
  - 土地利用类别
- [ ] 定义归一化函数：
  - [ ] `R_norm`：按比例缩放到 [0,1]
  - [ ] `G_norm`：`1 - d/D_max` 剪裁到 [0,1]
  - [ ] `T_norm`：基于坡度的 piecewise 线性函数
  - [ ] `L_norm`：根据 land cover code 查表
- [ ] 构建可用性 `mask_available`：
  - 坡度超过阈值 → 0
  - 土地利用不允许 → 0
  - 其它 → 1

### 任务 2：综合评分

- [ ] 实现评分公式：

  ```text
  Score = 100 * (w_R*R_norm + w_G*G_norm + w_T*T_norm + w_L*L_norm)
  Score_final = Score * mask_available
 默认权重使用 config.py 中的 DEFAULT_WEIGHTS

 将 Score_final 写出为 data/processed/score.tif

任务 3：Top N 候选点
 将评分栅格展平为表格（每个 cell 一行）

 过滤 mask_available == 0 的 cell

 按 Score_final 排序，取 Top N（如 N=50）

 计算每个 cell 的中心点坐标（经纬度）

 组装 GeoDataFrame，包含：

geometry（Point）

score

各个特征值：R/G/T/L

 输出到：

 data/processed/top_sites.geojson

 data/processed/top_sites.csv

任务 4：评分与 TopN 可视化 notebook
在 notebooks/03_scoring_and_maps.ipynb 中：

 载入 score.tif 并绘制热力图

 载入 top_sites.geojson，将点叠加在热力图和底图上

 选择若干典型候选点，打印其指标构成（方便解释）

Done 标准

data/processed/score.tif 存在且数值在 [0,100]

top_sites.geojson 中有 N 个点，每个点有 score+指标

03_scoring_and_maps.ipynb 能生成一张「热力图 + TopN 点叠加」的 PNG

Phase 4：Web Demo & 文档包装
目标：通过 Streamlit 提供一个可交互的 Demo，并补齐 README / docs。

任务 1：Streamlit 前端
在 app/app.py 中：

 布局：

 左：侧边栏（权重 slider、阈值 slider）

 右：地图展示区域

 参数：

 w_R, w_G, w_T, w_L（0–1 slider，自动归一化）

 最大坡度、最大电网距离等阈值

 逻辑：

 将当前参数传入 compute_scores_and_top_sites()

 获取新的 score 栅格和 TopN 点

 地图：

 调用 viz.make_maps 生成交互式地图（folium 等）

 在 Streamlit 中通过 HTML 或内置组件展示

任务 2：可视化封装
在 src/viz/make_maps.py 中：

 make_static_map(score_raster, top_sites) -> Matplotlib figure

 make_interactive_map(score_raster, top_sites) -> folium.Map

 确保可以同时供 notebook 和 Streamlit 调用

任务 3：文档 & README
 更新 README.md：

 项目简介（1–2 段）

 截图（热力图 + TopN 叠加）

 安装与运行步骤（环境、预处理、启动 app）

 数据来源列表（简略版本）

 更新 docs/：

 docs/overview.md 与实际结构保持一致

 新建或补充：

 docs/data_sources.md

 docs/interfaces.md（列出核心函数与入口）

Done 标准

在新环境中执行：

conda env create -f environment.yml

conda activate ai_renewable

streamlit run app/app.py

浏览器中可以：

看见基础地图

调节权重后候选点明显发生变化

README + docs 足以让陌生工程师在 1 小时内复现 Demo。
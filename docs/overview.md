# AI + 新能源选址 Demo · 概览（overview）

> 目标：  
> 构建一个 **AI + 光伏选址（先从爱尔兰开始）** 的最小可用 Demo：  
> - 能在本地一键运行  
> - 有清晰的地图可视化  
> - 能作为作品集/对话入口展示你的 **GIS + 气象 + 能源投资思维** 能力。

---

## 1. Demo 核心概念

做一个面向投资人/开发商的 **光伏选址评分系统**：

- 对研究区域（例如：爱尔兰全国或部分 county）进行 **栅格化评分**；
- 输出：
  - 一张：**最佳光伏场址热力图**（score raster）
  - 一组：**Top N 候选场址**（点或小区域，附带指标和总评分）
  - 一个：**交互式 Web 页面**（调整权重 / 阈值 → 实时刷新地图）

系统只做“前期筛选 + 可视化解释”，不做复杂金融模型。

---

## 2. MVP 范围与简化假设

### 2.1 考虑的因素（v0）

- **资源（R）**：  
  年平均太阳辐照度 / 光伏输出潜力（来自 PVGIS 等开源数据）
- **地形（T）**：  
  坡度（越平坦越好），可选地考虑坡向偏好
- **电网接入（G）**：  
  到最近高压输电线路或变电站的距离（OSM 或简化电网图）
- **土地利用（L）**：  
  农田/荒地更优，水体/保护区/核心城市区域视为不可用或低分

### 2.2 暂时不考虑的内容（后续版本再加）

- 电价、补贴政策、容量上限、并网排队等细节
- 完整的现金流 / NPV / IRR 金融模型
- 复杂的风光协同、电力系统约束

### 2.3 输出形式

1. **Score 栅格**：0–100 的综合评分（每个 cell 一分）
2. **Top N 候选点**：  
   每个点包含：
   - 经纬度  
   - Score  
   - R/G/T/L 各指标值与部分约束信息
3. **交互式 Demo（Streamlit）**：
   - 左侧：权重和阈值 slider  
   - 右侧：地图（热力图 + Top N 点）

---

## 3. 技术与数据选型（简表）

### 3.1 技术栈

- **语言**：Python 3.11
- **环境管理**：conda（`environment.yml`）
- **地理数据处理**：
  - `geopandas`, `shapely` —— 矢量数据
  - `rasterio`, `rioxarray`, `rasterstats` —— 栅格数据
- **数值 & 可视化**：
  - `numpy`, `pandas`, `matplotlib`, `folium`
- **Web Demo**：
  - `streamlit`

### 3.2 典型数据源（以爱尔兰为例）

- **太阳辐照度 / 光伏潜力**：
  - PVGIS（欧委会 JRC）长期平均辐照度 / PV potential
- **地形（DEM）**：
  - Copernicus DEM / EU-DEM（30m 级别）
- **土地利用**：
  - CORINE Land Cover（CLC 2018）或国家土地覆盖图
- **电网 / 道路**：
  - OpenStreetMap（`power=line/substation`，主干道路）

所有原始文件放在 `data/raw/`，通过脚本处理后写入 `data/interim/`、`data/processed/`。

---

## 4. 项目结构（Project Structure）

```text
ai_renewable_site_demo/
├── README.md
├── environment.yml           # conda 环境定义
├── data/
│   ├── raw/                  # 原始下载数据（只新增，不覆盖）
│   ├── interim/              # 中间文件：重投影 / 裁剪 / 重采样
│   └── processed/            # 最终特征 & 评分结果（score、top_sites）
├── notebooks/
│   ├── 01_explore_data.ipynb        # 基础数据探索（DEM + 辐照度）
│   ├── 02_feature_engineering.ipynb # 特征分布、阈值选择
│   └── 03_scoring_and_maps.ipynb    # 评分 + 地图可视化
├── src/
│   ├── config.py             # 全局配置（路径、CRS、默认参数）
│   ├── data/
│   │   └── preprocess.py     # 读取边界、重投影、裁剪、写入 interim
│   ├── features/
│   │   ├── build_features.py # 生成坡度、距离等特征
│   │   └── compute_scores.py # 归一化 + 评分 + Top N
│   └── viz/
│       └── make_maps.py      # 静态/交互地图封装
├── app/
│   └── app.py                # Streamlit Web Demo 入口
└── scripts/
    └── scratch.py            # 临时实验脚本（沙箱）

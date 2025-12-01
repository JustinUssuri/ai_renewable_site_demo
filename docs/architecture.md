# 架构概览

目前文档规模不大，概念层与实现层的关系紧密，放在一个文件里更方便同步维护，因此暂不拆分成两个 md（后续若 Web/App 与数据处理演进出更多职责，再按层拆分）。

## 概念层（业务流程）

```mermaid
flowchart LR
    A[原始数据\nDEM / 辐照度 / 土地利用 / OSM 电网] --> B[统一边界\nregion_boundary.geojson]
    B --> C[栅格预处理\n重投影 + 裁剪]
    C --> D[特征工程\n坡度/距离/土地利用栅格]
    D --> E[评分模型\n归一化 + 权重]
    E --> F[输出\nscore.tif + TopN]
    F --> G[可视化 & Demo\nNotebook + Streamlit]
```

## 实现层（代码与文件）

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

> **关联说明**：
> - `scripts/*` 负责一次性/独立的准备工作，例如 dissolve 边界、检查 DEM。
> - `src/data/preprocess.py` 提供可复用函数（读取边界、重投影、裁剪）供 notebooks 与 pipeline 共享。
> - `src/features/*` 以预处理产物为输入，生成特征与最后的评分。
> - `notebooks`、`src/viz`、`app/app.py` 共享评分结果进行可视化与交互展示。

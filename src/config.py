from pathlib import Path

# 根目录（ai_renewable_site_demo）
ROOT_DIR = Path(__file__).resolve().parents[1]

# 数据路径
DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"

# 空间参考 & 分辨率
TARGET_CRS = "EPSG:2157"  # Irish Transverse Mercator
GRID_RES_M = 1000         # 1 km resolution

# 默认评分权重（可以之后调整）
DEFAULT_WEIGHTS = {
    "R": 0.4,  # 资源（辐照度）
    "G": 0.3,  # 电网接入
    "T": 0.2,  # 地形
    "L": 0.1,  # 土地利用
}

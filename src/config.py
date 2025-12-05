from pathlib import Path

# Project root
ROOT_DIR = Path(__file__).resolve().parents[1]

# Data paths
DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"

# Spatial reference & resolution
TARGET_CRS = "EPSG:2157"  # Irish Transverse Mercator
GRID_RES_M = 1000         # 1 km resolution

# Default scoring weights (tweak as needed)
DEFAULT_WEIGHTS = {
    "R": 0.4,  # Resource (irradiance)
    "G": 0.3,  # Grid access
    "T": 0.2,  # Terrain
    "L": 0.1,  # Land use
}

from .dem import load_dem
from .distance import load_dist_grid, load_dist_roads
from .irradiance import load_irradiance
from .landcover import load_landcover
from .slope import load_slope

__all__ = [
    "load_dem",
    "load_dist_grid",
    "load_dist_roads",
    "load_irradiance",
    "load_landcover",
    "load_slope",
]

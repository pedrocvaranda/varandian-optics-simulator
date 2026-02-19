"""Core package initialization.

Re-export commonly used functions from submodules so users can
import them with `from core import compute_ray, SK, varandian_snell`.
"""

from .metrics import SK, dSK_dr, metric_tensor, proper_distance, space_type_name
from .geodesics import (
    compute_ray,
    compute_ray_numerical,
    compute_ray_analytical_sphere,
    compute_ray_analytical_hyperbolic,
)
from .refraction import (
    varandian_snell,
    critical_angle,
    index_curvature_duality_spherical,
    index_curvature_duality_hyperbolic,
    fresnel_coefficient_varandian,
)

__all__ = [
    "SK",
    "dSK_dr",
    "metric_tensor",
    "proper_distance",
    "space_type_name",
    "compute_ray",
    "compute_ray_numerical",
    "compute_ray_analytical_sphere",
    "compute_ray_analytical_hyperbolic",
    "varandian_snell",
    "critical_angle",
    "index_curvature_duality_spherical",
    "index_curvature_duality_hyperbolic",
    "fresnel_coefficient_varandian",
]

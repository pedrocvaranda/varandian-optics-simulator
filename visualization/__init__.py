"""
Varandian Optics - Visualization Module

Projection methods and plotting utilities.
"""

from .projections import (
    stereographic_projection,
    poincare_disk,
    polar_to_cartesian,
    project_ray
)

from .plotting import (
    plot_single_ray,
    plot_multiple_rays,
    plot_comparison,
    plot_polar
)

__all__ = [
    'stereographic_projection',
    'poincare_disk',
    'polar_to_cartesian',
    'project_ray',
    'plot_single_ray',
    'plot_multiple_rays',
    'plot_comparison',
    'plot_polar',
]

"""
Varandian Optics - Projections Module

2D projection methods for visualizing curved spaces:
- Stereographic projection (spherical space)
- Poincaré disk (hyperbolic space)
- Standard polar (Euclidean space)
"""

import numpy as np


def stereographic_projection(r, theta):
    """
    Stereographic projection from sphere to plane.
    
    Maps the sphere S² to the complex plane C via projection
    from the south pole.
    
    For a point at (r, θ) in geodesic polar coordinates on the sphere,
    we first convert to Cartesian on the sphere:
        x = sin(r) cos(θ)
        y = sin(r) sin(θ)
        z = cos(r)
    
    Then project from south pole (0,0,-1):
        u = x / (1 + z)
        v = y / (1 + z)
    
    Parameters
    ----------
    r : float or np.ndarray
        Radial coordinate on sphere [0, π]
    theta : float or np.ndarray
        Angular coordinate [0, 2π]
    
    Returns
    -------
    u, v : np.ndarray
        Cartesian coordinates in projection plane
    
    Notes
    -----
    - Preserves angles (conformal mapping)
    - Great circles → circles or lines
    - South pole maps to infinity
    """
    r = np.asarray(r)
    theta = np.asarray(theta)
    
    # Sphere coordinates
    x_sphere = np.sin(r) * np.cos(theta)
    y_sphere = np.sin(r) * np.sin(theta)
    z_sphere = np.cos(r)
    
    # Avoid division by zero at south pole
    denominator = 1 + z_sphere
    denominator = np.where(np.abs(denominator) < 1e-10, 1e-10, denominator)
    
    # Project
    u = x_sphere / denominator
    v = y_sphere / denominator
    
    return u, v


def poincare_disk(r, theta):
    """
    Poincaré disk model for hyperbolic space.
    
    Maps hyperbolic plane H² to unit disk |z| < 1.
    
    The radial coordinate r ∈ [0, ∞) is mapped to
    ρ = tanh(r/2) ∈ [0, 1)
    
    Then in Cartesian:
        u = ρ cos(θ)
        v = ρ sin(θ)
    
    Parameters
    ----------
    r : float or np.ndarray
        Radial coordinate in hyperbolic space [0, ∞)
    theta : float or np.ndarray
        Angular coordinate [0, 2π]
    
    Returns
    -------
    u, v : np.ndarray
        Cartesian coordinates in unit disk
    
    Notes
    -----
    - Preserves angles (conformal)
    - Geodesics → circular arcs perpendicular to boundary
    - Infinity maps to unit circle boundary
    """
    r = np.asarray(r)
    theta = np.asarray(theta)
    
    # Map r to [0,1) via tanh
    rho = np.tanh(r / 2.0)
    
    # Cartesian in disk
    u = rho * np.cos(theta)
    v = rho * np.sin(theta)
    
    return u, v


def polar_to_cartesian(r, theta):
    """
    Standard polar to Cartesian conversion (for Euclidean space).
    
    Parameters
    ----------
    r : float or np.ndarray
        Radial coordinate
    theta : float or np.ndarray
        Angular coordinate
    
    Returns
    -------
    x, y : np.ndarray
        Cartesian coordinates
    """
    r = np.asarray(r)
    theta = np.asarray(theta)
    
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    
    return x, y


def project_ray(r, theta, K):
    """
    Automatically choose appropriate projection based on curvature.
    
    Parameters
    ----------
    r : np.ndarray
        Radial coordinates
    theta : np.ndarray
        Angular coordinates
    K : float
        Curvature constant
    
    Returns
    -------
    u, v : np.ndarray
        Projected coordinates
    projection_name : str
        Name of projection used
    """
    if K > 0:
        u, v = stereographic_projection(r, theta)
        return u, v, "Stereographic Projection (Spherical)"
    
    elif K < 0:
        u, v = poincare_disk(r, theta)
        return u, v, "Poincaré Disk (Hyperbolic)"
    
    else:  # K == 0
        u, v = polar_to_cartesian(r, theta)
        return u, v, "Cartesian (Euclidean)"


def draw_reference_circle(ax, K):
    """
    Draw reference circle for bounded projections.
    
    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes to draw on
    K : float
        Curvature (only draws for K ≠ 0)
    """
    if K == 0:
        return
    
    circle = plt.Circle((0, 0), 1.0, 
                        fill=False, 
                        color='gray', 
                        linestyle='--', 
                        linewidth=1,
                        alpha=0.5,
                        label='Projection boundary')
    ax.add_patch(circle)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
    # Test projections
    print("Testing projections:")
    
    # Sample ray
    theta = np.linspace(0, 2*np.pi, 100)
    r = 0.5 + 0.3 * np.sin(3 * theta)  # Some wavy curve
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Spherical
    u, v, name = project_ray(r, theta, K=1.0)
    axes[0].plot(u, v)
    axes[0].set_aspect('equal')
    axes[0].set_title(name)
    axes[0].grid(True, alpha=0.3)
    
    # Euclidean
    u, v, name = project_ray(r, theta, K=0.0)
    axes[1].plot(u, v)
    axes[1].set_aspect('equal')
    axes[1].set_title(name)
    axes[1].grid(True, alpha=0.3)
    
    # Hyperbolic
    u, v, name = project_ray(r, theta, K=-1.0)
    axes[2].plot(u, v)
    axes[2].set_aspect('equal')
    axes[2].set_title(name)
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/claude/test_projections.png', dpi=100, bbox_inches='tight')
    print("Saved test_projections.png")

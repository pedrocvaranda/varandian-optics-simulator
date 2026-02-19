"""
Varandian Optics - Plotting Module

High-level plotting functions for visualizing rays and comparisons.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from .projections import project_ray, stereographic_projection, poincare_disk, polar_to_cartesian


def plot_single_ray(theta, r, K, figsize=(8, 8), save_path=None):
    """
    Plot a single ray with appropriate projection.
    
    Parameters
    ----------
    theta : np.ndarray
        Angular coordinates
    r : np.ndarray
        Radial coordinates
    K : float
        Curvature constant
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save figure
    
    Returns
    -------
    fig, ax : matplotlib figure and axes
    """
    # Project to 2D
    u, v, projection_name = project_ray(r, theta, K)
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot ray
    ax.plot(u, v, 'b-', linewidth=2, label='Light ray')
    
    # Mark start and end
    ax.plot(u[0], v[0], 'go', markersize=10, label='Start', zorder=5)
    ax.plot(u[-1], v[-1], 'ro', markersize=10, label='End', zorder=5)
    
    # Reference circle for bounded projections
    if K != 0:
        circle = Circle((0, 0), 1.0, fill=False, color='gray', 
                       linestyle='--', linewidth=1, alpha=0.5)
        ax.add_patch(circle)
    
    # Formatting
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('u', fontsize=12)
    ax.set_ylabel('v', fontsize=12)
    
    # Title with space type
    if K > 0:
        space_name = "Spherical"
    elif K < 0:
        space_name = "Hyperbolic"
    else:
        space_name = "Euclidean"
    
    ax.set_title(f'{space_name} Space (K={K:.2f})\n{projection_name}', 
                 fontsize=14, fontweight='bold')
    
    ax.legend(loc='best', fontsize=10)
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved to {save_path}")
    
    return fig, ax


def plot_multiple_rays(rays_data, K, figsize=(10, 10), save_path=None):
    """
    Plot multiple rays on the same figure.
    
    Parameters
    ----------
    rays_data : list of tuples
        Each tuple is (theta, r, label, color)
    K : float
        Curvature (same for all rays)
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save
    
    Returns
    -------
    fig, ax : matplotlib figure and axes
    
    Examples
    --------
    >>> rays = [
    ...     (theta1, r1, 'Ray 1', 'blue'),
    ...     (theta2, r2, 'Ray 2', 'red'),
    ... ]
    >>> plot_multiple_rays(rays, K=1.0)
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    for theta, r, label, color in rays_data:
        u, v, projection_name = project_ray(r, theta, K)
        ax.plot(u, v, color=color, linewidth=2, label=label, alpha=0.8)
        # Mark start
        ax.plot(u[0], v[0], 'o', color=color, markersize=8, zorder=5)
    
    # Reference circle
    if K != 0:
        circle = Circle((0, 0), 1.0, fill=False, color='gray',
                       linestyle='--', linewidth=1, alpha=0.5)
        ax.add_patch(circle)
    
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('u', fontsize=12)
    ax.set_ylabel('v', fontsize=12)
    
    if K > 0:
        space_name = "Spherical"
    elif K < 0:
        space_name = "Hyperbolic"
    else:
        space_name = "Euclidean"
    
    ax.set_title(f'Multiple Rays in {space_name} Space (K={K:.2f})',
                 fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved to {save_path}")
    
    return fig, ax


def plot_comparison(theta, r, K_values=[-1, 0, 1], figsize=(15, 5), save_path=None):
    """
    Compare same initial conditions across different curvatures.
    
    Parameters
    ----------
    theta : np.ndarray
        Angular coordinate (same for all)
    r : dict
        Dictionary mapping K values to r arrays
        e.g., {-1: r_hyperbolic, 0: r_euclidean, 1: r_spherical}
    K_values : list
        List of K values to compare
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save
    
    Returns
    -------
    fig, axes : matplotlib figure and axes array
    """
    n_plots = len(K_values)
    fig, axes = plt.subplots(1, n_plots, figsize=figsize)
    
    if n_plots == 1:
        axes = [axes]
    
    for idx, K in enumerate(K_values):
        ax = axes[idx]
        
        # Get r for this K
        r_data = r[K]
        
        # Project
        u, v, projection_name = project_ray(r_data, theta, K)
        
        # Plot
        ax.plot(u, v, 'b-', linewidth=2)
        ax.plot(u[0], v[0], 'go', markersize=10, zorder=5)
        ax.plot(u[-1], v[-1], 'ro', markersize=10, zorder=5)
        
        # Reference circle
        if K != 0:
            circle = Circle((0, 0), 1.0, fill=False, color='gray',
                           linestyle='--', linewidth=1, alpha=0.5)
            ax.add_patch(circle)
        
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('u', fontsize=11)
        ax.set_ylabel('v', fontsize=11)
        
        if K > 0:
            space_name = "Spherical"
        elif K < 0:
            space_name = "Hyperbolic"
        else:
            space_name = "Euclidean"
        
        ax.set_title(f'{space_name}\nK={K:.1f}', fontsize=12, fontweight='bold')
    
    plt.suptitle('Ray Propagation Comparison', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved to {save_path}")
    
    return fig, axes


def plot_polar(theta, r, K, figsize=(8, 8), save_path=None):
    """
    Plot in native polar coordinates (before projection).
    
    Useful for seeing the raw geodesic shape.
    
    Parameters
    ----------
    theta : np.ndarray
        Angular coordinates
    r : np.ndarray
        Radial coordinates
    K : float
        Curvature (for labeling)
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save
    
    Returns
    -------
    fig, ax : matplotlib figure and axes
    """
    fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(projection='polar'))
    
    ax.plot(theta, r, 'b-', linewidth=2)
    ax.plot(theta[0], r[0], 'go', markersize=10, zorder=5)
    ax.plot(theta[-1], r[-1], 'ro', markersize=10, zorder=5)
    
    ax.set_title(f'Geodesic in Polar Coordinates\nK={K:.2f}',
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved to {save_path}")
    
    return fig, ax


if __name__ == "__main__":
    # Quick test
    from core.geodesics import compute_ray
    
    print("Testing plotting functions...")
    
    # Compute a sample ray
    theta, r = compute_ray(r0=0.5, theta0=0, K=1.0, C=0.3)
    
    # Test single ray plot
    fig, ax = plot_single_ray(theta, r, K=1.0, 
                              save_path='/home/claude/test_single_ray.png')
    plt.close()
    
    print("Test completed! Check test_single_ray.png")

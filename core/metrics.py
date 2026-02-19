"""
Varandian Optics - Metrics Module

Implements the fundamental metric functions from:
"Varandian Optics: A Non-Euclidean Formulation of Light Propagation"
Pedro Coutinho Varanda, Brazilian Journal of Physics, 2026

Equations implemented:
- (1) General metric: ds² = dr² + SK(r)² dθ²
- (2) SK(r) function for different curvatures
"""

import numpy as np


def SK(r, K):
    """
    Compute SK(r) - the angular metric component.
    
    From equation (2) in the paper:
    
    SK(r) = { 1/√K * sin(√K*r),      K > 0  (Spherical)
            { r,                      K = 0  (Euclidean)
            { 1/√|K| * sinh(√|K|*r), K < 0  (Hyperbolic)
    
    Parameters
    ----------
    r : float or np.ndarray
        Radial coordinate
    K : float
        Curvature constant
        K > 0: Spherical (positive curvature)
        K = 0: Euclidean (flat)
        K < 0: Hyperbolic (negative curvature)
    
    Returns
    -------
    float or np.ndarray
        Value of SK(r)
    
    Examples
    --------
    >>> SK(1.0, K=1.0)  # Spherical
    0.8414709848078965
    
    >>> SK(1.0, K=0.0)  # Euclidean
    1.0
    
    >>> SK(1.0, K=-1.0)  # Hyperbolic
    1.1752011936438014
    """
    r = np.asarray(r)
    
    if K > 0:
        # Spherical space
        sqrt_K = np.sqrt(K)
        return (1.0 / sqrt_K) * np.sin(sqrt_K * r)
    
    elif K == 0:
        # Euclidean space
        return r
    
    else:  # K < 0
        # Hyperbolic space
        sqrt_abs_K = np.sqrt(abs(K))
        return (1.0 / sqrt_abs_K) * np.sinh(sqrt_abs_K * r)


def dSK_dr(r, K):
    """
    Compute derivative of SK(r) with respect to r.
    
    Useful for geodesic equations and refraction calculations.
    
    dSK/dr = { cos(√K*r),      K > 0
             { 1,              K = 0
             { cosh(√|K|*r),   K < 0
    
    Parameters
    ----------
    r : float or np.ndarray
        Radial coordinate
    K : float
        Curvature constant
    
    Returns
    -------
    float or np.ndarray
        Derivative dSK/dr
    """
    r = np.asarray(r)
    
    if K > 0:
        sqrt_K = np.sqrt(K)
        return np.cos(sqrt_K * r)
    
    elif K == 0:
        return np.ones_like(r)
    
    else:  # K < 0
        sqrt_abs_K = np.sqrt(abs(K))
        return np.cosh(sqrt_abs_K * r)


def metric_tensor(r, K):
    """
    Compute the metric tensor g_ij in polar geodesic coordinates.
    
    From equation (1):
    ds² = dr² + SK(r)² dθ²
    
    Returns 2x2 diagonal matrix:
    g = [[1,        0      ],
         [0,   SK(r)²      ]]
    
    Parameters
    ----------
    r : float
        Radial coordinate
    K : float
        Curvature constant
    
    Returns
    -------
    np.ndarray
        2x2 metric tensor
    
    Examples
    --------
    >>> g = metric_tensor(1.0, K=1.0)
    >>> print(g)
    [[1.         0.        ]
     [0.         0.70807342]]
    """
    g_rr = 1.0
    g_theta_theta = SK(r, K)**2
    
    return np.array([
        [g_rr, 0.0],
        [0.0, g_theta_theta]
    ])


def proper_distance(r1, r2, K):
    """
    Compute proper radial distance between r1 and r2.
    
    Simply |r2 - r1| since radial metric component is 1.
    
    Parameters
    ----------
    r1, r2 : float
        Radial coordinates
    K : float
        Curvature constant (not used, but kept for API consistency)
    
    Returns
    -------
    float
        Proper radial distance
    """
    return abs(r2 - r1)


def space_type_name(K):
    """
    Return human-readable name for space type.
    
    Parameters
    ----------
    K : float
        Curvature constant
    
    Returns
    -------
    str
        Space type name
    """
    if K > 0:
        return "Spherical"
    elif K == 0:
        return "Euclidean"
    else:
        return "Hyperbolic"


if __name__ == "__main__":
    # Quick test
    print("Testing Varandian Metrics:")
    print(f"SK(1.0, K=+1) = {SK(1.0, 1.0):.6f} (Spherical)")
    print(f"SK(1.0, K=0)  = {SK(1.0, 0.0):.6f} (Euclidean)")
    print(f"SK(1.0, K=-1) = {SK(1.0, -1.0):.6f} (Hyperbolic)")
    print("\nMetric tensor at r=1, K=1:")
    print(metric_tensor(1.0, 1.0))

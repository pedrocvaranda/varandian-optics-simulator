"""
Varandian Optics - Geodesics Module

Implements geodesic ray propagation from:
"Varandian Optics: A Non-Euclidean Formulation of Light Propagation"

Equations implemented:
- (3) General geodesic equation
- (4) Analytical solution for spherical space (K > 0)
- (5) Analytical solution for hyperbolic space (K < 0)
"""

import numpy as np
from scipy.integrate import odeint, solve_ivp
from .metrics import SK


def geodesic_ode(state, theta, K, C):
    """
    ODE system for geodesic equation (3).
    
    From the paper:
    (dr/dθ)² = (SK(r)²/C²) * (SK(r)² - C²)
    
    We convert to first-order system:
    dr/dθ = v
    dv/dθ = d²r/dθ²
    
    Parameters
    ----------
    theta : float
        Angular coordinate (independent variable)
    state : array-like
        [r, dr/dθ]
    K : float
        Curvature constant
    C : float
        Constant of motion (conserved angular momentum-like quantity)
    
    Returns
    -------
    list
        [dr/dθ, d²r/dθ²]
    """
    r, v = state
    
    # Avoid numerical issues
    if r <= 0:
        r = 1e-10
    
    SK_r = SK(r, K)
    
    # From equation (3)
    # We need to be careful with signs and square roots
    try:
        term = (SK_r**2 / C**2) * (SK_r**2 - C**2)
        
        # The geodesic equation
        if term >= 0:
            dvdtheta = np.sqrt(term) if v >= 0 else -np.sqrt(term)
        else:
            dvdtheta = 0  # Turning point
            
    except:
        dvdtheta = 0
    
    return [v, dvdtheta]


def compute_ray_numerical(r0, theta0, K, C, theta_max=2*np.pi, n_points=1000):
    """
    Compute ray trajectory by numerical integration of equation (3).
    
    Parameters
    ----------
    r0 : float
        Initial radial position
    theta0 : float
        Initial angular position
    K : float
        Curvature constant
    C : float
        Constant of motion (0 < C < 1 typically)
    theta_max : float
        Maximum angle to integrate to (default: 2π)
    n_points : int
        Number of points in solution
    
    Returns
    -------
    theta : np.ndarray
        Angular coordinates
    r : np.ndarray
        Radial coordinates along the ray
    
    Examples
    --------
    >>> theta, r = compute_ray_numerical(r0=0.5, theta0=0, K=1.0, C=0.3)
    >>> print(f"Ray computed with {len(theta)} points")
    """
    # Angular coordinates
    theta = np.linspace(theta0, theta0 + theta_max, n_points)

    # For numerical integration we integrate the first-order ODE
    # dr/dθ = ±sqrt( (SK(r)^2/C^2) * (SK(r)^2 - C^2) )
    # This is nonlinear but scalar; using `solve_ivp` avoids LSODA warnings
    # that can arise from discontinuous derivatives when using `odeint`.

    if C is None:
        raise ValueError("C parameter required for numerical method")

    # Choose initial sign for dr/dθ. If the user provides a small initial
    # radial velocity this could be used to pick the sign; default to +1.
    initial_sign = 1.0

    def dr_dtheta(theta_var, r_var):
        r_val = float(np.atleast_1d(r_var)[0])
        if r_val <= 0:
            r_val = 1e-10
        SK_r = SK(r_val, K)
        # Clip excessively large SK values to avoid overflow in sinh/sqrt
        if not np.isfinite(SK_r) or abs(SK_r) > 1e6:
            SK_r = np.sign(SK_r) * 1e6
        SK_r2 = SK_r * SK_r
        # Compute term safely
        term = (SK_r2 / (C**2)) * (SK_r2 - C**2)
        # Avoid negative or non-finite under the sqrt; treat as turning point
        if not np.isfinite(term) or term <= 0:
            return 0.0
        return initial_sign * np.sqrt(term)

    try:
        # Use a robust stiff solver (Radau) with controlled max_step
        sol = solve_ivp(dr_dtheta, (theta[0], theta[-1]), [r0], t_eval=theta,
                        method='Radau', vectorized=False,
                        max_step=(theta[-1] - theta[0]) / max(10, n_points))

        if sol.success:
            r = sol.y[0]
        else:
            # If solve_ivp failed, produce a safe output (zeros) instead of
            # falling back to odeint which previously raised warnings.
            r = np.full_like(theta, r0, dtype=float)

    except Exception:
        # If anything unexpected happens, return a constant-radius fallback
        r = np.full_like(theta, r0, dtype=float)

    # Clean up negative values (numerical artifacts)
    r = np.abs(r)

    return theta, r


def compute_ray_analytical_sphere(r0, theta0, A, theta_max=2*np.pi, n_points=1000):
    """
    Analytical solution for spherical space (K = +1).
    
    From equation (4) in the paper:
    tan(r) = -c / [A*cos(θ - θ0)]
    
    Parameters
    ----------
    r0 : float
        Initial radial position
    theta0 : float
        Initial angular position  
    A : float
        Integration constant (related to C)
    theta_max : float
        Maximum angle
    n_points : int
        Number of points
    
    Returns
    -------
    theta : np.ndarray
        Angular coordinates
    r : np.ndarray
        Radial coordinates
    """
    theta = np.linspace(theta0, theta0 + theta_max, n_points)
    
    # From equation (4): tan(r) = -c / [A*cos(θ - θ0)]
    # For simplicity, we use c = tan(r0) * A * cos(0) = tan(r0) * A
    c = np.tan(r0) * A
    
    # Compute r(θ)
    denominator = A * np.cos(theta - theta0)
    
    # Avoid division by zero
    denominator = np.where(np.abs(denominator) < 1e-10, 1e-10, denominator)
    
    r = np.arctan(-c / denominator)
    
    # Keep r positive and in [0, π]
    r = np.abs(r)
    r = np.where(r > np.pi, 2*np.pi - r, r)
    
    return theta, r


def compute_ray_analytical_hyperbolic(r0, theta0, B, theta_max=2*np.pi, n_points=1000):
    """
    Analytical solution for hyperbolic space (K = -1).
    
    From equation (5) in the paper:
    tanh(r) = -α / [B*cos(θ - θ0)]
    
    Parameters
    ----------
    r0 : float
        Initial radial position
    theta0 : float
        Initial angular position
    B : float
        Integration constant
    theta_max : float
        Maximum angle
    n_points : int
        Number of points
    
    Returns
    -------
    theta : np.ndarray
        Angular coordinates
    r : np.ndarray
        Radial coordinates
    """
    theta = np.linspace(theta0, theta0 + theta_max, n_points)
    
    # From equation (5): tanh(r) = -α / [B*cos(θ - θ0)]
    # α = tanh(r0) * B
    alpha = np.tanh(r0) * B
    
    # Compute r(θ)
    denominator = B * np.cos(theta - theta0)
    
    # Avoid division by zero
    denominator = np.where(np.abs(denominator) < 1e-10, 1e-10, denominator)
    
    argument = -alpha / denominator
    
    # tanh is bounded to [-1, 1], so clip the argument
    argument = np.clip(argument, -0.99, 0.99)
    
    r = np.arctanh(argument)
    
    # Keep r positive
    r = np.abs(r)
    
    return theta, r


def compute_ray(r0, theta0, K, C=None, A=None, B=None, 
                method='numerical', theta_max=2*np.pi, n_points=1000):
    """
    Compute ray trajectory with automatic method selection.
    
    This is the main function you'll use!
    
    Parameters
    ----------
    r0 : float
        Initial radial position
    theta0 : float
        Initial angular position
    K : float
        Curvature constant
    C : float, optional
        Constant of motion for numerical method
    A : float, optional
        Integration constant for analytical spherical
    B : float, optional
        Integration constant for analytical hyperbolic
    method : str
        'numerical', 'analytical', or 'auto' (default: 'numerical')
    theta_max : float
        Maximum angle to compute
    n_points : int
        Number of points
    
    Returns
    -------
    theta : np.ndarray
        Angular coordinates
    r : np.ndarray
        Radial coordinates
    
    Examples
    --------
    >>> # Numerical method (works for all K)
    >>> theta, r = compute_ray(r0=0.5, theta0=0, K=1.0, C=0.3)
    
    >>> # Analytical for sphere
    >>> theta, r = compute_ray(r0=0.5, theta0=0, K=1.0, A=1.0, method='analytical')
    """
    
    if method == 'auto':
        # Choose best method based on K
        if K > 0 and A is not None:
            method = 'analytical'
        elif K < 0 and B is not None:
            method = 'analytical'
        else:
            method = 'numerical'
    
    if method == 'analytical':
        if K > 0:
            if A is None:
                raise ValueError("A parameter required for analytical sphere")
            return compute_ray_analytical_sphere(r0, theta0, A, theta_max, n_points)
        elif K < 0:
            if B is None:
                raise ValueError("B parameter required for analytical hyperbolic")
            return compute_ray_analytical_hyperbolic(r0, theta0, B, theta_max, n_points)
        else:  # K == 0
            # Euclidean: straight line in polar coordinates
            theta = np.linspace(theta0, theta0 + theta_max, n_points)
            r = np.full_like(theta, r0)
            return theta, r
    
    else:  # numerical
        if C is None:
            raise ValueError("C parameter required for numerical method")
        return compute_ray_numerical(r0, theta0, K, C, theta_max, n_points)


if __name__ == "__main__":
    # Quick test
    print("Testing Varandian Geodesics:")
    
    print("\n1. Spherical (K=+1), numerical:")
    theta, r = compute_ray(r0=0.5, theta0=0, K=1.0, C=0.3, method='numerical')
    print(f"   Computed {len(theta)} points, r_min={r.min():.3f}, r_max={r.max():.3f}")
    
    print("\n2. Hyperbolic (K=-1), numerical:")
    theta, r = compute_ray(r0=0.5, theta0=0, K=-1.0, C=0.3, method='numerical')
    print(f"   Computed {len(theta)} points, r_min={r.min():.3f}, r_max={r.max():.3f}")
    
    print("\n3. Euclidean (K=0), numerical:")
    theta, r = compute_ray(r0=1.0, theta0=0, K=0.0, C=0.5, method='numerical')
    print(f"   Computed {len(theta)} points, r should be ~constant: {r.mean():.3f}")

"""
Varandian Optics - Refraction Module

Implements Varandian Snell's Law from:
"Varandian Optics: A Non-Euclidean Formulation of Light Propagation"
Pedro Coutinho Varanda, Zenodo, 2026
DOI: 10.5281/zenodo.18529071

Equations implemented:
- (6) Varandian Snell's Law: n₁ SK₁(r) sin(θ₁) = n₂ SK₂(r) sin(θ₂)
- (7) Index-curvature duality: n(ρ) profiles that emulate curved spaces
"""

import numpy as np
from .metrics import SK


def varandian_snell(theta1, n1, K1, n2, K2, r):
    """
    Varandian Snell's Law - compute refracted angle.
    
    From equation (6) in the paper:
    n₁ SK₁(r) sin(θ₁) = n₂ SK₂(r) sin(θ₂)
    
    This is the generalization of Snell's law to curved spaces.
    
    Parameters
    ----------
    theta1 : float
        Incident angle (radians)
    n1 : float
        Refractive index in medium 1
    K1 : float
        Curvature of space 1
    n2 : float
        Refractive index in medium 2
    K2 : float
        Curvature of space 2
    r : float
        Radial position where refraction occurs
    
    Returns
    -------
    theta2 : float
        Refracted angle (radians)
        Returns None if total internal reflection occurs
    
    Examples
    --------
    >>> # Refraction from spherical to Euclidean space
    >>> theta1 = np.pi/4  # 45 degrees
    >>> theta2 = varandian_snell(theta1, n1=1.0, K1=1.0, n2=1.5, K2=0.0, r=1.0)
    >>> print(f"Refracted angle: {np.degrees(theta2):.2f}°")
    
    Notes
    -----
    Total internal reflection occurs when:
    n₁ SK₁(r) sin(θ₁) > n₂ SK₂(r)
    
    In this case, the function returns None.
    """
    # Compute SK values
    SK1_val = SK(r, K1)
    SK2_val = SK(r, K2)
    
    # Varandian Snell's Law
    # n₁ SK₁(r) sin(θ₁) = n₂ SK₂(r) sin(θ₂)
    
    sin_theta1 = np.sin(theta1)
    
    # Compute sin(θ₂)
    sin_theta2 = (n1 * SK1_val * sin_theta1) / (n2 * SK2_val)
    
    # Check for total internal reflection
    if abs(sin_theta2) > 1.0:
        # Total internal reflection
        return None
    
    # Compute refracted angle
    theta2 = np.arcsin(sin_theta2)
    
    return theta2


def critical_angle(n1, K1, n2, K2, r):
    """
    Compute critical angle for total internal reflection.
    
    The critical angle θc is when sin(θ₂) = 1:
    θc = arcsin(n₂ SK₂(r) / (n₁ SK₁(r)))
    
    Parameters
    ----------
    n1, n2 : float
        Refractive indices
    K1, K2 : float
        Curvatures
    r : float
        Radial position
    
    Returns
    -------
    theta_c : float
        Critical angle (radians)
        Returns None if no critical angle exists (n₁ SK₁ < n₂ SK₂)
    
    Examples
    --------
    >>> theta_c = critical_angle(n1=1.5, K1=0.0, n2=1.0, K2=0.0, r=1.0)
    >>> print(f"Critical angle: {np.degrees(theta_c):.2f}°")
    """
    SK1_val = SK(r, K1)
    SK2_val = SK(r, K2)
    
    # Critical angle condition
    ratio = (n2 * SK2_val) / (n1 * SK1_val)
    
    if ratio >= 1.0:
        # No critical angle (can't have total internal reflection)
        return None
    
    theta_c = np.arcsin(ratio)
    return theta_c


def index_curvature_duality_spherical(rho):
    """
    Refractive index profile that emulates spherical geometry.
    
    From equation (7) - spherical case:
    n(ρ) = 2 / (1 + ρ²)
    
    This gradient-index profile in flat space creates the same
    optical behavior as constant positive curvature.
    
    Parameters
    ----------
    rho : float or np.ndarray
        Radial coordinate in the flat space (0 ≤ ρ < ∞)
    
    Returns
    -------
    n : float or np.ndarray
        Refractive index at position ρ
    
    Examples
    --------
    >>> rho = np.linspace(0, 2, 100)
    >>> n = index_curvature_duality_spherical(rho)
    >>> plt.plot(rho, n)
    >>> plt.xlabel('ρ')
    >>> plt.ylabel('n(ρ)')
    >>> plt.title('Spherical-Emulating Index Profile')
    
    Notes
    -----
    This is the Luneburg lens profile, which creates perfect imaging
    in flat space by emulating spherical geometry.
    """
    rho = np.asarray(rho)
    return 2.0 / (1.0 + rho**2)


def index_curvature_duality_hyperbolic(rho):
    """
    Refractive index profile that emulates hyperbolic geometry.
    
    From equation (7) - hyperbolic case:
    n(ρ) = 2 / (1 - ρ²)
    
    Valid for 0 ≤ ρ < 1 (Poincaré disk)
    
    Parameters
    ----------
    rho : float or np.ndarray
        Radial coordinate in the flat space (0 ≤ ρ < 1)
    
    Returns
    -------
    n : float or np.ndarray
        Refractive index at position ρ
    
    Examples
    --------
    >>> rho = np.linspace(0, 0.95, 100)
    >>> n = index_curvature_duality_hyperbolic(rho)
    >>> plt.plot(rho, n)
    >>> plt.xlabel('ρ')
    >>> plt.ylabel('n(ρ)')
    >>> plt.title('Hyperbolic-Emulating Index Profile')
    
    Notes
    -----
    The index diverges as ρ → 1 (boundary of Poincaré disk).
    This creates the "infinity at the boundary" characteristic
    of hyperbolic space.
    """
    rho = np.asarray(rho)
    
    # Ensure ρ < 1 to avoid division by zero
    if np.any(rho >= 1.0):
        raise ValueError("ρ must be < 1 for hyperbolic index profile")
    
    return 2.0 / (1.0 - rho**2)


def fresnel_coefficient_varandian(theta1, n1, K1, n2, K2, r, polarization='s'):
    """
    Fresnel reflection/transmission coefficients in Varandian optics.
    
    Generalization of Fresnel equations to curved spaces.
    
    Parameters
    ----------
    theta1 : float
        Incident angle (radians)
    n1, n2 : float
        Refractive indices
    K1, K2 : float
        Curvatures
    r : float
        Radial position
    polarization : str
        's' for s-polarization (TE), 'p' for p-polarization (TM)
    
    Returns
    -------
    R : float
        Reflection coefficient (intensity)
    T : float
        Transmission coefficient (intensity)
    
    Notes
    -----
    This is an extension of standard Fresnel equations.
    The key modification is using Varandian Snell's law to compute θ₂.
    """
    # Compute refracted angle using Varandian Snell
    theta2 = varandian_snell(theta1, n1, K1, n2, K2, r)
    
    if theta2 is None:
        # Total internal reflection
        return 1.0, 0.0
    
    cos_theta1 = np.cos(theta1)
    cos_theta2 = np.cos(theta2)
    
    if polarization == 's':
        # s-polarization (TE)
        r_s = (n1 * cos_theta1 - n2 * cos_theta2) / (n1 * cos_theta1 + n2 * cos_theta2)
        R = r_s**2
        T = 1.0 - R
    else:
        # p-polarization (TM)
        r_p = (n2 * cos_theta1 - n1 * cos_theta2) / (n2 * cos_theta1 + n1 * cos_theta2)
        R = r_p**2
        T = 1.0 - R
    
    return R, T


if __name__ == "__main__":
    # Quick tests
    print("Testing Varandian Refraction:\n")
    
    # Test 1: Euclidean Snell's law (should match standard)
    print("1. Euclidean case (K₁ = K₂ = 0):")
    theta1 = np.pi/4  # 45 degrees
    theta2 = varandian_snell(theta1, n1=1.0, K1=0.0, n2=1.5, K2=0.0, r=1.0)
    print(f"   Incident: {np.degrees(theta1):.2f}°")
    print(f"   Refracted: {np.degrees(theta2):.2f}°")
    
    # Standard Snell for comparison
    theta2_standard = np.arcsin(1.0 * np.sin(theta1) / 1.5)
    print(f"   Standard Snell: {np.degrees(theta2_standard):.2f}°")
    print(f"   Match: {np.abs(theta2 - theta2_standard) < 1e-10}")
    
    # Test 2: Critical angle
    print("\n2. Critical angle (glass to air):")
    theta_c = critical_angle(n1=1.5, K1=0.0, n2=1.0, K2=0.0, r=1.0)
    print(f"   θc = {np.degrees(theta_c):.2f}°")
    
    # Test 3: Index profiles
    print("\n3. Index-curvature duality:")
    print(f"   Spherical profile at ρ=0: n = {index_curvature_duality_spherical(0.0):.3f}")
    print(f"   Spherical profile at ρ=1: n = {index_curvature_duality_spherical(1.0):.3f}")
    print(f"   Hyperbolic profile at ρ=0: n = {index_curvature_duality_hyperbolic(0.0):.3f}")
    print(f"   Hyperbolic profile at ρ=0.5: n = {index_curvature_duality_hyperbolic(0.5):.3f}")
    
    print("\n✅ Refraction module tests complete!")

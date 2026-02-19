"""
Tests for Varandian Optics geodesic calculations and refraction
"""

import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.metrics import SK, space_type_name
from core.geodesics import compute_ray
from core.refraction import varandian_snell, critical_angle


def test_SK_euclidean():
    """Test SK function for Euclidean space"""
    r = 1.0
    K = 0.0
    result = SK(r, K)
    assert abs(result - 1.0) < 1e-10, f"SK(1, 0) should be 1.0, got {result}"
    print("SK Euclidean test passed")


def test_SK_spherical():
    """Test SK function for spherical space"""
    r = 1.0
    K = 1.0
    result = SK(r, K)
    expected = np.sin(1.0)
    assert abs(result - expected) < 1e-10, f"SK(1, 1) should be {expected}, got {result}"
    print("SK Spherical test passed")


def test_SK_hyperbolic():
    """Test SK function for hyperbolic space"""
    r = 1.0
    K = -1.0
    result = SK(r, K)
    expected = np.sinh(1.0)
    assert abs(result - expected) < 1e-10, f"SK(1, -1) should be {expected}, got {result}"
    print("SK Hyperbolic test passed")


def test_geodesic_computation():
    """Test that geodesic computation runs without errors"""
    try:
        # Test spherical
        theta, r = compute_ray(r0=0.5, theta0=0, K=1.0, C=0.3, method='numerical')
        assert len(theta) > 0, "Should return non-empty arrays"
        assert len(r) == len(theta), "Arrays should have same length"
        print(f"Geodesic computation test passed (spherical, {len(theta)} points)")
        
        # Test hyperbolic
        theta, r = compute_ray(r0=0.5, theta0=0, K=-1.0, C=0.3, method='numerical')
        assert len(theta) > 0, "Should return non-empty arrays"
        print(f"Geodesic computation test passed (hyperbolic, {len(theta)} points)")
        
    except Exception as e:
        raise AssertionError(f"Geodesic computation failed: {e}")


def test_space_names():
    """Test space type naming"""
    assert space_type_name(1.0) == "Spherical"
    assert space_type_name(0.0) == "Euclidean"
    assert space_type_name(-1.0) == "Hyperbolic"
    print("Space naming test passed")


def test_varandian_snell():
    """Test Varandian Snell's law reduces to classical Snell in Euclidean space"""
    theta1 = np.pi/4  # 45 degrees
    n1, n2 = 1.0, 1.5
    K1, K2 = 0.0, 0.0
    r = 1.0
    
    # Varandian
    theta2_varandian = varandian_snell(theta1, n1, K1, n2, K2, r)
    
    # Classical
    theta2_classical = np.arcsin(n1 * np.sin(theta1) / n2)
    
    diff = abs(theta2_varandian - theta2_classical)
    assert diff < 1e-10, f"Varandian Snell should match classical in Euclidean space, diff={diff}"
    print("Varandian Snell test passed (matches classical)")


def test_critical_angle():
    """Test critical angle computation"""
    n1, n2 = 1.5, 1.0  # Glass to air
    K1, K2 = 0.0, 0.0
    r = 1.0
    
    theta_c = critical_angle(n1, K1, n2, K2, r)
    
    # Classical critical angle
    theta_c_classical = np.arcsin(n2 / n1)
    
    diff = abs(theta_c - theta_c_classical)
    assert diff < 1e-10, f"Critical angle should match classical, diff={diff}"
    print(f"Critical angle test passed (theta_c = {np.degrees(theta_c):.2f} degrees)")


if __name__ == "__main__":
    print("Running Varandian Optics tests...\n")
    
    test_SK_euclidean()
    test_SK_spherical()
    test_SK_hyperbolic()
    test_space_names()
    test_geodesic_computation()
    test_varandian_snell()
    test_critical_angle()
    
    print("\nAll tests passed!")

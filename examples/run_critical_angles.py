import sys
import os
import numpy as np

# Ensure project root is on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core import critical_angle, SK

n1 = 1.5
n2 = 1.0
r = 1.0

pairs = [
    (0.0, 0.0, 'Euclidean -> Euclidean'),
    (1.0, 1.0, 'Spherical -> Spherical'),
    (-1.0, -1.0, 'Hyperbolic -> Hyperbolic'),
    (1.0, 0.0, 'Spherical -> Euclidean'),
    (0.0, 1.0, 'Euclidean -> Spherical'),
    (1.0, -1.0, 'Spherical -> Hyperbolic'),
    (-1.0, 1.0, 'Hyperbolic -> Spherical'),
]

print("Critical Angles for Total Internal Reflection (mixed geometries):\n")
for K1, K2, label in pairs:
    theta_c = critical_angle(n1=n1, K1=K1, n2=n2, K2=K2, r=r)
    SK1 = SK(r, K1)
    SK2 = SK(r, K2)
    ratio = (n2 * SK2) / (n1 * SK1)
    if theta_c is None:
        out = 'No critical angle (ratio >= 1)'
    else:
        out = f"{np.degrees(theta_c):.2f}°"
    print(f"{label:30s}: SK1={SK1:.4f}, SK2={SK2:.4f}, ratio={ratio:.4f} -> θc = {out}")

print("\nDone.")

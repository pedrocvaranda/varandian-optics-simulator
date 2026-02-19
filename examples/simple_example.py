#!/usr/bin/env python3
"""
Simple example of Varandian Optics simulation
No Jupyter needed - just run: python examples/simple_example.py
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import matplotlib.pyplot as plt

from core import compute_ray, space_type_name, SK
from visualization import plot_single_ray


def main():
    print("=" * 60)
    print("   VARANDIAN OPTICS - Simple Demonstration")
    print("=" * 60)
    print("\nPaper: doi.org/10.5281/zenodo.18529071\n")
    
    # Example 1: Spherical space
    print("1. Computing ray in SPHERICAL space (K = +1)...")
    K_sphere = 1.0
    r0 = 0.5
    C = 0.3
    
    theta_sphere, r_sphere = compute_ray(r0=r0, theta0=0, K=K_sphere, C=C)
    print(f"   Computed {len(theta_sphere)} points")
    print(f"   r ranges from {r_sphere.min():.3f} to {r_sphere.max():.3f}")
    
    # Example 2: Hyperbolic space
    print("\n2. Computing ray in HYPERBOLIC space (K = -1)...")
    K_hyp = -1.0
    
    theta_hyp, r_hyp = compute_ray(r0=r0, theta0=0, K=K_hyp, C=C)
    print(f"   Computed {len(theta_hyp)} points")
    print(f"   r ranges from {r_hyp.min():.3f} to {r_hyp.max():.3f}")
    
    # Example 3: Compare metric functions
    print("\n3. Comparing metric functions SK(r)...")
    r_test = 1.0
    SK_sphere_val = SK(r_test, K_sphere)
    SK_eucl_val = SK(r_test, 0.0)
    SK_hyp_val = SK(r_test, K_hyp)
    
    print(f"   SK(1.0, K=+1) = {SK_sphere_val:.4f} (Spherical)")
    print(f"   SK(1.0, K=0)  = {SK_eucl_val:.4f} (Euclidean)")
    print(f"   SK(1.0, K=-1) = {SK_hyp_val:.4f} (Hyperbolic)")
    
    # Visualization
    print("\n4. Creating visualizations...")
    
    # Plot spherical
    fig1, ax1 = plot_single_ray(theta_sphere, r_sphere, K_sphere, figsize=(8, 8))
    plt.savefig('spherical_ray.png', dpi=150, bbox_inches='tight')
    print("   Saved: spherical_ray.png")
    plt.close()
    
    # Plot hyperbolic
    fig2, ax2 = plot_single_ray(theta_hyp, r_hyp, K_hyp, figsize=(8, 8))
    plt.savefig('hyperbolic_ray.png', dpi=150, bbox_inches='tight')
    print("   Saved: hyperbolic_ray.png")
    plt.close()
    
    # Plot metric comparison
    r_range = np.linspace(0.01, 2.0, 100)
    SK_sphere_range = SK(r_range, K_sphere)
    SK_eucl_range = SK(r_range, 0.0)
    SK_hyp_range = SK(r_range, K_hyp)
    
    plt.figure(figsize=(10, 6))
    plt.plot(r_range, SK_sphere_range, 'b-', linewidth=2, label='Spherical (K=+1)')
    plt.plot(r_range, SK_eucl_range, 'g-', linewidth=2, label='Euclidean (K=0)')
    plt.plot(r_range, SK_hyp_range, 'r-', linewidth=2, label='Hyperbolic (K=-1)')
    
    plt.xlabel('r', fontsize=12)
    plt.ylabel('$S_K(r)$', fontsize=12)
    plt.title('Metric Function Comparison', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('metric_comparison.png', dpi=150, bbox_inches='tight')
    print("   Saved: metric_comparison.png")
    plt.close()
    
    print("\n" + "=" * 60)
    print("   Simulation complete!")
    print("=" * 60)
    print("\nGenerated files:")
    print("  • spherical_ray.png")
    print("  • hyperbolic_ray.png")
    print("  • metric_comparison.png")
    print("\nFor more examples, see examples/quickstart.ipynb")


if __name__ == "__main__":
    main()

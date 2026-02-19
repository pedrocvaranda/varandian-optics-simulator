# 🌌 Varandian Optics Simulator


**Interactive 2D visualization of light propagation in constant-curvature spaces**

Implementation of the theoretical framework from:
> **Varandian Optics: A Non-Euclidean Formulation of Light Propagation**  
> Pedro Coutinho Varanda  
> *Zenodo*, 2026 
> [📄 Read the paper](https://doi.org/10.5281/zenodo.18529071)

---

## 🎯 What is This?

This simulator brings to life the **Varandian Optics** framework, which extends classical geometric optics from flat (Euclidean) space to curved spaces with constant curvature.

**Key Features:**
- ✨ Simulate geodesic light ray propagation in **spherical** (K > 0) and **hyperbolic** (K < 0) spaces
- 🎨 Beautiful 2D projections: **Stereographic** (spherical) and **Poincaré disk** (hyperbolic)
- 🎮 **Interactive Jupyter notebooks** with real-time parameter control
- 📊 Compare propagation across different curvatures side-by-side
- 🧮 **Exact implementation** of equations (1)-(7) from the research paper

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/pedrocvaranda/varandian-optics-simulator.git
cd varandian-optics-simulator

# Install dependencies
pip install -r requirements.txt

# Launch Jupyter
python -m notebook examples/quickstart.ipynb
```

### Your First Ray

```python
from core import compute_ray
from visualization import plot_single_ray

# Compute ray in spherical space
theta, r = compute_ray(r0=0.5, theta0=0, K=1.0, C=0.3)

# Visualize with stereographic projection
plot_single_ray(theta, r, K=1.0)
```

---

## 📐 Theory

### The Four Laws of Varandian Optics

**Law I — Geodesic Propagation**  
Light propagates along geodesics of the curved space.

**Law II — Varandian Refraction** (Equation 6)  
Generalized Snell's law:
```
n₁ SK₁(r) sin(θ₁) = n₂ SK₂(r) sin(θ₂)
```

**Law III — Varandian Reflection**  
Reflection follows geodesic symmetry: `θᵢ = θᵣ`

**Law IV — Index-Curvature Duality** (Equation 7)  
Radial refractive index profiles can emulate curved metrics:
```
n(ρ) = 2/(1 + ρ²)   for K = +1 (spherical)
n(ρ) = 2/(1 - ρ²)   for K = -1 (hyperbolic)
```

### The Metric (Equations 1-2)

```
ds² = dr² + SK(r)² dθ²
```

where:
```
         ⎧ (1/√K) sin(√K r)      K > 0  (Spherical)
SK(r) =  ⎨ r                     K = 0  (Euclidean)
         ⎩ (1/√|K|) sinh(√|K| r) K < 0  (Hyperbolic)
```

---

## 📂 Project Structure

```
varandian-optics-simulator/
├── README.md                    # You are here
├── requirements.txt
├── INSTALL.md
├── paper/
│   ├── README.md
│   └── Varandian_Optics.pdf    # Original research paper
├── core/
│   ├── __init__.py
│   ├── metrics.py              # Equations (1)-(2): Metrics
│   ├── geodesics.py            # Equations (3)-(5): Ray propagation
│   └── refraction.py           # Equation (6): Refraction law
├── visualization/
│   ├── projections.py          # Stereographic & Poincaré projections
│   ├── plotting.py             # High-level plotting functions
│   └── __init__.py
├── git/
│   ├── .gitattributes
│   └── .gitgnore
├── examples/
│   ├── quickstart.ipynb        # 🌟 START HERE
│   ├── refraction_demo.ipynb
│   ├── simple_example.py
│   ├── run_critical_angles.py
│   └── comparison.ipynb
└── tests/
│   ├── __init__.py
    └── test_geodesics.py
```

---


## 🧪 Examples

### Example 1: Basic Ray

```python
from core import compute_ray, space_type_name
from visualization import plot_single_ray

# Parameters
r0 = 0.5      # Initial radius
K = 1.0       # Curvature (spherical)
C = 0.3       # Constant of motion

# Compute
theta, r = compute_ray(r0, theta0=0, K=K, C=C)

# Visualize
plot_single_ray(theta, r, K)
print(f"Ray in {space_type_name(K)} space")
```

### Example 2: Comparing Curvatures

```python
from visualization import plot_comparison

# Compute for different K
results = {}
for K in [-1, 0, 1]:
    _, r = compute_ray(r0=0.6, theta0=0, K=K, C=0.35)
    results[K] = r

# Compare
plot_comparison(theta, results, K_values=[-1, 0, 1])
```

### Example 3: Multiple Rays

```python
from visualization import plot_multiple_rays

rays = []
for C_val in [0.2, 0.3, 0.4, 0.5]:
    theta, r = compute_ray(r0=0.5, theta0=0, K=1.0, C=C_val)
    rays.append((theta, r, f'C={C_val}', plt.cm.viridis(C_val)))

plot_multiple_rays(rays, K=1.0)
```

---

## 👨‍🔬 About the Author

**Pedro Coutinho Varanda**

- 🥇 **#1 Brazil** - National Astronomy Olympiad (OBA 2025, Perfect Score)
- 🥈 **#2 Brazil** - OBA 2023  
- 🥉 **#3 Brazil** - OBA 2024
- 🎯 **3× Selected** - International Olympiad on Astronomy and Astrophysics (IOAA)
- 🥇 **4× Gold** - Canguru Mathematics Competition (2022-2025)

ML/AI enthusiast | Rio de Janeiro, Brazil 🇧🇷

[GitHub](https://github.com/pedrocvaranda) • [Email](mailto:pedrocvaranda@example.com)


---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🔗 Related Projects

- [Cash Allocation Model](https://github.com/pedrocvaranda/modelo_alocacao_caixa) - ML-based financial optimizer
- [Chess Trainer](https://github.com/pedrocvaranda/treinador-xadrez) - AI-powered chess learning

---

*"Remember to look up at the stars and not down at your feet."* — Stephen Hawking


[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18529071.svg)](https://doi.org/10.5281/zenodo.18529071)

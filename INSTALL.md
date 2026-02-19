# Installation Guide - Varandian Optics Simulator

## Quick Start (5 minutes)

### Step 1: Prerequisites

Make sure you have Python 3.8+ installed:

```bash
python --version  # Should be 3.8 or higher
```

### Step 2: Clone/Download

If you have the code:

```bash
cd varandian-optics-simulator
```

### Step 3: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- numpy (numerical computing)
- scipy (integration)
- matplotlib (visualization)
- jupyter (notebooks)
- ipywidgets (interactivity)
- And more...

### Step 5: Test Installation

```bash
python -m tests.test_geodesics
```

You should see:
```
SK Euclidean test passed
SK Spherical test passed  
SK Hyperbolic test passed
Space naming test passed
Geodesic computation test passed

All tests passed!
```

### Step 6: Launch Jupyter

```bash
jupyter notebook examples/quickstart.ipynb
```

Your browser will open with the interactive tutorial!

---

## Troubleshooting

### Issue: "No module named 'core'"

**Solution:** Make sure you're in the project root directory:
```bash
cd varandian-optics-simulator
python -m tests.test_geodesics
```

### Issue: "numpy not found"

**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Issue: Jupyter doesn't open

**Solution:**
```bash
pip install --upgrade jupyter
jupyter notebook
```

---

## Project Structure

```
varandian-optics-simulator/
├── core/                    # Core mathematical engine
│   ├── metrics.py          # Eq (1)-(2): SK(r) functions
│   ├── geodesics.py        # Eq (3)-(5): Ray propagation
│   └── __init__.py
│
├── visualization/          # Plotting & projections
│   ├── projections.py     # 2D projections
│   ├── plotting.py        # Plot functions
│   └── __init__.py
│
├── examples/              # Jupyter notebooks
│   ├── quickstart.ipynb   # 🌟 START HERE
│   └── comparison.ipynb   # Advanced comparisons
│
├── tests/                 # Unit tests
│   └── test_geodesics.py
│
├── paper/                 # Original research paper
├── requirements.txt       # Dependencies
└── README.md              # Documentation
```

---

## Next Steps

After installation:

1. **Run quickstart:** `jupyter notebook examples/quickstart.ipynb`
2. **Explore code:** Read through `core/metrics.py`
3. **Run tests:** `python -m tests.test_geodesics`
4. **Modify examples:** Create your own notebooks!

---

## Citation

If you use this software, please cite:

```bibtex
@software{varanda2026varandian_sim,
  author = {Varanda, Pedro Coutinho},
  title = {Varandian Optics Simulator},
  year = {2026},
  url = {https://github.com/pedrocvaranda/varandian-optics-simulator}
}
```

And the original paper:

```bibtex
@article{varanda2026varandian,
  author = {Varanda, Pedro Coutinho},
  title = {Varandian Optics: A Non-Euclidean Formulation of Light Propagation},
  year = {2026},
  doi = {10.5281/zenodo.18529071},
  url = {https://doi.org/10.5281/zenodo.18529071}
}
```

---

## Need Help?

- Read the [README.md](README.md)
- Check the [paper](https://doi.org/10.5281/zenodo.18529071)
- Open an issue on GitHub

Happy simulating!

# 🧊 `stpyvista`

Streamlit component to show PyVista 3D visualizations

## Installation instructions 

```sh
pip install stpyvista
```

## Usage instructions

<a href="https://stpyvista.streamlit.app"><img alt="Streamlit Cloud" src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg"></a>

```python
import streamlit as st
import pyvista as pv
from stpyvista import stpyvista

## Initialize a plotter object
plotter = pv.Plotter(window_size=[400,400])

## Create a mesh with a cube 
mesh = pv.Cube(center=(0,0,0))

## Add some scalar field associated to the mesh
mesh['myscalar'] = mesh.points[:, 2]*mesh.points[:, 0]

## Add mesh to the plotter
plotter.add_mesh(mesh, scalars='myscalar', cmap='bwr', line_width=1)
plotter.add_scalar_bar()

## Final touches
plotter.view_isometric()
plotter.background_color = 'white'

## Pass a key to avoid re-rendering at each time something changes in the page
stpyvista(plotter, key="pv_cube")
```
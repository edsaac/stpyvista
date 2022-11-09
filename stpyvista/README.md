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

# ipythreejs does not support scalar bars :(
pv.global_theme.show_scalar_bar = False 

## Initialize a plotter object
plotter = pv.Plotter(window_size=[400,400])

## Create a mesh with a cube 
mesh = pv.Cube(center=(0,0,0))

## Add some scalar field associated to the mesh
mesh['myscalar'] = mesh.points[:, 2]*mesh.points[:, 0]

## Add mesh to the plotter
plotter.add_mesh(mesh, scalars='myscalar', cmap='bwr', line_width=1)

## Final touches
plotter.view_isometric()
plotter.background_color = 'white'

## Pass a key to avoid re-rendering at each time something changes in the page
stpyvista(plotter, key="pv_cube")
```

## Log changes

<details>
<summary>
v 0.0.5
</summary>
- Support transparent backgrounds to blend with streamlit's web app theme.
- Add a control to spin along a certain axis the first mesh passed to the plotter.
</details>

<details>
<summary>
v 0.0.4
</summary>
- Pass a key to the stpyvista component to avoid re-rendering at every streamlit interaction
- Using ipywidgets `embed_minimal_html` directly instead of pyvista `export_html`. 
- Update examples as a multipage streamlit app
</details>
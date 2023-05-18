# 🧊 `stpyvista`
## Show PyVista 3D visualizations in Streamlit

<center>
<a href="https://stpyvista.streamlit.app"><img alt="Streamlit Cloud" src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg"></a>

<a href="https://github.com/edsaac/streamlit-PyVista-viewer"><img alt="Github Repo" src="https://img.shields.io/static/v1?label=&message=Source code&color=black&logo=github"></a> [![PyPi version](https://badgen.net/pypi/v/stpyvista/)](https://pypi.org/project/stpyvista/) <a href="https://github.com/edsaac/stpyvista-tests"><img alt="Github tests repo" src="https://img.shields.io/static/v1?label=&message=Check examples&color=black&logo=github"></a>

![howto-stpyvista|508x500, 100%](assets/stpyvista_intro.gif)

</center>

This is a simple component that takes a PyVista plotter object and shows it on Streamlit as an interactive element (as in it can be zoomed in/out, moved and rotated, but the visualization state is not returned). It uses PyVista's [panel backend](https://docs.pyvista.org/user-guide/jupyter/panel.html) and it basically takes the plotter, [exports it to HTML](https://docs.pyvista.org/api/plotting/_autosummary/pyvista.Plotter.export_html.html) and displays that within an iframe.

> ⚠️ `panel` and `pythreejs` as pyvista backends were deprecated in favor of `trame`. 


******
## Installation 

```sh
pip install stpyvista
```
************
## Docs and examples

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://stpyvista.streamlit.app/)

******

## Basic example:

```python
import streamlit as st
import pyvista as pv
from stpyvista import stpyvista

# pythreejs does not support scalar bars :(
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
plotter.add_scalar_bar()
plotter.background_color = 'white'

## Pass a key to avoid re-rendering at each time something changes in the page
stpyvista(plotter, key="pv_cube")
```

****

#### Also check:
* The PyVista project at [https://www.pyvista.org/](https://www.pyvista.org/)
* @blackary['s blog post](https://blog.streamlit.io/how-to-build-your-own-streamlit-component/) on how to build a custom component

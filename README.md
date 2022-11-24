# 🧊 `stpyvista`: Show PyVista 3D visualizations in Streamlit

<p align=center>💾 <strong>Source code repository</strong> 💾</p>

<center>
<a href="https://stpyvista.streamlit.app"><img alt="Streamlit Cloud" src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg"></a>

<a href="https://github.com/edsaac/streamlit-PyVista-viewer"><img alt="Github Repo" src="https://img.shields.io/static/v1?label=&message=Source code&color=black&logo=github"></a> [![PyPi version](https://badgen.net/pypi/v/stpyvista/)](https://pypi.org/project/stpyvista/) <a href="https://github.com/edsaac/stpyvista-tests"><img alt="Github tests repo" src="https://img.shields.io/static/v1?label=&message=Check examples&color=black&logo=github"></a>
</center>

![howto-stpyvista|600x340](https://aws1.discourse-cdn.com/business7/uploads/streamlit/original/3X/f/d/fdcb8cb7be524e4c8d1e45e9371cc6b17a732b24.gif)

This is a simple component that takes a PyVista plotter object and shows it on Streamlit as an interactive element (as in it can be zoomed in/out, moved and rotated, but the visualization state is not returned). It uses PyVista's [pythreejs backend](https://docs.pyvista.org/user-guide/jupyter/pythreejs.html) and it basically takes the plotter, [exports it to HTML](https://docs.pyvista.org/api/plotting/_autosummary/pyvista.Plotter.export_html.html) and displays that within an iframe.

## Installation 

```sh
pip install stpyvista
```

## Demos 

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://stpyvista.streamlit.app/)

📤 Display your own STL file on Streamlit

![textures-stpyvista|508x500, 85%](https://aws1.discourse-cdn.com/business7/uploads/streamlit/original/3X/e/6/e64c7054ffadafee7c8ad66e5a2dfc5b0f702cbd.gif)

🍞 Physically Based Rendering (PBR) 

![textures-stpyvista|508x500, 85%](https://aws1.discourse-cdn.com/business7/uploads/streamlit/original/3X/8/d/8dd4a20952a798c917180ec187edaac77a766cee.gif)

******

## Usage example:

```python
import pyvista as pv
import streamlit as st
from stpyvista import stpyvista

# pythreejs does not support scalar bars :(
pv.global_theme.show_scalar_bar = False

st.title("A cube")
st.info("""Code adapted from https://docs.pyvista.org/user-guide/jupyter/pythreejs.html#scalars-support""")

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

## Send to streamlit
stpyvista(plotter, key="pv_cube")

```
> Result: 
>
> ![image|589x500, 50%](https://aws1.discourse-cdn.com/business7/uploads/streamlit/original/3X/8/e/8e77cf6a5d7b102c8aae79db3ad0ad2272d10b5b.png)

****

#### Also check:
* The PyVista project at [https://www.pyvista.org/](https://www.pyvista.org/)
* @blackary['s blog post](https://blog.streamlit.io/how-to-build-your-own-streamlit-component/) on how to build a custom component

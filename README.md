<h1 align="center">
  <b>🧊 <code>stpyvista</code></b>
</h1>

<h3 align="center">
  Show <a href="https://docs.pyvista.org/index.html">PyVista</a> visualizations in Streamlit.
</h3>

<p align="center">
<a href="https://stpyvista.streamlit.app"><img alt="Streamlit Cloud" src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg"></a>
</p>
<p align="center">
<a href="https://github.com/edsaac/stpyvista"><img alt="Github Repo" src="https://img.shields.io/static/v1?label=&message=Source code&color=black&logo=github"></a> 
<a href="https://pypi.org/project/stpyvista/"><img alt="Check it at PyPI" src="https://badgen.net/pypi/v/stpyvista/">
<a href="https://github.com/edsaac/stpyvista-tests"><img alt="Github tests repo" src="https://img.shields.io/static/v1?label=&message=Check examples&color=black&logo=github"></a>
</p>
<p align="center">
<a href="https://stpyvista.streamlit.app"><img alt="Streamlit Cloud" src="assets/stpyvista_intro_crop.gif" width="400"></a>
</p>

This component takes a PyVista plotter object and shows it on Streamlit as an interactive element (as in it can be zoomed in/out, moved and rotated, but the visualization state is not returned). It uses [Panel](https://panel.holoviz.org/reference/panes/VTK.html#working-with-pyvista) to render PyVista plotter objects within an iframe.

******
### 📦 Installation 

```sh
pip install stpyvista
```

******

### 📚 Demo and documentation 

[https://stpyvista.streamlit.app](https://stpyvista.streamlit.app)

******

### ✨ Minimal example
<details>
<summary>
<b>Render a cube</b>
</summary>
  
```python
import streamlit as st
import pyvista as pv
from stpyvista import stpyvista

## Initialize a plotter object
plotter = pv.Plotter(window_size=[400,400])

## Create a mesh with a cube 
mesh = pv.Cube(center=(0,0,0))

## Add some scalar field associated to the mesh
mesh['my_scalar'] = mesh.points[:, 2] * mesh.points[:, 0]

## Add mesh to the plotter
plotter.add_mesh(mesh, scalars='my_scalar', cmap='bwr')

## Final touches
plotter.view_isometric()
plotter.add_scalar_bar()
plotter.background_color = 'white'

## Pass a key to avoid re-rendering at each page change
stpyvista(plotter, key="pv_cube")

```
</details>

****

### 🎈 Deploying to Streamlit Community Cloud

- Add `stpyvista` to the `requirements.txt` file.
- Install `procps`, `libgl1-mesa-glx` and `xvfb` by adding them to the `packages.txt` file.
- By default, Community Cloud will run Python 3.8, make sure to deploy using Python 3.10 or 3.11 (New App → Advanced settings... → Python version)

****

### 🚩 Known issues

- [`NSInternalInconsistencyException`](https://github.com/edsaac/stpyvista/issues/14) thrown when running on macOS. Current solution is to deploy using a VM.
- [`RuntimeError`](https://github.com/edsaac/stpyvista/issues/17) thrown when running Python 3.9. Current solution is to run with Python 3.10 or higher. 

****

### 🍏 Also check
* The PyVista project at [https://www.pyvista.org/](https://www.pyvista.org/)
* Working with Panel and Pyvista [https://panel.holoviz.org](https://panel.holoviz.org/reference/panes/VTK.html#working-with-pyvista)
* @blackary['s blog post](https://blog.streamlit.io/how-to-build-your-own-streamlit-component/) on how to build a custom component
* Other stuff from me on [https://edsaac.github.io](https://edsaac.github.io)

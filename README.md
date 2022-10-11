# stpyvista

Streamlit component that allows you to show PyVista 3d visualizations

## Installation instructions 

```sh
pip install stpyvista
```

## Usage instructions

```python
import pyvista as pv
import streamlit as st
from stpyvista import stpyvista, HTML_stpyvista

plotter = pv.Plotter()

# Store the 3D visualization in a sessions state variable
# to avoid re-rendering each time streamlit reruns the script

if "model" not in st.session.state:
    plotter = pv.Plotter()
    st.session.state.model = HTML_stpyvista(plotter)

stpyvista(st.session.state.model)
```
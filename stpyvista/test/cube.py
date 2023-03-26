import streamlit as st
import pyvista as pv
from stpyvista import stpyvista

st.set_page_config(page_icon="🧊", layout="wide")
st.title("🧊 `stpyvista`")
st.sidebar.header("Show PyVista 3D visualizations in Streamlit")

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
plotter.background_color = 'white'

## Pass a key to avoid re-rendering at each time something changes in the page
stpyvista(plotter, key="pv_cube")
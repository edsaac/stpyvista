import streamlit as st
import pyvista as pv
from stpyvista import stpyvista

st.set_page_config(page_icon="🧊", layout="wide")
st.title("🧊 `stpyvista`")
st.sidebar.header("Show PyVista 3D visualizations in Streamlit")

## Initialize a plotter object
plotter = pv.Plotter(window_size=[500,400])

## Create a mesh with a cube 
mesh = pv.Cube(center=(0,0,0))

## Add some scalar field associated to the mesh
mesh['myscalar'] = mesh.points[:, 2]*mesh.points[:, 0]
mesh['otherscalar'] = mesh.points[:, 2]**2 + mesh.points[:, 0]
mesh.set_active_scalars('otherscalar')

## Add mesh to the plotter
plotter.add_mesh(mesh, cmap='bwr', line_width=1,  label="cube")
plotter.add_scalar_bar()
plotter.add_title("My cube", color="black", font_size=14)

## Final touches
plotter.view_isometric()
plotter.background_color = 'lightgray'

chk = st.sidebar.checkbox("use_container_width", False)
align = st.sidebar.select_slider("align", ["left", "center", "right"])

## Pass a key to avoid re-rendering at each time something changes in the page
stpyvista(
    plotter, 
    use_container_width=chk, 
    panel_kwargs=dict(orientation_widget = True),
    horizontal_align=align
)

## Add something else below
st.markdown("Jello there"*50)

cols = st.columns([1,2,1], gap="small")

for col in cols:
    with col:
        stpyvista(plotter, use_container_width=chk, bokeh_resources="CDN")
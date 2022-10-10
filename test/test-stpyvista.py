import pyvista as pv
import streamlit as st
from stpyvista import stpyvista, HTML_stpyvista

# Storing the threejs models as a session_state variable
# allows to avoid rerendering at each time something changes
# in the page
if "carburator" not in st.session_state:
    pl = pv.Plotter(window_size=[400,300])
    mesh = pv.examples.download_carburator()
    pl.set_background('white')
    mesh.decimate(0.5, inplace=True)
    pl.add_mesh(mesh, color='lightgrey', pbr=True, metallic=0.5)
    pl.camera.zoom(2.0)
    st.session_state.carburator = HTML_stpyvista(pl)

if "sphere" not in st.session_state:
    pl = pv.Plotter(window_size=[300,200])
    pl.set_background('#D3EEFF')
    pl.add_mesh(pv.Sphere(center=(1, 0, 1)))
    st.session_state.sphere = HTML_stpyvista(pl)

sphere = st.session_state.sphere
carburator = st.session_state.carburator

cols = st.columns([1,1.5])

with cols[0]: 
    st.title("Component `stpyvista`")
    st.write("Show [**pyvista**](https://www.pyvista.org/) 3D visualizations in streamlit")
with cols[1]: stpyvista(carburator)

st.header("Different horizontal alignment")

with st.echo():
    # The default is centered
    stpyvista(sphere)

with st.echo():
    # It can also go to the left
    stpyvista(sphere, horizontal_align="left")

with st.echo():
    # Or to the right
    stpyvista(sphere, horizontal_align="right")
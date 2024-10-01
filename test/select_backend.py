import pyvista as pv
import streamlit as st

backend = st.selectbox("Backend", ["panel", "trame"])

if backend == "panel":
    from stpyvista.panel_backend import stpyvista
elif backend == "trame":
    from stpyvista.trame_backend import stpyvista


st.title("🧊 `stpyvista`")
st.header("Show PyVista 3D visualizations in Streamlit")

## Initialize a plotter object
plotter = pv.Plotter(window_size=[200, 200])

## Create a mesh with a cube
mesh = pv.Cube(center=(0, 0, 0))

## Add some scalar field associated to the mesh
mesh["myscalar"] = mesh.points[:, 2] * mesh.points[:, 0]
mesh["otherscalar"] = mesh.points[:, 2] ** 2 + mesh.points[:, 0]
mesh.set_active_scalars("otherscalar")

## Add mesh to the plotter
plotter.add_mesh(mesh, cmap="bwr", line_width=1, label="cube")
plotter.add_title("My cube", color="black", font_size=14)

## Final touches
plotter.view_isometric()
plotter.background_color = "red"

stpyvista(plotter, key="my_plot")

if st.checkbox("Do something"):
    st.write("Hello")

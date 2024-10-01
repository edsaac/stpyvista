import pyvista as pv
import streamlit as st
from stpyvista.panel_backend import stpyvista as stpv_panel
from stpyvista.trame_backend import stpyvista as stpv_trame

st.title("🧊 `stpyvista`")
st.subheader("Show PyVista 3D visualizations in Streamlit")

## Initialize a plotter object
plotter = pv.Plotter(window_size=[350, 350])

## Create a mesh with a sphere
mesh = pv.Sphere(radius=1.0, center=(0, 0, 0))

## Add some scalar field associated to the mesh
x, y, z = mesh.cell_centers().points.T
mesh["My scalar"] = z
mesh.set_active_scalars("My scalar")

## Add mesh to the plotter
plotter.add_mesh(
    mesh,
    scalars="My scalar",
    cmap="prism",
    show_edges=True,
    edge_color="#001100",
    ambient=0.2,
    show_scalar_bar=True,
)

## Final touches
plotter.add_title("My Sphere", color="black", font_size=14)
plotter.view_isometric()
plotter.background_color = "#dddddd"

cols = st.columns(2, vertical_alignment="center")
with cols[0]:
    st.write("**Using Panel (default)**")
    stpv_panel(plotter, key="stpv_panel")

with cols[1]:
    st.write("**Using Trame**")
    stpv_trame(plotter, key="stpv_trame")

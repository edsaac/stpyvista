import streamlit as st
import pyvista as pv
from stpyvista import stpyvista

st.set_page_config(page_icon="🧊", layout="wide")

st.title("🧊 `stpyvista`")
st.sidebar.header("Show PyVista 3D visualizations in Streamlit")
backend = st.sidebar.radio("Select backend", ["panel", "trame_html", "trame"], index=0)
st.sidebar.divider()


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
plotter.background_color = "lightgray"

cols = st.columns(2)

with cols[0]:
    stpyvista(
        plotter,
        backend="panel",
        backend_kwargs=dict(orientation_widget=True),
        key="cube_panel",
    )

with cols[1]:
    stpyvista(
        plotter,
        backend="trame",
        key="cube_trame",
    )

## Add something else below
st.markdown("hello there 🍒 " * 50)

# cols = st.columns([1, 2, 1], gap="small")

# for i, col in enumerate(cols):
#     with col:
#         stpyvista(plotter, use_container_width=chk, key=f"cube_{i}_{chk}")

# stpyvista(plotter, use_container_width=chk)
# print(hash(plotter))

st.sidebar.button("Rerun")

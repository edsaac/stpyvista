import streamlit as st
import pyvista as pv
from stpyvista import experimental_vtkjs
from threading import Thread
import signal

st.set_page_config(page_icon="🧊", layout="wide")
st.title("🧊 `stpyvista`")
st.sidebar.header("Show PyVista 3D visualizations in Streamlit")

signal.set_wakeup_fd(0)

def create_plotter_vtksz():
    # Initialize a plotter object
    plotter = pv.Plotter(window_size=[400, 400])
    mesh = pv.Sphere(radius=1.0, center=(0, 0, 0))
    x, y, z = mesh.cell_centers().points.T
    mesh["My scalar"] = z

    ## Add mesh to the plotter
    plotter.add_mesh(
        mesh,
        scalars="My scalar",
        cmap="prism",
        show_edges=True,
        edge_color="#001100",
        ambient=0.2,
    )

    ## Some final touches
    plotter.background_color = "white"
    plotter.view_isometric()

    plotter.export_vtksz("test1.zip")

## Pass a key to avoid re-rendering at each time something changes in the page
@st.cache_data
def get_plotter_vtksz(fname= "test.zip"): 
    with open(fname, 'rb') as f:
        data = f.read()
    return data


data = get_plotter_vtksz()

with st.form("3D window"):
    camera = experimental_vtkjs(data)
    submit = st.form_submit_button("Capture camera")

if submit:
    st.json(camera)

if st.button("Generate"):
    create_plotter_vtksz()
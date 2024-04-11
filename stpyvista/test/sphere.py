import streamlit as st
import pyvista as pv
from pyvista.plotting import Plotter

from stpyvista import experimental_vtkjs
from stpyvista.export import export_vtksz
import asyncio

@st.cache_resource
def create_plotter(dummy:str = "sphere"):
    
    # Initialize a plotter object
    plotter = pv.Plotter()
    mesh = pv.Sphere(radius=1.0, center=(0, 0, 0))
    mesh2 = pv.Sphere(radius=0.3, center=(1.1, 1.1, 0.8))
    
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
        show_scalar_bar = False
    )

    actor = plotter.add_mesh(mesh2, name="small_sphere")

    ## Some final touches
    plotter.background_color = "pink"
    plotter.view_isometric()
    
    # Add events
    def callback(step):
        actor.position = [step / 100.0, step / 100.0, 0]
    plotter.add_timer_event(
        max_steps=200, duration=500, callback=callback
    )
    return plotter

async def main():

    st.set_page_config(page_icon="🧊", layout="wide")
    st.title("🧊 `stpyvista`")
    st.write("*Show PyVista 3D visualizations in Streamlit*")
    
    plotter = create_plotter()

    if "data" not in st.session_state:
        st.session_state.data = await export_vtksz(plotter)
    
    lcol, rcol = st.columns(2)
    with rcol:
        "🌎 3D Model"
        camera = experimental_vtkjs(st.session_state.data)#, key="experimental-stpv")
        
    with lcol:
        "🎥 Camera"
        st.json(camera)

if __name__ == "__main__":
    asyncio.run(main())
import streamlit as st
import pyvista as pv
from stpyvista import experimental_vtkjs
from stpyvista.export import export_vtksz
import asyncio

@st.cache_resource
def create_plotter(dummy:str = "sphere"):
    
    # Initialize a plotter object
    plotter = pv.Plotter(window_size=[400, 400])
    mesh = pv.Sphere(radius=1.0, center=(0, 0, 0))
    x, y, z = mesh.cell_centers().points.T
    mesh["My scalar"] = z

    # Scalar bar configuration
    scalar_bar_kwargs = dict(
        font_family='arial',
        interactive=True,
        position_x = 0.05,
        position_y = 0.05,
        vertical=False
    )

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

    ## Some final touches
    plotter.background_color = "pink"
    plotter.view_isometric()

    return plotter

async def main():

    st.set_page_config(page_icon="🧊", layout="wide")
    st.title("🧊 `stpyvista`")
    st.sidebar.header("Show PyVista 3D visualizations in Streamlit")
    
    plotter = create_plotter()

    if "data" not in st.session_state:
        st.session_state.data = await export_vtksz(plotter)

    camera = experimental_vtkjs(st.session_state.data, key="view")
    st.sidebar.json(camera)

if __name__ == "__main__":
    asyncio.run(main())
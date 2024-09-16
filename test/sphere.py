import asyncio
import streamlit as st
import pyvista as pv

from stpyvista import experimental_vtkjs
from stpyvista.export import export_vtksz


@st.cache_resource
def create_plotter(dummy: str = "sphere"):
    # Initialize a plotter object
    plotter = pv.Plotter()
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
        show_scalar_bar=False,
    )

    ## Some final touches
    plotter.view_isometric()
    plotter.background_color = "pink"

    return plotter


async def main():
    st.set_page_config(page_icon="🧊", layout="wide")
    st.title("🧊 `stpyvista`")
    st.write("*Show PyVista 3D visualizations in Streamlit*")

    plotter = create_plotter()

    if "data" not in st.session_state:
        st.session_state.data = await export_vtksz(plotter)

    lcol, rcol = st.columns([2, 1])
    with lcol:
        with st.form("experimental_vtkjs"):
            "🌎 3D Model"
            camera = experimental_vtkjs(st.session_state.data, key="experimental-stpv")
            grab_camera = st.form_submit_button(":camera: Grab view state")

    with rcol:
        "🎥 Camera"
        if grab_camera:
            st.json(camera)
        else:
            st.info("Click the button to grab the view state")


if __name__ == "__main__":
    asyncio.run(main())

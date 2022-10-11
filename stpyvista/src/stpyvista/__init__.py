# __init__.py

from pathlib import Path
from typing import Optional

import streamlit as st
import streamlit.components.v1 as components

import pyvista as pv
pv.set_jupyter_backend('pythreejs')

from io import StringIO

# Tell streamlit that there is a component called stpyvista,
# and that the code to display that component is in the "frontend" folder
frontend_dir = (Path(__file__).parent / "frontend").absolute()

_component_func = components.declare_component(
	"stpyvista", 
    path=str(frontend_dir)
)

class HTML_stpyvista:
    """
    Receives a pyvista Plotter object and builds an HTML model
    using pythreejs. This takes care of temporal files needed to 
    dump the generated HTML and store the dimensions to render the 
    iframe in the frontend

    Usage
    ----------
    model = HTML_stpyvista(plotter)
    
    plotter: pv.Plotter
        Plotter to export to html
    
    """
    def __init__(self, plotter:pv.Plotter) -> None:
        model_html = StringIO()
        plotter.export_html(model_html, backend='pythreejs')
        threejs_html = model_html.getvalue()
        model_html.close()
        dimensions = plotter.window_size

        self.threejs_html = threejs_html
        self.window_dimensions = dimensions

# Create the python function that will be called from the front ende
def stpyvista(
    input : HTML_stpyvista,
    horizontal_align : str = "center",
    key: Optional[str] = None
) -> None:
    """
    Renders a HTML_stpyvista as a threejs model.
    
    Parameters
    ----------
    processed: dict
        Plotter to render
    
    key: str|None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.
    
    Returns
    -------
    None
    """
    component_value = _component_func(
        threejs_html = input.threejs_html,
        width = input.window_dimensions[0],
        height = input.window_dimensions[1],
        horizontal_align = horizontal_align,
        key = key,
        default = 0
    )

    return component_value

def main():

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
    
if __name__ == "__main__":
    main()

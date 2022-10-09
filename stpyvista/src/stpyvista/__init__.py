from pathlib import Path
from turtle import window_height, window_width
from typing import Optional

import streamlit as st
import streamlit.components.v1 as components

import pyvista as pv
import io
import os

## Using pythreejs as pyvista backend
pv.set_jupyter_backend('pythreejs')

# Tell streamlit that there is a component called stpyvista,
# and that the code to display that component is in the "frontend" folder
frontend_dir = (Path(__file__).parent / "frontend").absolute()

_component_func = components.declare_component(
	"stpyvista", 
    path=str(frontend_dir)
)

# Create the python function that will be called
def stpyvista(
    plotter : pv.Plotter,
    key: Optional[str] = None,
):
    """
    Renders a pyvista Plotter object
    
    Parameters
    ----------
    plotter: pyvista.Plotter
        Plotter to render
    
    key: str|None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.
    
    Returns
    -------
    None
    """

    model_html = io.StringIO()
    plotter.export_html(model_html, backend='pythreejs')
    parsed_html = model_html.getvalue()
    model_html.close()
    
    window_width, window_height = plotter.window_size
    print(window_width is plotter.window_size[0])
    print(window_height)

    component_value = _component_func(
        value = parsed_html,
        width = window_width,
        height = window_height,
        key = key
    )

    return component_value

def main():

    st.title("Component `stpyvista`")
    
    path_to_stl = "../../../onewaywrap/assets/ToolHolder.STL"
    if os.path.exists(path_to_stl):

        ## Initialize pyvista reader and plotter
        plotter = pv.Plotter(border=True, window_size=[600,400]) 
        plotter.set_background('white', top='black')

        ## Color panel
        color_stl = st.color_picker("Element","#0BD88D")

        ## Initialize pyvista reader and plotter
        reader = pv.STLReader(path_to_stl)
        mesh = reader.read()
        plotter.add_mesh(mesh, color=color_stl, texture="wood")

        stpyvista(plotter)

        st.header("Hello Again")
        st.button("Hey")
    else:
        st.error("fix path")


if __name__ == "__main__":
    main()

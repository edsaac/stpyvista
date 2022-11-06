# __init__.py

from pathlib import Path
from typing import Optional

import streamlit as st
import streamlit.components.v1 as components

import pyvista as pv
pv.set_jupyter_backend('pythreejs')

from io import StringIO
from ipywidgets.embed import embed_minimal_html

# Tell streamlit that there is a component called stpyvista,
# and that the code to display that component is in the "frontend" folder
frontend_dir = (Path(__file__).parent / "frontend").absolute()

_component_func = components.declare_component(
	"stpyvista", 
    path=str(frontend_dir)
)

class stpyvistaTypeError(TypeError):
    """ Unsupported format for input? """
    pass

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
        pv_to_tjs = plotter.to_pythreejs()
        embed_minimal_html(model_html, pv_to_tjs, title="🧊-stpyvista")
        threejs_html = model_html.getvalue()
        model_html.close()
        dimensions = plotter.window_size

        self.threejs_html = threejs_html
        self.window_dimensions = dimensions

# Create the python function that will be called from the front end
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

    if isinstance(input, pv.Plotter):
        input = HTML_stpyvista(input)
    elif isinstance(input, HTML_stpyvista):
        pass
    else:
        raise(stpyvistaTypeError)

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
    pass
    
if __name__ == "__main__":
    main()

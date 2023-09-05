# __init__.py

from pathlib import Path
from typing import Optional, Union

import streamlit as st
import streamlit.components.v1 as components

import pyvista as pv
pv.set_jupyter_backend('static')

#from tempfile import NamedTemporaryFile
from io import BytesIO

import panel as pn
pn.extension('vtk')
from bokeh.resources import INLINE

# Tell streamlit that there is a component called stpyvista,
# and that the code to display that component is in the "frontend" folder
frontend_dir = (Path(__file__).parent / "frontend").absolute()

_component_func = components.declare_component(
	"stpyvista", 
    path=str(frontend_dir)
)

class stpyvistaTypeError(TypeError):
    """ Unsupported format for input"""
    pass

# Create the python function that will be called from the front end
def stpyvista(
    plotter : pv.Plotter,
    horizontal_align : str = "center",
    panel_kwargs = None,
    key: Optional[str] = None
    ) -> None:

    """
    Renders a HTML_stpyvista as a threejs model.
    
    Parameters
    ----------
    input: Union[pv.Plotter, HTML_stpyvista]
        Plotter to render
    
    horizontal_align: str = "center"
        Either "center", "left" or "right"

    panel_kwargs: dict | None
        Optional keyword parameters to pass to pn.panel() Check: 
        https://panel.holoviz.org/api/panel.pane.vtk.html for details. Here is
        a useful one:
        
        orientation_widget: bool
            Show the xyz axis indicator


    key: str|None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.
    
    Returns
    -------
    None
    """

    if isinstance(plotter, pv.Plotter): 

        if panel_kwargs is None:
            panel_kwargs = dict()
        
        width, height = plotter.window_size
        geo_pan_pv = pn.panel(
            plotter.ren_win, 
            width = width, 
            height = height,
            **panel_kwargs) 
        
        # Create HTML file
        model_bytes = BytesIO()
        geo_pan_pv.save(model_bytes, resources=INLINE)
        panel_html = model_bytes.getvalue().decode('utf-8')
        model_bytes.close()

        component_value = _component_func(
            panel_html = panel_html,
            width = width,
            height = height,
            horizontal_align = horizontal_align,
            key = key,
            default = 0)

        return component_value

    else: 
        raise(stpyvistaTypeError)

def main():
    pass

if __name__ == "__main__":
    main()

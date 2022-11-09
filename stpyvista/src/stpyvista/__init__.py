# __init__.py

from pathlib import Path
from typing import Optional, Union

import streamlit as st
import streamlit.components.v1 as components

import pyvista as pv
pv.set_jupyter_backend('pythreejs')

from io import StringIO
from ipywidgets.embed import embed_minimal_html

import pythreejs as tjs

# Tell streamlit that there is a component called stpyvista,
# and that the code to display that component is in the "frontend" folder
frontend_dir = (Path(__file__).parent / "frontend").absolute()

_component_func = components.declare_component(
	"stpyvista", 
    path=str(frontend_dir)
)

def get_Meshes(renderer: tjs.Renderer) -> list[tjs.Mesh]:
    return [child for child in renderer._trait_values["scene"].children if isinstance(child, tjs.Mesh)]

def spin_element_on_axis(renderer: tjs.Renderer, axis:str = "z", revolution_time:float = 4.0):
    
    ## Makes a full spin in a second
    spin_track = tjs.NumberKeyframeTrack(name=f'.rotation[{axis}]', times=[0, revolution_time], values=[0, 6.28])
    spin_clip = tjs.AnimationClip(tracks=[spin_track])
    
    ## Animate all meshes in scene
    ## This adds a separate control to all the meshes 
    ## Need to implement this as a tjs.AnimationObjectGroup in the AnimationMixer, 
    ## but that is not implemented pythreejs: https://github.com/jupyter-widgets/pythreejs/issues/372
    # spin_action = [tjs.AnimationAction(tjs.AnimationMixer(mesh), spin_clip, mesh) for mesh in get_Meshes(renderer)]

    # This adds controls for only the firts mesh in the plotter
    mesh = get_Meshes(renderer)[0]
    spin_action = [tjs.AnimationAction(tjs.AnimationMixer(mesh), spin_clip, mesh)]
    return spin_action

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

    rotation: dict{"axis":'z', "revolution_time":float}

    transparent_background: bool 
    
    """
    def __init__(
        self, 
        plotter:pv.Plotter, 
        rotation:dict = None, 
        opacity_background:float = 0.0) -> None:
        
        model_html = StringIO()
        pv_to_tjs = plotter.to_pythreejs()

        ## Animation controls        
        animations = []
        if rotation:
            animations = spin_element_on_axis(pv_to_tjs, **rotation)
        else:
            pass
        
        # Build transparent background
        ## Remove background
        pv_to_tjs._trait_values["scene"].background = None
        
        ## Support transparency
        pv_to_tjs._alpha = True

        ## Retrieve intended color from pv.Plotter
        pv_to_tjs.clearColor = plotter.background_color.hex_rgb
        
        ## Assign alpha
        pv_to_tjs.clearOpacity = opacity_background

        # Create HTML file
        embed_minimal_html(model_html, [pv_to_tjs, *animations], title="🧊-stpyvista")
        threejs_html = model_html.getvalue()
        model_html.close()

        dimensions = plotter.window_size
        self.threejs_html = threejs_html
        self.window_dimensions = dimensions

# Create the python function that will be called from the front end
def stpyvista(
    input : Union[pv.Plotter, HTML_stpyvista],
    horizontal_align : str = "center",
    rotation : Union[bool, dict] = None,
    opacity_background : float = 0.0,
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

    rotation: dict = None
        [Experimental]. Add a play button to spin the mesh along an axis. 
        If not False, expects a dictionary with keys {"axis": "z", "revolution_time":5}.
        >> It only works for a single mesh, as it rotates the mesh rather than moving the camera
        >> Also, edges are left behind - a lot to fix
    
    opacity_background: float = 0.0
        [Experimental]. Ignore background color.

    key: str|None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.
    
    Returns
    -------
    None
    """

    if isinstance(input, pv.Plotter): 
        input = HTML_stpyvista(
            input, 
            rotation=rotation, 
            opacity_background=opacity_background)
    elif isinstance(input, HTML_stpyvista): pass
    else: raise(stpyvistaTypeError)

    if rotation: has_controls = 1.0
    else: has_controls = 0.0

    component_value = _component_func(
        threejs_html = input.threejs_html,
        width = input.window_dimensions[0],
        height = input.window_dimensions[1],
        horizontal_align = horizontal_align,
        has_controls = has_controls,
        key = key,
        default = 0)

    return component_value

def main():
    pass

if __name__ == "__main__":
    main()

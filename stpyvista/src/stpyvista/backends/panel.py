from typing import Optional, Literal
from io import BytesIO
import panel as pn
from bokeh.resources import CDN, INLINE
import pyvista as pv

from ..errors import *

pn.extension("vtk", sizing_mode="stretch_width")
BOKEH_RESOURCES = {"CDN": CDN, "INLINE": INLINE}

def prerender(
    plotter: pv.Plotter,
    **backend_options
) -> None:
    
    panel_kwargs = backend_options.get("panel_html", None)

    if panel_kwargs is None:
        panel_kwargs = dict()

    width, height = plotter.window_size

    if backend_options.get("use_container_width", False):
        geo_pan_pv = pn.panel(plotter.ren_win, height=height, **panel_kwargs)
    else:
        geo_pan_pv = pn.panel(
            plotter.ren_win, height=height, width=width, **panel_kwargs
        )
    
    # Check bokeh_resources
    bokeh_resources = backend_options.get("bokeh_resources", "INLINE")
    if not bokeh_resources in ("CDN", "INLINE"):
        raise stpyvistaTypeError(
            f'"{bokeh_resources}" is not a valid resource. '
            'Valid bokeh resource options are "CDN" or "INLINE".'
        )
        
    # Create HTML file
    model_bytes = BytesIO()
    geo_pan_pv.save(
        model_bytes, 
        resources=BOKEH_RESOURCES[bokeh_resources]
    )
    panel_html = model_bytes.getvalue().decode("utf-8")
    model_bytes.close()
    
    return panel_html
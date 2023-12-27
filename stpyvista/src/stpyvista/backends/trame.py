from typing import Optional, Literal
import pyvista as pv
from ..errors import *

def prerender(
    plotter: pv.Plotter,
    **backend_options
) -> None:
   
    width, height = plotter.window_size

    if backend_options.get("use_container_width", False):
        width = "100%"

    # Create HTML file
    trame_html = pv.trame.jupyter.EmbeddableWidget(plotter, width, height).value
    # trame_html = plotter.export_html(filename=None)

    return trame_html
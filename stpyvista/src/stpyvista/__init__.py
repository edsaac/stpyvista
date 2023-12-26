# __init__.py

from pathlib import Path
import streamlit.components.v1 as components
import pyvista as pv
from typing import Optional, Literal
from .errors import *

# Tell streamlit that there is a component called stpyvista,
# and that the code to display that component is in the "frontend" folder
frontend_dir = (Path(__file__).parent / "frontend").absolute()
_component_func = components.declare_component("stpyvista", path=str(frontend_dir))

STPYVISTA_BACKEND = "panel"

def set_backend(backend: Literal["trame", "panel"]):
    global STPYVISTA_BACKEND

    if backend not in ("trame", "panel"):
        raise stpyvistaValueError(
            f"{backend} not a valid backend. "
            "Valid backends are `panel` and `trame`"
        )
    else:
        STPYVISTA_BACKEND = backend

###############
        
def stpyvista(
        plotter: pv.Plotter,
        key: Optional[str] = None,
        use_container_width: bool = True,
        horizontal_align: Literal["center", "left", "right"] = "center",
        **backend_options,
    ):
    """
    Renders an interactive pyvisya Plotter in streamlit.
    
    Parameters
    ----------
    plotter: pv.Plotter
        Pyvista plotter object to render.
    
    key: str|None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    use_container_width : bool = True
        If True, set the dataframe width to the width of the parent container. \
        This takes precedence over the `horizontal_align` argument. \
        Defaults to `True`.
    
    horizontal_align : Literal["center", "left", "right"] = "center"
        Horizontal alignment of the stpyvista component. This parameter is ignored if 
        `use_container_width = True`. Defaluts to `"center"`.

    *If using the **panel** backend*:

    panel_kwargs : dict | None = None
        Optional keyword parameters to pass to pn.panel(). 
        Check: https://panel.holoviz.org/api/panel.pane.vtk.html 
        for more details. Here is an useful one:
        
        orientation_widget : bool
            Show the xyz axis indicator

    bokeh_resources: Literal["CDN", "INLINE"] = "Inline"
        Source of the BokehJS configuration. Check:
        https://docs.bokeh.org/en/latest/docs/reference/resources.html for details. \
        Defaults to "INLINE" 

    *If using the **trame** backend*:

    
    Returns
    -------
    None

    """

    if not isinstance(plotter, pv.Plotter):
        raise stpyvistaTypeError(
            f'{plotter} is not a `pv.Plotter` instance. '
        ) 

    else:

        width, height = plotter.window_size

        if use_container_width:
            width = "100%"

        if backend_options is None:
            backend_options = {}
        
        backend_options.update(
            {"use_container_width": use_container_width}
        )
        
        if STPYVISTA_BACKEND == "panel":
            from .backends.panel import prerender
        
        elif STPYVISTA_BACKEND == "trame":
            from .backends.trame import prerender



        html = prerender(plotter, **backend_options)

        component_value = _component_func(
            embed_html = html,
            height=height,
            width=width,
            horizontal_align=horizontal_align,
            use_container_width=1 if use_container_width else 0,
            key=key,
            default=0,
        )

def main():
    pass


if __name__ == "__main__":
    main()

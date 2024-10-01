from io import StringIO
from typing import Optional, Literal

import panel as pn
import streamlit.components.v1 as components

from pyvista.plotting import Plotter
from pathlib import Path
from bokeh.resources import CDN, INLINE

pn.extension("vtk", sizing_mode="stretch_both")
BOKEH_RESOURCES = {"CDN": CDN, "INLINE": INLINE}


frontend_dir = (Path(__file__).parent / "panel_based").absolute()
_component_func = components.declare_component(
    "stpyvista_panel", path=str(frontend_dir)
)


def stpyvista(
    plotter: Plotter,
    use_container_width: bool = True,
    horizontal_align: Literal["center", "left", "right"] = "center",
    panel_kwargs: Optional[dict] = None,
    bokeh_resources: Literal["CDN", "INLINE"] = "INLINE",
    key: Optional[str] = None,
) -> None:
    """
    Renders an interactive Pyvista Plotter in streamlit.
    
    Parameters
    ----------
    plotter: pv.Plotter
        Pyvista plotter object to render.
    
    use_container_width : bool = True
        If True, set the dataframe width to the width of the parent container. \
        This takes precedence over the `horizontal_align` argument. \
        Defaults to `True`.
    
    horizontal_align : Literal["center", "left", "right"] = "center"
        Horizontal alignment of the stpyvista component. This parameter is ignored if 
        `use_container_width = True`. Defaults to `"center"`.

    panel_kwargs : dict | None = None
        Optional keyword parameters to pass to pn.panel(). Check: 
        https://panel.holoviz.org/api/panel.pane.vtk.html for details. Here are a couple
        of useful ones:
        
        orientation_widget : bool
            Show the xyz axis indicator

        interactive_orientation_widget: bool
            Show and interactive xyz axis indicator

        axes: dict
            Parameters of the axes to construct in the 3D view. Check the example
            at https://stpyvista.streamlit.app/?gallery=axes

    bokeh_resources: Literal["CDN", "INLINE"] = "Inline"
        Source of the BokehJS configuration. Check:
        https://docs.bokeh.org/en/latest/docs/reference/resources.html for details. \
        Defaults to "INLINE" 

    key: str | None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.
    
    Returns
    -------
    None

    """

    if not isinstance(plotter, Plotter):
        raise TypeError(f"{plotter} is not a `pyvista.Plotter` instance.")

    if panel_kwargs is None:
        panel_kwargs = {}

    width, height = plotter.window_size
    vtk_pane = pn.pane.VTK(plotter.ren_win, **panel_kwargs)

    # Check bokeh_resources
    if bokeh_resources not in ("CDN", "INLINE"):
        raise ValueError(
            f'"{bokeh_resources}" is not a valid bokeh resource. '
            'Valid options are "CDN" or "INLINE".'
        )

    # Create HTML file
    with StringIO() as model_bytes:
        vtk_pane.save(
            model_bytes,
            resources=BOKEH_RESOURCES[bokeh_resources],
            title="Running stpyvista",
        )
        panel_html = model_bytes.getvalue()

    component_value = _component_func(
        panel_html=panel_html,
        height=height,
        width=width,
        horizontal_align=horizontal_align,
        use_container_width=1 if use_container_width else 0,
        bgcolor=plotter.background_color.hex_rgba,
        key=key,
        default=0,
    )

    return component_value

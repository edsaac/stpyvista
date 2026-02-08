from typing import Optional, Literal, TypeAlias

from packaging.version import Version
from pyvista.plotting import Plotter
from streamlit.components.v2 import component
from streamlit.version import STREAMLIT_VERSION_STRING

from .dataview import dataview
from .panel_backend import PanelVTKKwargs, _panel_html
from .trame_backend import _trame_html

WindowDimension: TypeAlias = int | Literal["stretch", "content"]

if Version(STREAMLIT_VERSION_STRING) < Version("1.51.0"):
    raise ImportError(
        f"Streamlit version {STREAMLIT_VERSION_STRING} should be >= 1.51"
        "Pin stpyvista<=0.1.4 for components.v1 compatibility"
    )

_html = (
    '<div id="stpyvistadiv">'
    '<iframe id="stpyvistaframe" frameborder="0" allowfullscreen allowtransparency referrerpolicy="same-origin">'
    "</iframe></div>"
)

_stpv_component = component(
    "stpyvista.simple",
    html=_html,
    js="v2/stpyvista.js",
    css="v2/style.css",
    isolate_styles=True,
)


def stpyvista(
    plotter: Plotter,
    backend: Literal["panel", "trame"] = "trame",
    backend_kwargs: Optional[PanelVTKKwargs] = None,
    width: WindowDimension = "stretch",
    key: Optional[str] = None,
) -> None:
    """
    Renders an interactive Pyvista Plotter in streamlit using the
    panel backend.

    Parameters
    ----------
    plotter: pv.Plotter
        Pyvista plotter object to render.

    backend: Literal["panel", "trame"] = "trame",
        Supported backends are `panel` or `trame`

    backend_kwargs : Optional[PanelVTKKwargs | dict] = None
        Optional keyword parameters to pass to pn.panel(). Check the `PanelVTKKwargs`
        documentation for details. Here are a couple of useful ones:

        axes: PanelAxesConfig
            Parameters of the axes to construct in the 3D view.

        orientation_widget : bool
            Show the xyz axis indicator

        interactive_orientation_widget: bool
            Show and interactive xyz axis indicator

        See the example guide at https://stpyvista.streamlit.app/?gallery=axes

    key: Optional[str] = None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.
    """

    if not isinstance(plotter, Plotter):
        raise TypeError(f"{plotter} is not a `pyvista.Plotter` instance.")

    if backend_kwargs is None:
        backend_kwargs = {}

    # Determine width
    use_container_width = width == "stretch"
    plotter_width, height = plotter.window_size

    if not use_container_width:
        if not isinstance(width, int):
            width = plotter_width

    if backend == "panel":
        iframe = _panel_html(plotter, use_container_width=use_container_width, **backend_kwargs)
    elif backend == "trame":
        iframe = _trame_html(plotter, **backend_kwargs)
    else:
        raise ValueError("backend value not supporter")

    data = {
        "_html": iframe,
        "backend": backend,
        "height": height,
        "width": width,
        "use_container_width": use_container_width,
    }

    component_value = _stpv_component(key=key, data=data)
    return component_value


__all__ = ["dataview", "stpyvista"]

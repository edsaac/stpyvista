from pathlib import Path
from typing import Optional, Literal, TypeAlias

import streamlit as st
from streamlit.components.v2 import component
from streamlit.version import STREAMLIT_VERSION_STRING
from pyvista.plotting import Plotter
from packaging.version import Version

from .dataview import dataview
from .panel_backend import PanelVTKKwargs, _panel_html
from .trame_backend import _trame_html

WindowDimension: TypeAlias = int | Literal["stretch", "content"]

if Version(STREAMLIT_VERSION_STRING) < Version("1.51.0"):
    frontend_dir = (Path(__file__).parent / "backends/panel_based").absolute()


_html = """\
<div id="stpyvistadiv">
    <iframe id="stpyvistaframe" sandbox="allow-forms allow-modals allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts allow-downloads" frameborder="0" allowfullscreen allowtransparency="true">
    </iframe>
</div>
"""

_js = """\
export default function (component) {
    const { setStateValue, parentElement, data } = component;
    const stpyvistaframe = parentElement.getElementById("stpyvistaframe");

    // Put plotter in iframe
    stpyvistaframe.srcdoc = data._html;
    stpyvistaframe.style.width = "100%";
    }
"""

_stpv_component = component("stpyvista", html=_html, js=_js)


def stpyvista(
    plotter: Plotter,
    backend: Literal["panel", "trame"] = "trame",
    backend_kwargs: Optional[PanelVTKKwargs] = None,
    width: WindowDimension = "stretch",
    height: WindowDimension = "stretch",
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

    if backend == "panel":
        iframe = _panel_html(plotter, **backend_kwargs)

    elif backend == "trame":
        iframe = _trame_html(plotter, **backend_kwargs)
    else:
        raise ValueError("backend value not supporter")

    data = {"_html": iframe}
    component_value = _stpv_component(data=data, width=width, height=height, key=key)
    return component_value


__all__ = ["dataview", "stpyvista"]

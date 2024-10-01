from base64 import b64encode
from pathlib import Path
from typing import Optional

import streamlit.components.v1 as components

from trame.app import get_server
from trame.widgets import (
    vuetify as vuetify,
)
from trame.widgets.vtk import VtkLocalView
from trame.ui.vuetify import SinglePageLayout
from pyvista.plotting import Plotter


# Tell streamlit that there is a component called `experimental_vtkjs`,
# and that the code to display that component is in the "vanilla_vtkjs" folder
experimental_frontend_dir = (Path(__file__).parent / "vanilla_vtkjs").absolute()
_exp_component_func = components.declare_component(
    "experimental_vtkjs", path=str(experimental_frontend_dir)
)

SERVER_NAME = "stpyvista_server"


async def export_vtksz(plotter: Plotter) -> bytes:
    """Export this plotter as a VTK.js OfflineLocalView file.

    Parameters
    ----------
    plotter : Plotter
        PyVista Plotter object.

    Returns
    -------
    bytes
        The exported plotter view.
    """

    # Get a trame server and launch it
    server = get_server(name=SERVER_NAME, client_type="vue2")
    _, ctrl = server.state, server.controller

    with SinglePageLayout(server) as layout:
        with layout.content:
            view = VtkLocalView(plotter.ren_win)
            ctrl.view_update = view.update

    server.start(
        exec_mode="task",
        host="127.0.0.1",
        port="0",
        open_browser=False,
        show_connection_info=False,
        disable_logging=True,
        timeout=0,
        backend="tornado",
    )

    content = view.export(format=format)
    view.release_resources()

    return content


def stpyvista(vtksz_data: bytes, height: int = 400, key: Optional[str] = None) -> dict:
    """
    Renders an interactive Pyvista Plotter in streamlit.

    Parameters
    ----------
    vtksz_data: bytes
        Data from a vtksz in zip format.

    Returns
    -------
    dict
        A dictionary with the current Camera view properties.
    """

    base64_str = b64encode(vtksz_data).decode().replace("\n", "")

    component_value = _exp_component_func(
        plotter_data=base64_str,
        height=str(height),
        key=key,
        default=0,
    )

    return component_value

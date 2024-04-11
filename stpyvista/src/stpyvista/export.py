from trame.app import get_server
from trame.widgets import (
    vuetify as vuetify,
)

from trame.widgets.vtk import VtkLocalView
from trame.ui.vuetify import SinglePageLayout

from pyvista.plotting import Plotter

SERVER_NAME = "stpyvista_server"


async def export_vtksz(plotter: Plotter):
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



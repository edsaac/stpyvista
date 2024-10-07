from multiprocessing import Process, Queue
from warnings import warn

import streamlit.components.v1 as components

from pyvista.plotting import Plotter


def _export_html(queue: Queue, plotter: Plotter):
    queue.put(plotter.export_html(filename=None))


def stpyvista(plotter: Plotter, **kwargs) -> None:
    """
    Renders an interactive Pyvista Plotter in streamlit using the
    trame backend.

    Parameters
    ----------
    plotter: pv.Plotter
        Pyvista plotter object to render.
    """
    if not isinstance(plotter, Plotter):
        raise TypeError(f"{plotter} is not a `pyvista.Plotter` instance.")

    if "panel_kwargs" in kwargs:
        warn(
            "panel_kwargs is not supported by the trame backend.\n"
            "They will be ignored"
        )

    if "horizontal_align" in kwargs:
        warn(
            "horizontal_align is not supported by the trame backend.\n"
            "It will be ignored"
        )

    queue = Queue(maxsize=1)
    process = Process(target=_export_html, args=(queue, plotter))

    process.start()
    html_plotter = queue.get().read()
    process.join()

    if kwargs.get("use_container_width", True):
        width = None
    else:
        width = plotter.window_size[0]

    components.html(html_plotter, height=plotter.window_size[1], width=width)

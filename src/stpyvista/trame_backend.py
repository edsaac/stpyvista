from multiprocessing import Process, Queue
from typing import Optional

import streamlit.components.v1 as components

from pyvista.plotting import Plotter


def _export_html(queue: Queue, plotter: Plotter):
    queue.put(plotter.export_html(filename=None))


def stpyvista(plotter: Plotter, key: Optional[str] = None) -> None:
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

    queue = Queue(maxsize=1)
    process = Process(target=_export_html, args=(queue, plotter))

    process.start()
    html_plotter = queue.get().read()
    process.join()

    components.html(html_plotter, height=plotter.window_size[1])

from multiprocessing import Process, Queue
from typing import Optional

import streamlit.components.v1 as components

from pyvista.plotting import Plotter


def _export_html(queue: Queue, plotter: Plotter):
    queue.put(plotter.export_html(filename=None))


def stpyvista(plotter: Plotter, key: Optional[str] = None):
    if not isinstance(plotter, Plotter):
        raise TypeError(f"{plotter} is not a `pyvista.Plotter` instance.")

    q = Queue(maxsize=1)
    p = Process(target=_export_html, args=(q, plotter))

    p.start()
    html_plotter = q.get().read()
    p.join()

    components.html(html_plotter, height=plotter.window_size[1])

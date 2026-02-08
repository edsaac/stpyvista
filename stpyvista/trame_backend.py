from multiprocessing import Process, Queue
from pyvista.plotting import Plotter


def _trame_html(plotter: Plotter) -> str:
    if not isinstance(plotter, Plotter):
        raise TypeError(f"{plotter} is not a `pyvista.Plotter` instance.")

    def _export_html(queue: Queue, plotter: Plotter):
        queue.put(plotter.export_html(filename=None))

    queue = Queue(maxsize=1)
    process = Process(target=_export_html, args=(queue, plotter))

    process.start()
    html_plotter = queue.get().read()
    process.join()

    return html_plotter

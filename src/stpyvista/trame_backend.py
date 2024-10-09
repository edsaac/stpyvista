from multiprocessing import Process, Queue
from warnings import warn
from pathlib import Path
from typing import Optional

import streamlit.components.v1 as components
from pyvista.plotting import Plotter


def _export_html(queue: Queue, plotter: Plotter):
    queue.put(plotter.export_html(filename=None))


def _as_html(plotter: Plotter, **kwargs) -> None:
    """Plan to remove this function in the future"""
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


## Using component declaration

frontend_dir = (Path(__file__).parent / "trame_based").absolute()
_component_func = components.declare_component(
    "stpyvista_trame", path=str(frontend_dir)
)


def stpyvista(
    plotter: Plotter,
    use_container_width: bool = True,
    key: Optional[str] = None,
    **kwargs,
) -> None:
    """
    Renders an interactive Pyvista Plotter in streamlit using the
    trame backend.

    Parameters
    ----------
    plotter: pv.Plotter
        Pyvista plotter object to render.
    use_container_width: bool = True
        If True, set the 3D view width to the width of the parent container. \
        If False, the width is taken from the plotter window size.    
    key: Optional[str] = None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    """

    ## Checks
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

    ## Get HTML of plotter
    queue = Queue(maxsize=1)
    process = Process(target=_export_html, args=(queue, plotter))

    process.start()
    html_plotter = queue.get().read()
    process.join()

    ## Set dimensions
    width = None if use_container_width else plotter.window_size[0]
    height = plotter.window_size[1]

    _component_func(
        trame_html=html_plotter,
        height=height,
        width=width,
        use_container_width=use_container_width,
        key=key,
    )

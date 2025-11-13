from io import StringIO
from typing import TypedDict

import panel as pn
from pyvista import Plotter

try:
    # Available from Python 3.11
    from typing import Required, NotRequired

except ImportError:
    # Fallback for older Python versions.
    #   typing_extensions is not a dependency of stpyvista but it
    #   is a dependency of streamlit, so it should be available.
    from typing_extensions import Required, NotRequired


pn.extension("vtk", sizing_mode="stretch_both")


class PanelTicker(TypedDict):
    """
    A `PanelTicker` is a dictionary that contains:
    - **ticks** : `list[float]`, required.
        Positions in the scene coordinates of the corresponding axis' ticks.
    - **labels** : `list[str]`, optional.
        Label displayed respectively to the **ticks** positions.
        If **labels** are not defined, they are inferred from the **ticks** list.
    """

    ticks: list[float]
    labels: NotRequired[list[str]]


class PanelAxesConfig(TypedDict, total=False):
    """
    A `PanelAxesConfig` is a dictionary containing the parameters of the
    axes to construct in the 3D view. It **must contain**:
    - **xticker**: `PanelTicker`, required
    - **yticker**: `PanelTicker`, required
    - **zticker**: `PanelTicker`, required

    Other optional parameters for `PanelAxesConfig` are:
    - **digits** : `int`
        number of decimal digits when `ticks` are converted to `labels`.
    - **fontsize** : `int`
        size in pts of the ticks labels.
    - **show_grid** : `bool`, default is True
        if true the axes grid is visible.
    - **grid_opacity** : `float`, between 0-1
        defines the grid opacity.
    - **axes_opacity** : `float`, between 0-1
        defines the axes lines opacity.
    """

    xticker: Required[PanelTicker]
    yticker: Required[PanelTicker]
    zticker: Required[PanelTicker]
    origin: tuple[float, float, float]
    fontsize: int
    show_grid: bool
    grid_opacity: float
    axes_opacity: float
    digits: int


class PanelVTKKwargs(TypedDict, total=False):
    """
    A `PanelVTKKwargs` is a dictionary containing the parameters of the
    vtk pane to construct in the 3D view. Optional parameters are:
    - **axes**: `PanelAxesConfig`
        parameters of the axes to construct in the 3D view.
    - **orientation_widget** : `bool`
        show the xyz axis indicator
    - **interactive_orientation_widget** : `bool`
        show and interactive xyz axis indicator
    """

    axes: PanelAxesConfig
    orientation_widget: bool
    interactive_orientation_widget: bool


def _panel_html(plotter: Plotter, **backend_kwargs) -> str:
    width, height = plotter.window_size
    vtk_pane = pn.pane.VTK(plotter.ren_win, **backend_kwargs)

    # Create HTML file
    with StringIO() as model_bytes:
        vtk_pane.save(
            model_bytes,
            title="Running stpyvista",
        )
        html_plotter = model_bytes.getvalue()

    return html_plotter

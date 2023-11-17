# __init__.py

from io import BytesIO
from pathlib import Path
from typing import Optional, Literal
import streamlit.components.v1 as components
import pyvista as pv
import panel as pn
from bokeh.resources import CDN

pv.set_jupyter_backend("static")
pn.extension("vtk", sizing_mode="stretch_width")

# Tell streamlit that there is a component called stpyvista,
# and that the code to display that component is in the "frontend" folder
frontend_dir = (Path(__file__).parent / "frontend").absolute()

_component_func = components.declare_component("stpyvista", path=str(frontend_dir))


class stpyvistaTypeError(TypeError):
    """Unsupported format for input"""

    pass


# Create the python function that will be called from the front end
HA_MODES = Literal["left", "center", "right"]


def stpyvista(
    plotter: pv.Plotter,
    use_container_width: bool = True,
    horizontal_align: HA_MODES = "center",
    panel_kwargs=None,
    key: Optional[str] = None,
) -> None:
    """
    Renders an interactive pyvisya Plotter in streamlit.
    
    Parameters
    ----------
    input: Union[pv.Plotter, HTML_stpyvista]
        Plotter to render
    
    use_container_width : bool = True
        If True, set the dataframe width to the width of the parent container. \
        This takes precedence over the `horizontal_align` argument. \
        Defaults to True
    
    horizontal_align: str = "center"
        Either "center", "left" or "right". Defaults to "center". 

    panel_kwargs: dict | None
        Optional keyword parameters to pass to pn.panel() Check: 
        https://panel.holoviz.org/api/panel.pane.vtk.html for details. Here is
        a useful one:
        
        orientation_widget: bool
            Show the xyz axis indicator

    key: str|None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.
    
    Returns
    -------
    None
    """

    if isinstance(plotter, pv.Plotter):
        if panel_kwargs is None:
            panel_kwargs = dict()

        width, height = plotter.window_size

        if use_container_width:
            geo_pan_pv = pn.panel(plotter.ren_win, height=height, **panel_kwargs)
        else:
            geo_pan_pv = pn.panel(
                plotter.ren_win, height=height, width=width, **panel_kwargs
            )

        # Create HTML file
        model_bytes = BytesIO()
        geo_pan_pv.save(model_bytes, resources=CDN)
        panel_html = model_bytes.getvalue().decode("utf-8")
        model_bytes.close()

        component_value = _component_func(
            panel_html=panel_html,
            height=height,
            width=width,
            horizontal_align=horizontal_align,
            use_container_width=1 if use_container_width else 0,
            key=key,
            default=0,
        )

        return component_value

    else:
        raise (stpyvistaTypeError)


def main():
    pass


if __name__ == "__main__":
    main()

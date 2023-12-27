# __init__.py

from io import BytesIO
from pathlib import Path
from typing import Optional, Literal
import streamlit.components.v1 as components
import pyvista as pv
import panel as pn

from bokeh.resources import CDN, INLINE
BOKEH_RESOURCES = {"CDN": CDN, "INLINE": INLINE}

pn.extension("vtk", sizing_mode="stretch_both")

# Tell streamlit that there is a component called stpyvista,
# and that the code to display that component is in the "frontend" folder
frontend_dir = (Path(__file__).parent / "frontend").absolute()
_component_func = components.declare_component("stpyvista", path=str(frontend_dir))


class stpyvistaTypeError(TypeError):
    pass

class stpyvistaValueError(ValueError):
    pass


# Create the python function that will be called from the front end

def stpyvista(
    plotter: pv.Plotter,
    use_container_width: bool = True,
    horizontal_align: Literal["center", "left", "right"] = "center",
    panel_kwargs: dict|None = None,
    bokeh_resources: Literal["CDN", "INLINE"] = "INLINE",
    key: Optional[str] = None,
) -> None:
    """
    Renders an interactive pyvisya Plotter in streamlit.
    
    Parameters
    ----------
    input: pv.Plotter
        Pyvista plotter object to render.
    
    use_container_width : bool = True
        If True, set the dataframe width to the width of the parent container. \
        This takes precedence over the `horizontal_align` argument. \
        Defaults to `True`.
    
    horizontal_align : Literal["center", "left", "right"] = "center"
        Horizontal alignment of the stpyvista component. This parameter is ignored if 
        `use_container_width = True`. Defaluts to `"center"`.

    panel_kwargs : dict | None = None
        Optional keyword parameters to pass to pn.panel() Check: 
        https://panel.holoviz.org/api/panel.pane.vtk.html for details. Here is
        a useful one:
        
        orientation_widget : bool
            Show the xyz axis indicator

    bokeh_resources: Literal["CDN", "INLINE"] = "Inline"
        Source of the BokehJS configuration. Check:
        https://docs.bokeh.org/en/latest/docs/reference/resources.html for details. \
        Defaults to "INLINE" 

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

        geo_pan_pv = pn.panel(plotter.ren_win, **panel_kwargs)
        
        # Check bokeh_resources
        if not bokeh_resources in ("CDN", "INLINE"):
            raise stpyvistaValueError(
                f'"{bokeh_resources}" is not a valid bokeh resource. '
                'Valid options are "CDN" or "INLINE".'
            )
            
        
        # Create HTML file
        model_bytes = BytesIO()
        geo_pan_pv.save(model_bytes, resources=BOKEH_RESOURCES[bokeh_resources])
        panel_html = model_bytes.getvalue().decode("utf-8")
        model_bytes.close()
        
        component_value = _component_func(
            panel_html=panel_html,
            height=height,
            width=width,
            horizontal_align=horizontal_align,
            use_container_width=1 if use_container_width else 0,
            bgcolor = plotter.background_color.hex_rgba,
            key=key,
            default=0,
        )

        return component_value

    else:
        raise stpyvistaTypeError(
            f'{plotter} is not a `pyvista.Plotter` instance. '
        )


def main():
    pass


if __name__ == "__main__":
    main()

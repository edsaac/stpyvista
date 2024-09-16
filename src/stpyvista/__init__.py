# __init__.py

from io import StringIO
from pathlib import Path
from typing import Optional, Literal
import base64
import xml.dom.minidom

import streamlit as st
import streamlit.components.v1 as components

from pyvista.plotting import Plotter
from pyvista import DataSet

import panel as pn
from bokeh.resources import CDN, INLINE

pn.extension("vtk", sizing_mode="stretch_both")
BOKEH_RESOURCES = {"CDN": CDN, "INLINE": INLINE}


class stpyvistaTypeError(TypeError):
    pass


class stpyvistaValueError(ValueError):
    pass


# Tell streamlit that there is a component called `experimental_vtkjs`,
# and that the code to display that component is in the "vanilla_vtkjs" folder
experimental_frontend_dir = (Path(__file__).parent / "vanilla_vtkjs").absolute()
_exp_component_func = components.declare_component(
    "experimental_vtkjs", path=str(experimental_frontend_dir)
)


def experimental_vtkjs(
    vtksz_data: bytes, height: int = 400, key: Optional[str] = None
) -> dict:
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

    base64_str = base64.b64encode(vtksz_data).decode().replace("\n", "")

    component_value = _exp_component_func(
        plotter_data=base64_str,
        height=str(height),
        key=key,
        default=0,
    )

    return component_value


frontend_dir = (Path(__file__).parent / "panel_based").absolute()
_component_func = components.declare_component("stpyvista", path=str(frontend_dir))


def stpyvista(
    plotter: Plotter,
    use_container_width: bool = True,
    horizontal_align: Literal["center", "left", "right"] = "center",
    panel_kwargs: Optional[dict] = None,
    bokeh_resources: Literal["CDN", "INLINE"] = "INLINE",
    key: Optional[str] = None,
) -> None:
    """
    Renders an interactive Pyvista Plotter in streamlit.
    
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

    if isinstance(plotter, Plotter):
        if panel_kwargs is None:
            panel_kwargs = dict()

        width, height = plotter.window_size

        geo_pan_pv = pn.pane.VTK(plotter.ren_win, **panel_kwargs)

        # Check bokeh_resources
        if bokeh_resources not in ("CDN", "INLINE"):
            raise stpyvistaValueError(
                f'"{bokeh_resources}" is not a valid bokeh resource. '
                'Valid options are "CDN" or "INLINE".'
            )

        # Create HTML file
        with StringIO() as model_bytes:
            geo_pan_pv.save(model_bytes, resources=BOKEH_RESOURCES[bokeh_resources])
            panel_html = model_bytes.getvalue()

        component_value = _component_func(
            panel_html=panel_html,
            height=height,
            width=width,
            horizontal_align=horizontal_align,
            use_container_width=1 if use_container_width else 0,
            bgcolor=plotter.background_color.hex_rgba,
            key=key,
            default=0,
        )

        return component_value

    else:
        raise stpyvistaTypeError(f"{plotter} is not a `pyvista.Plotter` instance. ")


def dataview(obj: DataSet):
    """
    Renders the HTML representation of a Pyvista/VTK dataset.

    Parameters
    ----------
    element: pv.DataSet
        Pyvista element with some data to show.

    Returns
    -------
    None
    """

    def assemble_details(title: str, table: str) -> str:
        return f"<details open><summary><em>{title}</em></summary>{table}</details>"

    try:
        # Look up an HTML representation and arange in details tags

        dom = xml.dom.minidom.parseString(obj._repr_html_())
        tables = dom.getElementsByTagName("table")

        css = """
            <style>
            details {
                padding: 6px;
                margin-bottom: 5px; 
                border: 1px solid #eeeeee;
                background-color: transparent;
                border-radius: 10px;
            }
            summary {
                background-color: transparent;
                opacity: 60%;
                padding: 5px;
            }
            summary::marker {
                color: purple;
                font-size: 1.1em;
            }
            </style>
        """

        html = StringIO("""<div class="stpv-dataview">""")

        if len(tables) == 1:
            html.write(assemble_details("Header", tables[0].toprettyxml()))

        else:
            headers = (
                dom.getElementsByTagName("table")[0]
                .getElementsByTagName("tr")[0]
                .getElementsByTagName("th")
            )

            for title, table in zip(headers, tables[1:]):
                html.write(
                    assemble_details(title.firstChild.nodeValue, table.toprettyxml())
                )

        html.write(css + "</div>")

        # Render in streamlit
        st.html(html.getvalue())

    except AttributeError:
        # Defaults to streamlit's write function
        st.write(obj)


def main():
    pass


if __name__ == "__main__":
    main()

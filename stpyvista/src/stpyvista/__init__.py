from pathlib import Path
from turtle import window_height, window_width
from typing import Optional

import streamlit as st
import streamlit.components.v1 as components

import pyvista as pv
import io
import tempfile
import os

## Using pythreejs as pyvista backend
pv.set_jupyter_backend('pythreejs')
pv.global_theme.transparent_background = True

# Tell streamlit that there is a component called stpyvista,
# and that the code to display that component is in the "frontend" folder
frontend_dir = (Path(__file__).parent / "frontend").absolute()
_component_func = components.declare_component(
	"stpyvista", path=str(frontend_dir)
)

# Create the python function that will be called
def stpyvista(
    title : str,
    plotter : pv.Plotter,
    key: Optional[str] = None,
):
    """
    Add a descriptive docstring
    """

    model_html = io.StringIO()
    plotter.export_html(model_html, backend='pythreejs')
    parsed_html = model_html.getvalue()
    model_html.close()
    
    window_width, window_height = plotter.window_size
    print(window_width is plotter.window_size[0])
    print(window_height)

    component_value = _component_func(
        title = window_height,
        value = parsed_html,
        width = f"{window_width}",
        height = window_height,
        key = key
    )

    return component_value


def main():
    st.write("## Example")
    value = stpyvista()

    st.write(value)


if __name__ == "__main__":
    main()

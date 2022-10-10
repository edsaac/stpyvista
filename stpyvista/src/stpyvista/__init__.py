from pathlib import Path
from typing import Optional

import streamlit as st
import streamlit.components.v1 as components

# Tell streamlit that there is a component called stpyvista,
# and that the code to display that component is in the "frontend" folder
frontend_dir = (Path(__file__).parent / "frontend").absolute()

_component_func = components.declare_component(
	"stpyvista", 
    path=str(frontend_dir)
)


import pyvista as pv
import io
import os

## Using pythreejs as pyvista backend
pv.set_jupyter_backend('pythreejs')
pv.global_theme.transparent_background = True

# Create the python function that will be called
def stpyvista(
    plotter : pv.Plotter = None,
    key: Optional[str] = None
    ) -> float:
    """
    Renders a pyvista Plotter object
    
    Parameters
    ----------
    plotter: pyvista.Plotter
        Plotter to render
    
    key: str|None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.
    
    Returns
    -------
    float
    """

    model_html = io.StringIO()
    plotter.export_html(model_html, backend='pythreejs')
    parsed_html = model_html.getvalue()
    model_html.close()
    
    # with open("generated.html",'w') as f:
    #     f.write(parsed_html)

    window_width, window_height = plotter.window_size

    # parsed2 = parsed_html.splitlines()[10:-1]
    # parsed3 = "\n".join(parsed2)

    component_value = _component_func(
        threejs_html = parsed_html,
        width = window_width,
        height = window_height,
        key = key,
        default = 0
    )

    return component_value

def main():
    import datetime

    st.title("Component `stpyvista`")
    placeholder = st.empty()
    path_to_stl = "../../../onewaywrap/assets/ToolHolder.STL"
    if os.path.exists(path_to_stl):

        ## Initialize pyvista reader and plotter
        plotter = pv.Plotter(border=True, border_width=1, window_size=[400,400]) 
        plotter.set_background('#D3EEFF')

        ## Color panel
        color_stl = st.color_picker("Element","#0BD88D")

        ## Initialize pyvista reader and plotter
        reader = pv.STLReader(path_to_stl)
        mesh = reader.read()
        plotter.add_mesh(mesh, color=color_stl)
        out = stpyvista(plotter=plotter)

        placeholder.markdown(f"{datetime.datetime.now()} :: {out}")
        print(f"{datetime.datetime.now()} :: {out}")

    " ************* "
    st.header("Hello Again")
    st.button("Hey")
    placeholder_spheres = st.empty()

    pl = pv.Plotter(window_size=[600,500])
    pl.set_background('#D3EEFF')

    # lower left, using physically based rendering
    pl.add_mesh(pv.Sphere(center=(-1, 0, -1)),
                show_edges=False, pbr=True, color='white', roughness=0.2,
                metallic=0.5)

    # upper right, matches default pyvista plotting
    pl.add_mesh(pv.Sphere(center=(1, 0, 1)))

    # Upper left, mesh displayed as points
    pl.add_mesh(pv.Sphere(center=(-1, 0, 1)),
                color='k', style='points', point_size=10)

    # mesh in lower right with flat shading
    pl.add_mesh(pv.Sphere(center=(1, 0, -1)), lighting=False,
                show_edges=True)

    # show mesh in the center with a red wireframe
    pl.add_mesh(pv.Sphere(), lighting=True, show_edges=False,
                color='red', line_width=0.5, style='wireframe',
                opacity=0.99)

    pl.camera_position = 'xz'
    
    out = stpyvista(pl)

    placeholder_spheres.markdown(
        f"{datetime.datetime.now()} :: {out}")
    
if __name__ == "__main__":
    main()

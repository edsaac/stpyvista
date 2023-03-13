import streamlit as st
import pyvista as pv
pv.set_jupyter_backend('panel')

from stpyvista import stpyvista

import panel as pn
pn.extension('vtk')
from bokeh.resources import INLINE

from tempfile import NamedTemporaryFile

## Initialize a plotter object
plotter = pv.Plotter(window_size=[500,500])
mesh = pv.Cube(center=(0,0,0))
mesh['myscalar'] = mesh.points[:, 2]*mesh.points[:, 0]
plotter.add_mesh(mesh, scalars='myscalar', cmap='bwr', line_width=1)
plotter.background_color = '#dddddd'

mesh = pv.Cube(center=(1.1, 0.0, 0.0))
plotter.add_mesh(mesh)
plotter.view_isometric()

"# Component:"
#stpyvista(plotter)

"# The gist of the component:"
width, height = plotter.window_size
geo_pan_pv = pn.pane.VTK(plotter.ren_win, width=width, height=height, orientation_widget=True, background="#aaaaaa") 
geo_pan_pv.vtk_camera.SetPosition(15, 15, 15)

player = pn.widgets.Player(name='Player', start=10, end=60, value=40, loop_policy='reflect', interval=100)

@pn.depends(value=player.param.value)
def animate(value) -> None:
    geo_pan_pv.vtk_camera.SetPosition(value, value, value)
    geo_pan_pv.synchronize()

pncol = pn.Column(player, geo_pan_pv, animate).servable()

# Create HTML file
with NamedTemporaryFile(mode='a+', suffix='.html') as model_html:
    pncol.save(model_html.name, resources=INLINE, embed=False)
    panel_html = model_html.read()

    st.components.v1.html(panel_html, height=1500)
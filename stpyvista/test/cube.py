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
plotter.view_isometric()

"# Component:"
stpyvista(plotter)

"# The gist of the component:"
width, height = plotter.window_size
geo_pan_pv = pn.panel(plotter.ren_win, width=width, height=height, orientation_widget=True, background="#f307eb") 
        
# Create HTML file
with NamedTemporaryFile(mode='a+', suffix='.html') as model_html:
    print(model_html.name)
    geo_pan_pv.save(model_html.name, resources=INLINE)
    panel_html = model_html.read()

dimensions = plotter.window_size

st.components.v1.html(panel_html, height=510)
import streamlit as st
from stpyvista import stpyvista
import os
import pyvista as pv

st.title("Not hello")

path_to_stl = "../onewaywrap/assets/ToolHolder.STL"
print(os.path.exists(path_to_stl))

## Initialize pyvista reader and plotter
plotter = pv.Plotter(border=True, window_size=[200,400]) 

## Color panel
col1,col2 = st.columns(2)
color_stl = col1.color_picker("Element","#0BD88D")
color_bkg = col2.color_picker("Background","#FFFFFF")

## Initialize pyvista reader and plotter
plotter.background_color = color_bkg

print(f"path is {path_to_stl}", os.path.exists(path_to_stl))
reader = pv.STLReader(path_to_stl)

mesh = reader.read()
plotter.add_mesh(mesh,color=color_stl)

i = stpyvista("Hi!, I'm a title", plotter)

st.header("Hello Again")
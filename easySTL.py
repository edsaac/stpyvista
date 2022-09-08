import streamlit as st
import pyvista as pv
import io

## Using pythreejs as pyvista backend
pv.set_jupyter_backend('pythreejs')

## Upload a pyvista file
stlFilePath ="./assets/ToolHolder.STL"

## Initialize pyvista reader and plotter
plotter = pv.Plotter(border=True, window_size=[500,400]) 
plotter.background_color = "#F2F2F2"

reader = pv.STLReader(stlFilePath)

## Read data and send to plotter
mesh = reader.read()
plotter.add_mesh(mesh)

## Export to a pythreejs HTML
model_html = io.StringIO()
plotter.export_html(model_html, backend='pythreejs')

## Show in webpage
st.components.v1.html(model_html.getvalue(),height=400)

## Print HTML
with st.expander("Code"):
    st.code(model_html.getvalue(),language='cshtml')
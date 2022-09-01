import streamlit as st
import pyvista as pv
import io
import tempfile

## Using pythreejs as pyvista backend
pv.set_jupyter_backend('pythreejs')

## Upload a pyvista file
uploadedFile = st.file_uploader("Upload a STL:",["stl"],False)

## Streamlit layout
st.sidebar.title("STL viewer")

if uploadedFile:
    
    ## Color panel
    col1,col2 = st.sidebar.columns(2)
    color_stl = col1.color_picker("Element","#0BD88D")
    color_bkg = col2.color_picker("Background","#FFFFFF")

    ## Initialize pyvista reader and plotter
    plotter = pv.Plotter(border=False, window_size=[500,400]) 
    plotter.background_color = color_bkg

    ## Create a tempfile to keep the uploaded file as pyvista's API 
    ## only supports file paths but not buffers
    with tempfile.NamedTemporaryFile(suffix="_streamlit") as f: 
        f.write(uploadedFile.getbuffer())
        reader = pv.STLReader(f.name)
    
        ## Read data and send to plotter
        mesh = reader.read()
        plotter.add_mesh(mesh,color=color_stl)

        ## Export to a pythreejs HTML
        model_html = io.StringIO()
        plotter.export_html(model_html, backend='pythreejs')
        
        ## Show in webpage
        st.components.v1.html(model_html.getvalue(),height=400)
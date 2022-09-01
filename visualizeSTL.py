import streamlit as st
import pyvista as pv
import io
import tempfile

pv.set_jupyter_backend(None)
pv.start_xvfb(wait=0,window_size=[500,800])

## Upload a pyvista file
uploadedFile = st.file_uploader("Upload a STL:",["stl"],False)

## Streamlit layout
st.sidebar.title("STL viewer")

if uploadedFile:
    
    ## Color panel
    col1,col2 = st.sidebar.columns(2)
    color_stl = col1.color_picker("Element","#0BD88D")
    color_bkg = col2.color_picker("Background","#FFFFFF")

    ## Create a tempfile to keep the uploaded file as pyvista's API 
    ## only supports file paths but not buffers
    with tempfile.NamedTemporaryFile(suffix=".streamlit",dir=".") as f: 
    
        ## Initialize pyvista reader and plotter
        plotter = pv.Plotter(border=True, window_size=[500,800],off_screen=False) 
        plotter.background_color = color_bkg

        ## Read file
        f.write(uploadedFile.getbuffer())
        reader = pv.STLReader(f.name)

        ## Read data and send to plotter
        mesh = reader.read()
        plotter.add_mesh(mesh,color=color_stl)

        ## Export to a pythreejs HTML
        model_html = io.StringIO()
        plotter.export_html(model_html, backend='pythreejs')
            
    st.code(model_html.getvalue(),language="cshtml")

    ## Show in webpage
    st.components.v1.html(model_html.getvalue(),height=800)
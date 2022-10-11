## 🧊 `stpyvista`: Show PyVista 3D visualizations in streamlit.
<a href="https://github.com/edsaac/streamlit-PyVista-viewer"><img alt="Github Repo" src="https://img.shields.io/static/v1?label=&message=Check repository&color=black&logo=github"></a> [![PyPi version](https://badgen.net/pypi/v/stpyvista/)](https://pypi.org/project/stpyvista/)

![howto-stpyvista|600x340](upload://AdaTZTB4w7T8b2b2ERcmwazK7Dm.gif)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://edsaac-stpyvista-tests-howtouse-stpyvista-2p9u5r.streamlitapp.com/)

This is a simple wrapper for PyVista plotter objects using the [pythreejs backend](https://docs.pyvista.org/user-guide/jupyter/pythreejs.html). I relied heavily on @blackary['s blog post](https://blog.streamlit.io/how-to-build-your-own-streamlit-component/) on how to build a custom component (thanks!). 

****
### Installation:
```sh
pip install stpyvista 
```
****
### Demos:

📤 Display your own STL file on Streamlit: 

![uploadstl-stpyvista|579x500, 75%](upload://wRjAqCvikVhY09MI5YqeC6i6T0N.gif)


[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://edsaac-stpyvista-tests-uploadstl-stpyvista-pqlypk.streamlitapp.com/)

🍞 Physically Based Rendering (PBR):

![textures-stpyvista|508x500, 85%](upload://keGT0Vs62ZrFJy6HYbegcuWIgtE.gif)


[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://edsaac-stpyvista-tests-textures-stpyvista-j3ovua.streamlitapp.com/)

****
### Usage example:
```python
import pyvista as pv
import streamlit as st
from stpyvista import stpyvista, HTML_stpyvista
import numpy as np

# ipythreejs does not support scalar bars :(
pv.global_theme.show_scalar_bar = False

st.title("A cube")
st.info("""Code adapted from https://docs.pyvista.org/user-guide/jupyter/pythreejs.html#scalars-support""")

# Storing the threejs models as a session_state variable allows
# to avoid re-rendering at each time something changes in the page

if "model" not in st.session_state:    
    ## Initialize a plotter object
    plotter = pv.Plotter(window_size=[400,400])

    ## Create a mesh with a cube 
    mesh = pv.Cube(center=(0,0,0))

    ## Add some scalar field associated to the mesh
    mesh['myscalar'] = mesh.points[:, 2]*mesh.points[:, 0]

    ## Add mesh to the plotter
    plotter.add_mesh(mesh, scalars='myscalar', cmap='bwr', line_width=1)

    ## Final touches
    plotter.view_isometric()
    plotter.background_color = 'white'
    
    ## Export and save to st.session_state
    st.session_state.model = HTML_stpyvista(plotter)

stpyvista(st.session_state.model)
```
> Result: 
> ![image|589x500, 75%](upload://kkkuz7VbI8WBVUrT3uAUMw00OiT.png)

****
#### Also check:
https://www.pyvista.org/




import streamlit as st
import pyvista as pv
import numpy as np
from stpyvista import stpyvista, dataview

def put_in_plotter(actor: pv.DataSet):
    plotter = pv.Plotter()
    plotter.window_size = (300, 300)
    plotter.add_mesh(actor, line_width=10)
    plotter.view_isometric()
    return plotter

def sphere():
    return pv.Sphere(radius=1.0, center=(0, 0, 0))

def spline():
    theta = np.linspace(-1 * np.pi, 1 * np.pi, 100)
    z = np.linspace(2, -2, 100)
    r = z**2 + 1
    x = r * np.sin(theta)
    y = r * np.cos(theta)
    points = np.column_stack((x, y, z))
    return pv.Spline(points, 1000)

def surface():
    x = np.arange(-10, 10, 0.5)
    y = np.arange(-10, 10, 0.5)
    x, y = np.meshgrid(x, y)
    z = np.sin(np.sqrt(x**2 + y**2))
    
    surf = pv.StructuredGrid(x, y, z)
    
    x, y, z = surf.cell_centers().points.T
    surf["x"] = x
    surf["y"] = y
    surf["z"] = z
    surf["r"] = np.sqrt(x**2 + y**2 + z**2)

    surf.set_active_scalars("r")

    return surf


def main():

    st.title("Testing `dataview`")

    datasets = [
        sphere(),
        spline(),
        surface()
    ]
    
    for obj in datasets:
        cols = st.columns([1, 1.5])
        
        with cols[0]:
            stpyvista(put_in_plotter(obj))
        with cols[1]:
            dataview(obj)
    
    dataview(pv.MultiBlock(datasets))

if __name__ == "__main__":
    main()
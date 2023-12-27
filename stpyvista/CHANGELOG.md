# Changelog

## [v 0.0.13] - 2023-12-27
- Tweak iframe dimensions to get iframe centered
- Add fullscreen button for all plotters
- Plotter background color is used as iframe bgcolor

## [v 0.0.12] - 2023-12-26
- Add option to pass to `bokeh.resources` to load either `CDN` or `INLINE`. Defaults to `INLINE`.
- Update docstring for stpyvista

## [v 0.0.11] - 2023-11-20
- Remove unnecessary pyvista call for a jupyter backend. Ipython dependency can be totally drop now.

## [v 0.0.10] - 2023-11-16
- Add `use_container_width` option to `stpyvista`. Defaults to True 
- Changed bokeh.resources to import CDN instead of INLINE to html generation.
- Drop ipython from the dependencies. 

## [v 0.0.9] - 2023-09-05

- Use hatchling for building package. Remove setup.py support.
- Remove `panel` as the jupyter_notebook backend. Not necessary if reading from panel.
- Move changelog from README.md to CHANGELOG.md 

## [v 0.0.8]

- Remove excessive whitespace below the rendered component.
- Can pass additional kwargs to panel.pane.vtk, e.g. setting an orientation_widget. Check panel-vtk for details on valid kwargs.
    
## [v 0.0.6]

- Replaced `pythreejs` backend for `panel` backend. This is a temporary solution as pyvista will remove panel support in favor of trame.

## [v 0.0.5]

- Support transparent backgrounds to blend with streamlit's web app theme.
- Add a control to spin along a certain axis the first mesh passed to the plotter.

## [v 0.0.4]

- Pass a key to the stpyvista component to avoid re-rendering at every streamlit interaction
- Using ipywidgets `embed_minimal_html` directly instead of pyvista `export_html`. 
- Update examples as a multipage streamlit app
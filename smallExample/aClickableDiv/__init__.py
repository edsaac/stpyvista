from pathlib import Path
from typing import Optional

import streamlit as st
import streamlit.components.v1 as components

# Tell streamlit that there is a component called stpyvista,
# and that the code to display that component is in the "frontend" folder
frontend_dir = (Path(__file__).parent / "frontend").absolute()

_component_func = components.declare_component(
	"clickablediv", 
    path=str(frontend_dir)
)

# Create the python function that will be called
def clickablediv(
    message : str,
    key: Optional[str] = None,
) -> float:
    """
    Renders a div
    
    Parameters
    ----------
    message: str
        Plotter to render
    
    key: str|None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.
    
    Returns
    -------
    float
    """
    component_value = _component_func(
        message = message,
        key = key,
        default = 0
    )

    return component_value

def main():
    import datetime

    st.title("Component `clickable div`")
    message = st.text_input("Input to div", value="Hello from main")
    placeholder = st.empty()
    out = clickablediv(message=message)

    placeholder.markdown(
        f"{datetime.datetime.now()} :: {out}")
    
if __name__ == "__main__":
    main()

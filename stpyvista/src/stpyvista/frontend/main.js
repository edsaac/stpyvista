// The `Streamlit` object exists because our html file includes
// `streamlit-component-lib.js`.
// If you get an error about "Streamlit" not being defined, that
// means you're missing that file.

function sendValue(value) {
  Streamlit.setComponentValue(value)
}

/**
 * The component's render function. This will be called immediately after
 * the component is initially loaded, and then again every time the
 * component gets new data from Python.
 */
function onRender(event) {
  
  // Only run the render code the first time the component is loaded.
  if (!window.rendered) {
    // You most likely want to get the data passed in like this
    const {value, width, height, key} = event.detail.args;

    const div_all = document.getElementById("stPyVista");
    const st_iframe = document.getElementById("stPyVistaFrame");
    
    // You'll most likely want to pass some data back to Python like this   
    // sendValue({output1: div_el.offsetWidth})

    st_iframe.srcdoc = value;
    
    st_iframe.width = width + 20;
    st_iframe.height = height + 30;
    
    st_iframe.style.border = "none";

    Streamlit.setFrameHeight(height + 50)
    window.rendered = true;
  }
}

// Render the component whenever python send a "render event"
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)

// Tell Streamlit that the component is ready to receive events
Streamlit.setComponentReady()

// Render with the correct height, if this is a fixed-height component
Streamlit.setFrameHeight()

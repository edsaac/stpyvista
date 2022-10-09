// The `Streamlit` object exists because our html file includes
// `streamlit-component-lib.js`.
// If you get an error about "Streamlit" not being defined, that
// means you're missing that file.

function sendValue(value) {
  Streamlit.setComponentValue(value)
}

function changeColor(color){
  document.getElementById("stPyVistaFrame").style.backgroundColor = color
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
    
    // Pass the threejs HTML to the iframe
    st_iframe.srcdoc = value;  
    
    // Overwrite default iframe dimensions
    st_iframe.width = width + 20;
    st_iframe.height = height + 25;
    Streamlit.setFrameHeight(height + 40);
    

    // Test sending back a value
    div_all.addEventListener('click', event => sendValue(666999), false);
    div_all.addEventListener('click', event => changeColor("red"), false);

    // Remove default iframe border. A border can be set from the pv.Plotter
    st_iframe.style.border = "none";

    window.rendered = true;
  }
  
  // You'll most likely want to pass some data back to Python like this   
  // document.getElementById("stPyVistaFrame").addEventListener('pointerover', event => changeColor("red"), false);
  // Streamlit.setComponentValue("HiOut")
}

// Render the component whenever python send a "render event"
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)

// Tell Streamlit that the component is ready to receive events
Streamlit.setComponentReady()

// Render with the correct height, if this is a fixed-height component
Streamlit.setFrameHeight()

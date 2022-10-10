// The `Streamlit` object exists because our html file includes
// `streamlit-component-lib.js`.
// If you get an error about "Streamlit" not being defined, that
// means you're missing that file.

function sendValue(value) {
  Streamlit.setComponentValue(value)
}

function changeColor(color){
  document.getElementById("clickablediv").style.backgroundColor = color;
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
    const {message, key} = event.detail.args;
    const my_div = document.getElementById("clickablediv");
    
    Streamlit.setFrameHeight(50)

    // Overwrite default iframe dimensions
    my_div.style.height = "200px";

    // Remove default iframe border. A border can be set from the pv.Plotter
    my_div.style.border = "solid 10px blue";
    my_div.innerHTML = message;
    
    // Do stuff on click
    my_div.addEventListener('pointerover', event => changeColor("rgba(250, 0, 114, 0.151)"), false);
    
    // Send some value to python 
    my_div.addEventListener('click', event => sendValue(50), false);
    
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

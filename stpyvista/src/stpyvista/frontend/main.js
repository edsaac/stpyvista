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
    const {threejs_html, width, height, horizontal_align, has_controls, key} = event.detail.args;
    const stpyvistadiv = document.getElementById("stpyvistadiv");
    const stpyvistaframe = document.getElementById("stpyvistaframe");

    // Style the wrapping div for the iframe
    stpyvistadiv.style.width = width + 15;
    stpyvistadiv.style.textAlign = horizontal_align;
    
    // Overwrite default iframe dimensions and put model in the iframe
    // just CSS styling does not apply to the iframe
    stpyvistaframe.srcdoc = threejs_html;
    stpyvistaframe.width = width + 15;
    console.log("WIDTH", width)
    console.log("CONTROLS", has_controls)

    if (has_controls > 0) {
      stpyvistaframe.height = height + 60;  
      Streamlit.setFrameHeight(height + 95)
    } else {
      stpyvistaframe.height = height + 15;
      Streamlit.setFrameHeight(height + 40)
    }
    
    stpyvistaframe.scrolling = "no";
    stpyvistaframe.style.border = "none";

    // Send some value to python 
    // Not very useful at the moment but keep it for later
    // stpyvistadiv.addEventListener('click', event => sendValue(50), false);

    window.rendered = true;
  }
}

// Render the component whenever python send a "render event"
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)

// Tell Streamlit that the component is ready to receive events
Streamlit.setComponentReady()

// Render with the correct height, if this is a fixed-height component
Streamlit.setFrameHeight()

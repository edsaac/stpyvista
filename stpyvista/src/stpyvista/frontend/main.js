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
    const {panel_html, height, width, horizontal_align, use_container_width, key} = event.detail.args;
    
    const stpyvistadiv = document.getElementById("stpyvistadiv");
    const stpyvistaframe = document.getElementById("stpyvistaframe");
    
    // Style the wrapping div for the iframe
    stpyvistadiv.style.textAlign = horizontal_align;

    // Overwrite default iframe dimensions with the container width
    if (Boolean(use_container_width)){
        
        stpyvistaframe.width = document.body.offsetWidth;
        
        // Listen to resize changes. If any, panel takes care of resizing
        function updateFrameWidth() {
            stpyvistaframe.width = document.body.offsetWidth;
        }
        
        window.onresize = function(event) {
            updateFrameWidth();
        }
    } else {
        stpyvistaframe.width = width + 24;
    }
    
    stpyvistaframe.srcdoc = panel_html;
    stpyvistaframe.height = height + 20;
    stpyvistaframe.scrolling = "yes";
    

    // stpyvistadiv.style.width = stpyvistaframe.width + 10;

    // console.log("HEIGHT", height)
    Streamlit.setFrameHeight(height + 50);
    stpyvistaframe.style.border = "2px red";
    
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

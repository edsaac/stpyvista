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
        const { panel_html, height, width, horizontal_align, use_container_width, bgcolor, key } = event.detail.args;

        const mainframe = window.parent.document.querySelector('iframe[title="stpyvista.panel_backend.stpyvista_panel"]');
        mainframe.title = "stpyvista.rendered"

        // const stpyvistadiv = document.getElementById("stpyvistadiv");
        const stpyvistaframe = document.getElementById("stpyvistaframe");
        const fullscreen_height = window.screen.height;

        // Style the wrapping div for the iframe
        mainframe.parentElement.style.textAlign = horizontal_align;
        mainframe.contentDocument.querySelector('body').style.backgroundColor = bgcolor;

        function updateFrameWidth() {
            delete mainframe.width;
            stpyvistaframe.width = document.body.offsetWidth + 20;
        }

        if (Boolean(use_container_width)) {
            window.onresize = function (event) {
                updateFrameWidth();
            }
        } else {
            mainframe.width = width + 10;
            stpyvistaframe.width = width + 16;
        }

        function fullscreenchanged(event) {

            if (document.fullscreenElement) {
                updateFrameWidth();

                stpyvistaframe.height = fullscreen_height - 4;
                Streamlit.setFrameHeight(fullscreen_height);

            } else {
                if (Boolean(use_container_width)) {
                    updateFrameWidth();
                } else {
                    mainframe.width = width + 10;
                    stpyvistaframe.width = width + 16;
                }

                stpyvistaframe.height = height;
                Streamlit.setFrameHeight(height + 4);
            }
        }

        document.addEventListener("fullscreenchange", fullscreenchanged);

        stpyvistaframe.srcdoc = panel_html;
        stpyvistaframe.scrolling = "yes";

        stpyvistaframe.height = height;
        Streamlit.setFrameHeight(height);

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

export default function (component) {
    const { setStateValue, parentElement, data } = component;
    const stpyvistaframe = parentElement.getElementById("stpyvistaframe");
    
    // Put plotter in iframe
    stpyvistaframe.srcdoc = data._html;
    stpyvistaframe.height = data.height;

    if (Boolean(data.use_container_width)) {
        stpyvistaframe.width = "100%";
    } else {
        stpyvistaframe.width = data.width;
    }

    // Remove margin after the iframe loads
    stpyvistaframe.addEventListener('load', () => {
        const iframedoc = stpyvistaframe.contentDocument || myframe.contentWindow.document;
        
        // Hide scrolling bars
        iframedoc.body.style.overflow = 'hidden';

        // Stretch to container width
        function updateFrameWidth() {
            stpyvistaframe.width = parentElement.host.offsetWidth;
        }

        // Remove default margins 
        if (data.backend == "panel") {
            var vtk_div = iframedoc.querySelector('div.bk-panel-models-vtk-VTKSynchronizedPlot');
            vtk_div.style.margin = "0";

            if (Boolean(data.use_container_width)) {
                updateFrameWidth();
                vtk_div.style.width = "calc(100% + 20px)";
                window.onresize = function (event) { updateFrameWidth(); }
            } else {
                stpyvistaframe.width = data.width;
            }
        } else if (data.backend == "trame") {
            if (Boolean(data.use_container_width)) {
                updateFrameWidth();
                window.onresize = function (event) { updateFrameWidth(); }
            } else {
                stpyvistaframe.width = data.width;
            }
        }
    });
}

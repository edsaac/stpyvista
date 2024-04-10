function onRender(event) {

    // Only run the render code the first time the component is loaded.
    if (!window.rendered) {

        // You most likely want to get the data passed in like this
        const { plotter_data, key } = event.detail.args;

        var container = document.querySelector('.content');
        var base64Str = plotter_data;
        OfflineLocalView.load(container, { base64Str });

        const interactor = renderWindow.getInteractor();
        interactor.onRightButtonPress((event) => {

            const camera = renderWindow.getRenderers()[1].getActiveCamera();

            var cameraProperties = {
                position: camera.getPosition(),
                focal_point: camera.getFocalPoint(),
                up: camera.getViewUp(),
                view_angle: camera.getViewAngle(),
                clipping_range: camera.getClippingRange(),
                parallel_projection: camera.getParallelProjection()
            };

            Streamlit.setComponentValue(cameraProperties);
        });

        window.rendered = true;
        Streamlit.setFrameHeight('300');
    }
}

Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender);
Streamlit.setComponentReady();

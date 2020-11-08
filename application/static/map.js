function configure_map() {
    var map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/dark-v10',
        center: [DEFAULT_CENTER_LONG, DEFAULT_CENTER_LAT],
        zoom: 16
    });

    map.on('load', function () {
        map.addSource('routers', {
            'type': 'geojson',
            'data': INITAL_FEATURES
        });
        const max_devices = Math.max(...INITAL_FEATURES.features.map(f => f.properties.devices));
        map.addLayer({
            'id': 'routers',
            'type': 'fill',
            'source': 'routers',
            'layout': {},
            'paint': {
                'fill-color': ['interpolate', ['linear'], ['get', 'devices'],
                    0, '#0a0',
                    max_devices / 2, '#ff0',
                    max_devices, '#a00'],
                'fill-opacity': 0.5
            }
        });

        var popup = new mapboxgl.Popup({
            closeButton: false,
            closeOnClick: false,
            offset: [30,0]
        });
        map.on('mousemove', 'routers', function (e) {
            map.getCanvas().style.cursor = 'pointer';

            var coordinates = e.lngLat.wrap();
            var name = e.features[0].properties.name;
            var devices = e.features[0].properties.devices;

            while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
                coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
            }

            popup.setLngLat(coordinates).setHTML(`<b>${name}:</h3> ${devices} online.`).addTo(map);
        });


        map.on('mouseleave', 'routers', function () {
            map.getCanvas().style.cursor = '';
            popup.remove();
        });
    });
}

$(document).ready(function () {
    // Configure the map
    configure_map();


    // Setup auto-submit for campus form
    $("#campus-select").change(function () {
        console.log("change");
        $("#campus-form").submit();
    });
});
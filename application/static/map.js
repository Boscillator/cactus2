$(document).ready(function() {
    var map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/dark-v10',
        center: [DEFAULT_CENTER_LONG, DEFAULT_CENTER_LAT],
        zoom: 16
    });
});
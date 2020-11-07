$(document).ready(function() {
    // Configure the map
    var map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/dark-v10',
        center: [DEFAULT_CENTER_LONG, DEFAULT_CENTER_LAT],
        zoom: 16
    });


    // Setup auto-submit for campus form
    $("#campus-select").change(function() {
        console.log("change");
        $("#campus-form").submit();
    })
});
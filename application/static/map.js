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
            offset: [30, 0]
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

    return map;
}

function timeConverter(UNIX_timestamp){
    var a = new Date(UNIX_timestamp * 1000);
    var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    var year = a.getFullYear();
    var month = months[a.getMonth()];
    var date = a.getDate();
    var hour = a.getHours();
    var min = a.getMinutes();
    var sec = a.getSeconds();
    var time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec ;
    return time;
}

$(document).ready(function () {
    // Configure the map
    var map = configure_map();


    // Setup auto-submit for campus form
    var campusSelect = $("#campus-select");
    campusSelect.change(function () {
        console.log("change");
        $("#campus-form").submit();
    });


    var timeSlider = $("#time-step-selector");

    function onSliderChange() {
        var currentCampus = campusSelect.val();
        var sliderValue = parseInt(timeSlider.val());
        var newTimestamp = Math.floor((Date.now() / 1000)) + (sliderValue * 60);

        console.log(new Date(newTimestamp * 1000).toUTCString())
        // map.getSource('routers').setData({
        //     'type': 'FeatureCollection',
        //     'features': []
        // });

        var mapElement = $("#map");
        mapElement.addClass("blur");
        mapElement.removeClass("deblur");

        $.getJSON(`/api/campus/${currentCampus}?t=${newTimestamp}`, function (data) {
            console.log(data);
            map.getSource('routers').setData(data);
            mapElement.removeClass("blur");
            mapElement.addClass("deblur");
        });
    }

    $("#btn-decrease-time").click(function () {
        timeSlider.val(Math.max(-30, parseInt(timeSlider.val()) - 1));
        onSliderChange();
    });

    $("#btn-increase-time").click(function () {
        timeSlider.val(Math.min(0, parseInt(timeSlider.val()) + 1));
        onSliderChange();
    });

    timeSlider.change(function () {
        onSliderChange();
    });
});
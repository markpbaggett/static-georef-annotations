<!DOCTYPE html>
<html data-theme="halloween">
<head>
    <title>Map Coordinates Finder</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
    <link href="https://cdn.jsdelivr.net/npm/daisyui@4.12.2/dist/full.min.css" rel="stylesheet" type="text/css" />
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        #map {
            height: 400px;
            width: 100%;
        }
    </style>
</head>
<body>
    <div id="map"></div>
    <p id="coordinates">Click on the map to get coordinates</p>
    <label for="latitude">Latitude:</label>
    <input type="text" id="latitude" class="input input-bordered input-primary w-auto max-w-xs" readonly>
    <label for="longitude">Longitude:</label>
    <input type="text" id="longitude" class="input input-bordered input-primary w-auto max-w-xs" readonly>
    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
    <script>
        var map = L.map('map').setView([30.61631726196063, -96.33998821143554], 13);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
        }).addTo(map);

        map.on('click', function(e) {
            var lat = e.latlng.lat;
            var lng = e.latlng.lng;
            document.getElementById('coordinates').innerHTML = "<br/>";
            document.getElementById('latitude').value = lat;
            document.getElementById('longitude').value = lng;
        });
    </script>
</body>
</html>


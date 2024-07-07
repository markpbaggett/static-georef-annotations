<!DOCTYPE html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.3.1/dist/leaflet.css" />
    <link rel="stylesheet" href="https://rawgit.com/heyman/leaflet-areaselect/master/src/leaflet-areaselect.css" />
    <link rel="stylesheet" href="static/styles.css">
    <script src="https://unpkg.com/leaflet@1.3.1/dist/leaflet.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="https://cdn.rawgit.com/mejackreed/Leaflet-IIIF/v1.2.2/leaflet-iiif.js"></script>
    <script src="https://cdn.rawgit.com/heyman/leaflet-areaselect/da8905695db78354ddd5b5d9de6ef13699b9d7a7/src/leaflet-areaselect.js"></script>
</head>
<body>
<div id="map"></div>
<div class="drawer">
    <div>
        <span>Points</span>
        <input id="point" />
    </div>
    <div>
        <span>Region</span>
        <input id="region" />
    </div>
</div>
<script src="static/app.js"></script>
</body>
</html>
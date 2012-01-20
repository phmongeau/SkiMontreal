var locations, infoWindows, icons;

$(document).ready(function(){
	infoWindows = [];

	var size = new OpenLayers.Size(32,37);
	icons = {
		blue: new OpenLayers.Icon('ski_blue.png', size),
		red:  new OpenLayers.Icon('ski_red.png', size),
		grey: new OpenLayers.Icon('ski_grey.png', size),
	};

	$.getJSON("/conditions.json", function(data){
		locations = data;
		$("#update").html(locations.updated);
		getLocation();
	});
});

function getLocation()
{
	var lat = 45.530079, long = -73.631354;
	//var latlng = OpenLayers.LonLat(-73.631354, 45.530079);
	//console.log(latlng);
	createMap(long, lat);
}

function createMap(long, lat)
{
	var zoom=11;

	map = new OpenLayers.Map('map', {
		panDuration: 200,
		controls: [
			new OpenLayers.Control.PanZoomBar(),
			new OpenLayers.Control.Navigation({dragPanOptions: {enableKinetic: true}}),
			new OpenLayers.Control.KeyboardDefaults()
		]
	}); 


	//Layers
	layerMapnik = new OpenLayers.Layer.OSM.Mapnik("Mapnik");
	map.addLayer(layerMapnik);
	

	map.proj = new OpenLayers.Projection("EPSG:4326");
	var lonLat = new OpenLayers.LonLat(long, lat);
	lonLat.transform(map.proj, map.getProjectionObject());

	map.setCenter(lonLat, zoom);

	addMarkers(locations, map);
}

function addMarkers(locations, map)
{
	var markers = new OpenLayers.Layer.Markers("Markers");
	map.addLayer(markers);

	var icon = new OpenLayers.Icon('ski_blue.png', new OpenLayers.Size(32, 37));

	for(var i in locations)
	{
		loc = locations[i];

		var icon = new OpenLayers.Icon('ski_blue.png', new OpenLayers.Size(32, 37));
		var icon = icons.blue.clone();

		var markerLoc = new OpenLayers.LonLat(loc.longitude, loc.latitude);
		markerLoc.transform(map.proj, map.getProjectionObject());

		//var marker = new OpenLayers.Marker(markerLoc, icon);
		//markers.addMarker(marker);
		
		markers.addMarker(createMarker(markerLoc, loc));

		//var markerLoc = new google.maps.LatLng(
				//loc.latitude,
				//loc.longitude);
		//addMarker(markerLoc, map, loc);

	}
}

function createMarker(markerLoc, track)
{
	marker = new OpenLayers.Marker(markerLoc);

	if (track.open == "null" || track.open == "0" || !track.open)
		marker.icon = icons.grey.clone();
	else if (track.condition == "Bonne" || track.condition == "Excellente")
		marker.icon = icons.blue.clone();
	else
		marker.icon = icons.red.clone();
	
	return marker;
	//contentText =   ""
				  //+ "<div>"
				  //+ "<h2>" + track.name + "</h2>"
				  //+ "<br>"
				  //+ "conditions: " + track.condition
				  //+ "<br>"
				  //+ "ouvert: " + track.open
				  //+ "<br>"
				  //+ "deblay&eacute;: " + track.deblaye;
				  //+ "</div>";

	//var info = new google.maps.InfoWindow({
			//content: contentText,
			//maxWidth: 400
	//});

	//infoWindows.push(info);

	//google.maps.event.addListener(marker, 'click', function() {
		//for (var i in infoWindows)
		//{
			//infoWindows[i].close();
		//}
		//info.open(map, marker);
	//});
	
}

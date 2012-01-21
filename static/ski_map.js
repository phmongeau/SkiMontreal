var locations, infoWindows, icons, markers, features;

AutoSizeAnchored = OpenLayers.Class(OpenLayers.Popup.FramedCloud, {
	'autoSize': true
});


$(document).ready(function(){
	infoWindows = [];
	features = [];

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

	layerMapnik = new OpenLayers.Layer.OSM("OSM");
	map.addLayer(layerMapnik);

	map.proj = new OpenLayers.Projection("EPSG:4326");

	var lonLat = new OpenLayers.LonLat(long, lat);
	lonLat.transform(map.proj, map.getProjectionObject());
	map.setCenter(lonLat, zoom);

	markers = new OpenLayers.Layer.Markers("Markers");
	map.addLayer(markers);

	addMarkers(locations, map);
}

function addMarkers(locations, map)
{
	for(var i in locations)
	{
		loc = locations[i];

		var markerLoc = new OpenLayers.LonLat(loc.longitude, loc.latitude);
		markerLoc.transform(map.proj, map.getProjectionObject());

		if(loc.name)
			addMarker(loc, markerLoc, AutoSizeAnchored, 'test', true);

	}

}

function addMarker(track, ll, popupClass, popupContentHTML, closeBox, overflow) {
	var feature = new OpenLayers.Feature(markers, ll);
	feature.closeBox = closeBox;
	feature.popupClass = popupClass;
	//feature.data.popupContentHTML = popupContentHTML;
	feature.data.overflow = (overflow) ? "auto" : "hidden";

	if (track.open == "null" || track.open == "0" || !track.open)
		feature.data.icon = icons.grey.clone();
	else if (track.condition == "Bonne" || track.condition == "Excellente")
		feature.data.icon = icons.blue.clone();
	else
		feature.data.icon = icons.red.clone();

	popupContentHTML =   ""
					   + "<div>"
					   + "<h2>" + track.name + "</h2>"
					   + "<br>"
					   + "conditions: " + track.condition
					   + "<br>"
					   + "ouvert: " + track.open
					   + "<br>"
					   + "deblay&eacute;: " + track.deblaye
					   + "<br>"
					   + "mise &agrave; jour: " + track["arrondissement"].date_maj
					   + "</div>";
	feature.data.popupContentHTML = popupContentHTML;

	marker = feature.createMarker();
	//marker.icon = icons.blue.clone();

	var markerClick = function (evt) {
		features.forEach(function(f){ if(f.popup) f.popup.hide();});
		if(this.popup == null) {
			this.popup = this.createPopup(this.closeBox);
			map.addPopup(this.popup);
			this.popup.show();
		} else {
			this.popup.toggle();
		}
		currentPopup = this.popup;
		OpenLayers.Event.stop(evt);
	};
	marker.events.register("mousedown", feature, markerClick);

	features.push(feature);
	markers.addMarker(marker);
}

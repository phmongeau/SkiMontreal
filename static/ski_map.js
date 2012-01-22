var locations, infoWindows, icons, ski_markers, glisse_markers, features, map;

AutoSizeAnchored = OpenLayers.Class(OpenLayers.Popup.FramedCloud, {
	'autoSize': true
});


$(document).ready(function(){
	infoWindows = [];
	features = [];

	var size = new OpenLayers.Size(32,37);
	var offset = new OpenLayers.Pixel(0,-37);
	ski_icons = {
		blue: new OpenLayers.Icon('ski_blue.png', size, offset),
		red:  new OpenLayers.Icon('ski_red.png', size, offset),
		grey: new OpenLayers.Icon('ski_grey.png', size, offset),
	};
	glisse_icons = {
		blue: new OpenLayers.Icon('glisse_blue.png', size, offset),
		red:  new OpenLayers.Icon('glisse_red.png', size, offset),
		grey: new OpenLayers.Icon('glisse_grey.png', size, offset),
	};

	$.getJSON("/conditions.json", function(data){
		locations = data;
		$("#update").html(locations.updated);
		//getLocation();
		addMarkers(locations, map);
	});
	map = createMap();
});


function createMap(long, lat)
{
	var map;
	var lat = 45.530079, long = -73.631354;
	var zoom=11;

	map = new OpenLayers.Map('map', {
		panDuration: 200,
		controls: [
			new OpenLayers.Control.PanZoomBar(),
			new OpenLayers.Control.LayerSwitcher(),
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

	ski_markers = new OpenLayers.Layer.Markers("Ski");
	map.addLayer(ski_markers);

	glisse_markers = new OpenLayers.Layer.Markers("Glisse");
	map.addLayer(glisse_markers);

	return map

	//addMarkers(locations, map);
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
	if(track.type == "ski")
		var feature = new OpenLayers.Feature(ski_markers, ll);
	else
		var feature = new OpenLayers.Feature(glisse_markers, ll);
	feature.closeBox = closeBox;
	feature.popupClass = popupClass;
	//feature.data.popupContentHTML = popupContentHTML;
	feature.data.overflow = (overflow) ? "auto" : "hidden";

	if(track.type == "ski")
	{
		if (track.open == "null" || track.open == "0" || !track.open)
			feature.data.icon = ski_icons.grey.clone();
		else if (track.condition == "Bonne" || track.condition == "Excellente")
			feature.data.icon = ski_icons.blue.clone();
		else
			feature.data.icon = ski_icons.red.clone();
	}
	else
	{
		if (track.open == "null" || track.open == "0" || !track.open)
			feature.data.icon = glisse_icons.grey.clone();
		else if (track.condition == "Bonne" || track.condition == "Excellente")
			feature.data.icon = glisse_icons.blue.clone();
		else
			feature.data.icon = glisse_icons.red.clone();
	}

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
	if(track.type == "ski")
		ski_markers.addMarker(marker);
	else
		glisse_markers.addMarker(marker);
}

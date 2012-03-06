var locations, infoWindows, icons, ski_markers, glisse_markers, features, map, style_ski, style_glisse, selectedFeatures, tracks;

AutoSizeAnchored = OpenLayers.Class(OpenLayers.Popup.FramedCloud, {
	'autoSize': true
});


$(document).ready(function(){
	infoWindows = [];
	features = [];
	tracks = [];

	//Icons
	var size = new OpenLayers.Size(32,37);
	var offset = new OpenLayers.Pixel(0,-37);
	ski_icons = {
		blue: new OpenLayers.Icon('static/ski_blue.png', size, offset),
		red:  new OpenLayers.Icon('static/ski_red.png', size, offset),
		grey: new OpenLayers.Icon('static/ski_grey.png', size, offset)
	};
	glisse_icons = {
		blue: new OpenLayers.Icon('static/glisse_blue.png', size, offset),
		red:  new OpenLayers.Icon('static/glisse_red.png', size, offset),
		grey: new OpenLayers.Icon('static/glisse_grey.png', size, offset)
	};

	style_ski = {};
	style_glisse = {};

	map = createMap();
	// Get JSON
	$.getJSON("/conditions.json", function(data){
		locations = data;
		$("#update").html(locations.updated);
		addMarkers(locations, map);
		loadPistes();
	});
	
	// Toggle Buttons
	$("#skiToggle").click(function() {
		ski_markers.setVisibility(!ski_markers.getVisibility());
		if(ski_markers.getVisibility())
			$("#skiToggle img").attr('src', '/static/button_ski_blue.png');
		else
			$("#skiToggle img").attr('src', '/static/button_ski_grey.png');
	});
	$("#glisseToggle").click(function() {
		glisse_markers.setVisibility(!glisse_markers.getVisibility());
		if(glisse_markers.getVisibility())
			$("#glisseToggle img").attr('src', '/static/button_glisse_blue.png');
		else
			$("#glisseToggle img").attr('src', '/static/button_glisse_grey.png');
	});

	$("#tracksToggle").click(function() {
		for (var i in tracks)
		{
			tracks[i].setVisibility(!tracks[i].getVisibility());
		}

		if(tracks[0].getVisibility())
			$("#tracksToggle img").attr('src', '/static/button_track_blue.png');
		else
			$("#tracksToggle img").attr('src', '/static/button_track_grey.png');
	});

});


function createMap()
{
	var map;
	var lat = 45.530079, lng = -73.631354;
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

	var lonLat = new OpenLayers.LonLat(lng, lat);
	lonLat.transform(map.proj, map.getProjectionObject());
	map.setCenter(lonLat, zoom);

	function createStyle(img)
	{
		var style;
		style = OpenLayers.Util.extend({}, OpenLayers.Feature.Vector.style['default']);
		style.externalGraphic = img;
		style.graphicOpacity = 1;
		style.graphicHeight = 37;
		style.graphicYOffset = -style.graphicHeight;
		return style;
	}
	
	style_ski.blue = createStyle("static/ski_blue.png");
	style_ski.red = createStyle("static/ski_red.png");
	style_ski.grey = createStyle("static/ski_grey.png");

	style_glisse.blue = createStyle("static/glisse_blue.png");
	style_glisse.red  = createStyle("static/glisse_red.png");
	style_glisse.grey = createStyle("static/glisse_grey.png");


	glisse_markers = new OpenLayers.Layer.Vector("Glisse");
	map.addLayer(glisse_markers);

	ski_markers = new OpenLayers.Layer.Vector("Ski");
	map.addLayer(ski_markers);

	var selectControl = new OpenLayers.Control.SelectFeature([ski_markers, glisse_markers]);
	map.addControl(selectControl);
	selectControl.activate();

	selectedFeatures = [];

	onFeatureSelect = function(evt) {
		//close all popups
		for(i in selectedFeatures)
		{
			var f = selectedFeatures.pop();
			f.popup.hide();
		}

		var feature = evt.feature;
		selectedFeatures.push(feature);
		if ( feature.popup === null)
		{
			popup = new AutoSizeAnchored("chicken",
					feature.geometry.getBounds().getCenterLonLat(),
					null,
					feature.data.popupContentHTML,
					null, true, null);
			feature.popup = popup;
			map.addPopup(popup);
		}
		else {
			feature.popup.show();
		}
	};

	onFeatureDeselect = function(evt) {
		evt.feature.popup.hide();
	};

	ski_markers.events.register("featureselected", ski_markers, onFeatureSelect);
	glisse_markers.events.register("featureselected", glisse_markers, onFeatureSelect);


	return map;
}

function addMarkers(locations, map)
{
	if(locations.ski_error && locations.glisse_error)
	{
		console.log("can't load data");
		console.log('ski: ' + locations.ski_error);
		console.log('glisse: ' + locations.glisse_error);
		return;
	}
	for(var i in locations)
	{
		loc = locations[i];

		var markerLoc = new OpenLayers.Geometry.Point(loc.longitude, loc.latitude);
		markerLoc.transform(map.proj, map.getProjectionObject());

		if(loc.name)
			addMarker(loc, markerLoc, AutoSizeAnchored, 'test', true);

	}

}

function addMarker(track, ll, popupClass, popupContentHTML, closeBox, overflow) {
	var feature;

	if(track.type == "ski")
	{
		feature = new OpenLayers.Feature.Vector(ll, null, style_ski.blue);

		if (track.open == "null" || track.open == "0" || !track.open)
			feature.style = style_ski.grey;
		else if (track.condition == "Bonne" || track.condition == "Excellente")
			feature.style = style_ski.blue;
		else
			feature.style = style_ski.red;

		ski_markers.addFeatures([feature]);
	}
	else
	{
		feature = new OpenLayers.Feature.Vector(ll, null, style_glisse.red);

		if (track.open == "null" || track.open == "0" || !track.open)
			feature.style = style_glisse.grey;
		else if (track.condition == "Bonne" || track.condition == "Excellente")
			feature.style = style_glisse.blue;
		else
			feature.style = style_glisse.red;

		glisse_markers.addFeatures([feature]);
	}

	feature.closeBox = closeBox;
	feature.popupClass = popupClass;
	feature.data.overflow = (overflow) ? "auto" : "hidden";

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


	features.push(feature);
}

function loadPistes()
{
	$.getJSON("/gpx/list", function(data){
		files = data;
		for (var i in files)
		{
			url = '/gpx/get/' + files[i];
			addGPX(url, files[i]);
		}
	});
}

function addGPX(file_url, index, color)
{
	if (color === null || color === undefined)
	{
		color = "blue";
	}
	var lgpx = new OpenLayers.Layer.Vector("Piste: " + index, {
		style: {strokeColor: color, strokeWidth: 2, strokeOpacity: 0.5},
		projection: map.proj,
		strategies: [new OpenLayers.Strategy.Fixed()],
		protocol: new OpenLayers.Protocol.HTTP({
			url: file_url,
			format: new OpenLayers.Format.GPX({
				extractAttributes: true,
				extractStyles: false,
				maxDepth: 4,
				extractTracks: true,
				extractRoutes: false,
				extractWaypoints: false
			})
		})
	});

	tracks.push(lgpx);
	map.addLayer(lgpx);
}

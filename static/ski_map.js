var locations, infoWindows;

$(document).ready(function(){
	infoWindows = [];
	$.getJSON("ski_coords.json", function(data){
		locations = data;
		getLocation();
	});
});

function getLocation()
{
	var latlng;
	//if (navigator.geolocation)
	//{
		//navigator.geolocation.getCurrentPosition(
			//function(position) {
				//latlng = new google.maps.LatLng(
					//position.coords.latitude,
					//position.coords.longitude);
				//createMap(latlng);
			//},
			//function(position) {
				//latlng = new google.maps.LatLng("45.50866990", "-73.55399249999999");
				//createMap(latlng);
			//}
		//);
	//}
	//else
	//{
		//latlng = new google.maps.LatLng("45.50866990", "-73.55399249999999");
		//createMap(latlng);
	//}
	latlng = new google.maps.LatLng("45.530079", "-73.631354");
	createMap(latlng);
}

function createMap(latlng)
{
	var opts = {
		zoom: 11,
		center: latlng,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	};

	var map = new google.maps.Map(
			document.getElementById("map"), opts);

	addMarkers(locations, map);
}

function addMarkers(locations, map)
{
	for(var i in locations)
	{
		loc = locations[i];

		var markerLoc = new google.maps.LatLng(
				loc.latitude,
				loc.longitude);
		addMarker(markerLoc, map, loc);

	}
}

function addMarker(latlng, map, track)
{
		var marker = new google.maps.Marker({
			position: latlng,
			map: map,
			title: track.name
		});

		if (track.open == "null" || track.open == "0" || !track.open)
			marker.setIcon("ski_grey.png");
		else if (track.condition == "Bonne")
			marker.setIcon("ski_blue.png");
		else
			marker.setIcon("ski_red.png");

		contentText =   ""
					  + "<div>"
					  + "<h2>" + track.name + "</h2>"
					  + "<br>"
					  + "conditions: " + track.condition
					  + "<br>"
					  + "ouvert: " + track.open
					  + "<br>"
					  + "deblay&eacute;: " + track.deblaye;
					  + "</div>";

		var info = new google.maps.InfoWindow({
				content: contentText,
				maxWidth: 400
		});

		infoWindows.push(info);

		google.maps.event.addListener(marker, 'click', function() {
			for (var i in infoWindows)
			{
				infoWindows[i].close();
			}
			info.open(map, marker);
		});
	
}

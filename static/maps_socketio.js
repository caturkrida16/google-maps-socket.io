// Google Maps
const defaultLatLng = {
	lat: 0.7893, 
	lng: 131.044 
};
var locations = {};

// >>> Initialization
window.initMap = function initMap() {
  const map = new google.maps.Map(document.getElementById("googleMap"), {
	zoom: 4,
	center: defaultLatLng
  });
  return map;
}

// >>> Marker Map
function markerMap() {
	var map = initMap();
	
	for (var key in locations) {
		new google.maps.Marker({
			position: new google.maps.LatLng(locations[key]["latitude"], locations[key]["longitude"]),
			map,
			title: key
		});
	}
}
// Socket.IO
const socket = io(SocketIoHost, {
	extraHeaders: {
		"accessToken": accessToken
	}
});
// >>> Listen
socket.on("gps_website", function(data) {
	for (var i=0; i < imeiGps.length; i++) {
		if (data.hasOwnProperty(imeiGps[i])) {
			locations[imeiGps[i]] = data[imeiGps[i]];
			markerMap();
			break;
		}
	}
});
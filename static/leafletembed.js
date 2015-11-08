var map;
var ajaxRequest;
var plotlist;
var plotlayers=[];

function initmap() {
	// set up the map
	map = new L.Map('map');

	// create the tile layer with correct attribution
	var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
	var osmAttrib='Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
	var osm = new L.TileLayer(osmUrl, {minZoom: 5, maxZoom: 18, attribution: osmAttrib});		

	// start the map at KSU Marietta
	map.setView(new L.LatLng(33.9383158, -84.5223048),9);
	map.addLayer(osm);
}
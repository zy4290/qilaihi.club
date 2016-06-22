/**
 * Created by huhai on 2016/6/16.
 */
var map = new BMap.Map("allmap");
var point = new BMap.Point(116.331398,39.897445);
map.centerAndZoom(point,12);
var geolocation = new BMap.Geolocation();
geolocation.getCurrentPosition(function(r){
    var mk = new BMap.Marker(r.point);
    map.addOverlay(mk);
    map.panTo(r.point);
    var gc = new BMap.Geocoder();
    gc.getLocation(r.point, function(rs){
        var addComp = rs.addressComponents;
        document.getElementById('place').innerText = rs.addressComponents.city
    },{enableHighAccuracy: true});
});
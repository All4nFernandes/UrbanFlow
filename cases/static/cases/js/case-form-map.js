(() => {
 const mapElement=document.getElementById("select-map");
 const latitudeField=document.getElementById("id_latitude");
 const longitudeField=document.getElementById("id_longitude");
 if(!mapElement||!latitudeField||!longitudeField||!window.L)return;
 const map=L.map(mapElement).setView([-14.2,-51.9],4);
 L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",{maxZoom:19,attribution:"&copy; OpenStreetMap contributors"}).addTo(map);
 let marker;
 const setPoint=(latitude,longitude)=>{
  latitudeField.value=Number(latitude).toFixed(6);
  longitudeField.value=Number(longitude).toFixed(6);
  if(marker)marker.setLatLng([latitude,longitude]);else marker=L.marker([latitude,longitude]).addTo(map);
 };
 map.on("click",event=>setPoint(event.latlng.lat,event.latlng.lng));
 if(latitudeField.value&&longitudeField.value){
  const point=[Number(latitudeField.value),Number(longitudeField.value)];
  map.setView(point,15);setPoint(point[0],point[1]);
 }
})();
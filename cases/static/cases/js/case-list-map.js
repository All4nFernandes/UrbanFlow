(() => {
 const mapElement=document.getElementById("case-map");
 const dataElement=document.getElementById("map-cases-data");
 if(!mapElement||!dataElement||!window.L)return;
 const data=JSON.parse(dataElement.textContent);
 const map=L.map(mapElement).setView([-14.2,-51.9],4);
 L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",{maxZoom:19,attribution:"&copy; OpenStreetMap contributors"}).addTo(map);
 const points=[];
 data.forEach(item=>{
  const marker=L.marker([item.latitude,item.longitude]).addTo(map);
  const popup=document.createElement("div");
  const title=document.createElement("strong");title.textContent=item.title;popup.appendChild(title);
  const status=document.createElement("div");status.textContent="Status: "+item.status;popup.appendChild(status);
  if(item.detail_url){const link=document.createElement("a");link.href=item.detail_url;link.textContent="Ver detalhes";popup.appendChild(link);}
  marker.bindPopup(popup);points.push([item.latitude,item.longitude]);
 });
 if(points.length)map.fitBounds(points,{padding:[24,24],maxZoom:15});
})();
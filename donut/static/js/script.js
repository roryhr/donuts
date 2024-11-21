var map = L.map('map').setView([37.910, -119.0117], 4);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

console.log('IN SCRIPT.JS from JS static');

async function loadShops() {
    try {
        const response = await fetch('/api/shops/');
        const shops = await response.json(); 
        console.log(shops); // Use the shop data
        // Use `shops` here, e.g., pass it to a map-rendering function
        renderShopsOnMap(shops);
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
    }
}

// Call the function to load and process the data
loadShops();

function renderShopsOnMap(shops) {
    // Example: Iterate over the shops and render them
    shops.forEach(shop => {
        console.log(`Shop: ${shop.name}, Location: (${shop.lat}, ${shop.lon})`);
        // Add map plotting logic here
        var marker = L.marker([shop.lat, shop.lon]).addTo(map);
        marker.bindPopup("<b>" + shop.name + "</b><br>");
    });
}


var popup = L.popup();

function onMapClick(e) {
    popup
        .setLatLng(e.latlng)
        .setContent("You clicked the map at " + e.latlng.toString())
        .openOn(map);
}

map.on('click', onMapClick);
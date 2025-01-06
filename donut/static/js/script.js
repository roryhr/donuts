var map = L.map('map').setView([37.910, -119.0117], 6);

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
        // console.log(`Shop: ${shop.name}, Location: (${shop.lat}, ${shop.lon})`);
        // Add map plotting logic here
        var marker = L.marker([shop.lat, shop.lon]).addTo(map);
        marker.bindPopup("<b>" + shop.name + "</b><br>");
    });
}


function renderShopsHTML(shops) {
    console.log("IN SHOPS HTML");
    console.log(shops);
    const shopList = document.getElementById('shop-list');
    shopList.innerHTML = '';

    shops.forEach(shop => {
        // Create a div for each shop
        const shopDiv = document.createElement('div', tagName = "shop");
        shopDiv.classList.add('shop');

        // Add elements inside the div

        const nameHeading = document.createElement('h2');
        nameHeading.textContent = shop.name;
        shopDiv.appendChild(nameHeading);

        const addressParagraph = document.createElement('p');
        const strongAddress = document.createElement('strong');
        strongAddress.textContent = 'Address:';
        addressParagraph.appendChild(strongAddress);
        addressParagraph.appendChild(document.createTextNode('\n')); // Add a line break
        addressParagraph.appendChild(document.createTextNode(shop.address_line_1));
        addressParagraph.appendChild(document.createTextNode('\n'));
        addressParagraph.appendChild(document.createTextNode(shop.address_line_2));
        shopDiv.appendChild(addressParagraph);

        const reviewParagraph = document.createElement('p');
        const strongReview = document.createElement('strong');
        strongReview.textContent = 'Review:';
        reviewParagraph.appendChild(strongReview);
        reviewParagraph.appendChild(document.createTextNode(shop.review));
        shopDiv.appendChild(reviewParagraph);

        // Add the shop div to the list container
        shopList.appendChild(shopDiv);
    });
}

var popup = L.popup();

function onMapClick(e) {
    const { lat, lng } = e.latlng;

    // Fetch distances from the server
    fetch(`/api/calculate_distances/?lat=${lat}&lon=${lng}`)
        .then(response => response.json())
        .then(data => {
            console.log('Shops with distances:', data);

            let content = `<b>Clicked Location:</b> (${lat}, ${lng})<br><br>`;
            content += `<b>Nearby Shops:</b><br>`;

            data.forEach(shop => {
                content += `${shop.name} - ${shop.distance.toFixed(0)} meters<br>`;
            });

            popup
                .setLatLng(e.latlng)
                .setContent(content)
                .openOn(map);

            renderShopsHTML(data);

        })
        .catch(error => {
            console.error('Error fetching distances:', error);
            popup
                .setLatLng(e.latlng)
                .setContent('Error fetching distances.')
                .openOn(map);
        });
}

map.on('click', onMapClick);

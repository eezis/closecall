// Incident Form Map - Google Maps integration for incident creation form
// This script provides the map widget for setting incident location

let map;
let marker;
let geocoder;

// Define initMap globally IMMEDIATELY so Google Maps can find it
window.initMap = function() {
    console.log('initMap called - initializing incident form map...');

    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', setupMap);
    } else {
        setupMap();
    }
};

function setupMap() {
    // Find the form and insert map container after the green alert box
    const alertBox = document.querySelector('.alert-success');
    if (!alertBox) {
        console.error('Could not find alert box to insert map after');
        return;
    }

    // Create map container elements
    const mapWrapper = document.createElement('div');
    mapWrapper.id = 'map-wrapper';
    mapWrapper.style.cssText = 'margin-bottom: 20px; padding: 15px; background: #f9f9f9; border: 1px solid #ddd; border-radius: 4px;';

    mapWrapper.innerHTML = `
        <label class="control-label" style="color: darkblue; font-size: 1.20em; font-weight: 400; display: block; margin-bottom: 10px;">
            Address where the incident occurred <span class="asteriskField" style="font-size: 1.40em; font-weight: 600; color: red;">*</span>
        </label>
        <input type="text" id="address-search"
               placeholder="Start typing an address (e.g., Olde Stage Rd, Boulder, CO)"
               class="form-control"
               style="margin-bottom: 15px; font-size: 1.1em;">
        <div id="incident-map" style="width: 100%; height: 400px; border: 2px solid #ddd; border-radius: 4px; margin-bottom: 10px;"></div>
        <div id="current-address" style="padding: 8px; background: #e8f5e9; border-radius: 4px; font-size: 0.95em; color: #2e7d32;"></div>
    `;

    // Insert after the alert box
    alertBox.parentNode.insertBefore(mapWrapper, alertBox.nextSibling);

    // Get the hidden address field
    const addressField = document.getElementById('id_address');
    if (!addressField) {
        console.error('Hidden address field (id_address) not found');
        return;
    }

    // Initialize geocoder
    geocoder = new google.maps.Geocoder();

    // Default coordinates (Boulder, CO)
    let initialLat = 40.0149856;
    let initialLng = -105.2705456;

    // Create the map
    const mapElement = document.getElementById('incident-map');
    map = new google.maps.Map(mapElement, {
        center: { lat: initialLat, lng: initialLng },
        zoom: 12,
        mapTypeId: 'roadmap',
        streetViewControl: false,
        mapTypeControl: true,
        mapTypeControlOptions: {
            style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
        }
    });

    // Create draggable marker
    marker = new google.maps.Marker({
        map: map,
        position: { lat: initialLat, lng: initialLng },
        draggable: true,
        animation: google.maps.Animation.DROP,
        title: 'Drag to incident location'
    });

    // Setup address search autocomplete
    const searchInput = document.getElementById('address-search');

    // Setup Places Autocomplete
    try {
        const autocomplete = new google.maps.places.Autocomplete(searchInput, {
            types: ['geocode', 'establishment'],
            fields: ['formatted_address', 'geometry', 'name']
        });

        // Bias results to map bounds
        autocomplete.bindTo('bounds', map);

        // Handle place selection from autocomplete
        autocomplete.addListener('place_changed', function() {
            const place = autocomplete.getPlace();

            if (!place.geometry || !place.geometry.location) {
                // User typed something but didn't select - try geocoding
                if (searchInput.value) {
                    geocodeAddress(searchInput.value);
                }
                return;
            }

            // Update map and marker
            if (place.geometry.viewport) {
                map.fitBounds(place.geometry.viewport);
            } else {
                map.setCenter(place.geometry.location);
                map.setZoom(17);
            }

            marker.setPosition(place.geometry.location);
            updateAddressField(place.formatted_address);
        });

        console.log('Places Autocomplete initialized successfully');
    } catch (e) {
        console.warn('Google Places Autocomplete not available:', e.message);
    }

    // Prevent form submission on Enter in search field
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            if (searchInput.value) {
                geocodeAddress(searchInput.value);
            }
        }
    });

    // Handle marker drag
    marker.addListener('dragend', function() {
        const pos = marker.getPosition();
        reverseGeocode(pos.lat(), pos.lng());
    });

    // Handle map click
    map.addListener('click', function(event) {
        marker.setPosition(event.latLng);
        reverseGeocode(event.latLng.lat(), event.latLng.lng());
    });

    console.log('Incident form map initialized successfully');
}

function geocodeAddress(address) {
    if (!geocoder) return;

    geocoder.geocode({ address: address }, function(results, status) {
        if (status === 'OK' && results[0]) {
            const location = results[0].geometry.location;
            map.setCenter(location);
            map.setZoom(17);
            marker.setPosition(location);
            updateAddressField(results[0].formatted_address);

            // Update search input with formatted address
            const searchInput = document.getElementById('address-search');
            if (searchInput) {
                searchInput.value = results[0].formatted_address;
            }
        } else {
            console.warn('Geocode failed: ' + status);
        }
    });
}

function reverseGeocode(lat, lng) {
    if (!geocoder) return;

    geocoder.geocode({ location: { lat, lng } }, function(results, status) {
        if (status === 'OK' && results[0]) {
            updateAddressField(results[0].formatted_address);

            // Update search input
            const searchInput = document.getElementById('address-search');
            if (searchInput) {
                searchInput.value = results[0].formatted_address;
            }
        }
    });
}

function updateAddressField(address) {
    // Update hidden form field
    const addressField = document.getElementById('id_address');
    if (addressField) {
        addressField.value = address;
    }

    // Update display
    const currentAddressDiv = document.getElementById('current-address');
    if (currentAddressDiv) {
        currentAddressDiv.innerHTML = '<strong>Selected location:</strong> ' + address;
    }

    console.log('Address updated:', address);
}

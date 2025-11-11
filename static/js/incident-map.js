// Google Maps incident location picker
let map;
let marker;
let geocoder;

async function initIncidentMap() {
    console.log('Initializing incident map...');

    // Ensure DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initIncidentMap);
        return;
    }

    // Wait a moment for crispy forms to finish rendering
    setTimeout(async () => {
        try {
            // Find the map container created by our custom template
            const mapElement = document.getElementById('incident-map');
            if (!mapElement) {
                console.error('Map container not found - template may not have rendered yet');
                // Try again in a moment
                setTimeout(initIncidentMap, 500);
                return;
            }

            console.log('Map container found:', mapElement);

            // Get form fields - they are hidden inputs
            const latField = document.getElementById('id_latitude') || document.querySelector('input[name="latitude"]');
            const lngField = document.getElementById('id_longitude') || document.querySelector('input[name="longitude"]');

            if (!latField || !lngField) {
                console.error('Latitude/longitude fields not found');
                console.log('Looking for id_latitude:', document.getElementById('id_latitude'));
                console.log('Looking for id_longitude:', document.getElementById('id_longitude'));
                console.log('Looking for name=latitude:', document.querySelector('input[name="latitude"]'));
                console.log('Looking for name=longitude:', document.querySelector('input[name="longitude"]'));
                return;
            }

            // Import required libraries
            const { Map } = await google.maps.importLibrary("maps");
            const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
            const { Autocomplete } = await google.maps.importLibrary("places");

            // Get initial coordinates
            let initialLat = parseFloat(latField.value) || 40.0149856;
            let initialLng = parseFloat(lngField.value) || -105.2705456;

            // Initialize the map
            map = new Map(mapElement, {
                center: { lat: initialLat, lng: initialLng },
                zoom: 13,
                mapTypeId: 'roadmap',
                streetViewControl: false,
                mapTypeControl: true,
                mapTypeControlOptions: {
                    style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
                },
                mapId: 'incident_map'
            });

            // Create marker
            marker = new AdvancedMarkerElement({
                map: map,
                position: { lat: initialLat, lng: initialLng },
                gmpDraggable: true,
                title: 'Incident Location'
            });

            // Initialize geocoder
            geocoder = new google.maps.Geocoder();

            // Setup address search with new Autocomplete API
            const searchInput = document.getElementById('address-search');
            if (searchInput) {
                setupAddressAutocomplete(searchInput);
            }

            // Handle marker drag
            marker.addListener('dragend', function(event) {
                const lat = event.latLng.lat();
                const lng = event.latLng.lng();
                updateCoordinates(lat, lng);
                reverseGeocode(lat, lng, searchInput);
            });

            // Handle map clicks
            map.addListener('click', function(event) {
                marker.position = event.latLng;
                updateCoordinates(event.latLng.lat(), event.latLng.lng());
                reverseGeocode(event.latLng.lat(), event.latLng.lng(), searchInput);
            });

            console.log('Map initialized successfully');

        } catch (error) {
            console.error('Error initializing map:', error);
        }
    }, 100);
}

function setupAddressAutocomplete(input) {
    // IMPORTANT: Using google.maps.places.Autocomplete (OLD Places API)
    // DO NOT change to PlaceAutocompleteElement - requires NEW Places API which is NOT enabled
    // The deprecation warning is expected and OK - Google gives 12+ months notice before changes
    const autocomplete = new google.maps.places.Autocomplete(input, {
        types: ['geocode', 'establishment'],
        fields: ['formatted_address', 'geometry', 'name']
    });

    // Bind to map bounds for better local results
    if (map) {
        autocomplete.bindTo('bounds', map);
    }

    // Listen for place selection
    autocomplete.addListener('place_changed', function() {
        const place = autocomplete.getPlace();

        if (!place.geometry || !place.geometry.location) {
            // User entered text that wasn't a suggestion - try geocoding
            console.log("No geometry for input, trying geocode: '" + input.value + "'");
            if (input.value) {
                geocodeAddress(input.value);
            }
            return;
        }

        // Update map view
        if (place.geometry.viewport) {
            map.fitBounds(place.geometry.viewport);
        } else {
            map.setCenter(place.geometry.location);
            map.setZoom(17);
        }

        // Set marker position
        marker.position = place.geometry.location;

        // Update coordinates
        updateCoordinates(
            place.geometry.location.lat(),
            place.geometry.location.lng()
        );
    });

    // Prevent form submission on Enter
    input.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
        }
    });
}

function geocodeAddress(address) {
    if (!geocoder) {
        console.error('Geocoder not initialized');
        return;
    }

    geocoder.geocode({ address: address }, function(results, status) {
        if (status === 'OK' && results[0]) {
            const location = results[0].geometry.location;
            map.setCenter(location);
            map.setZoom(17);
            marker.position = location;
            updateCoordinates(location.lat(), location.lng());
        } else {
            console.warn('Geocode was not successful: ' + status);
        }
    });
}

function reverseGeocode(lat, lng, input) {
    if (!geocoder || !input) return;

    geocoder.geocode({ location: { lat, lng } }, function(results, status) {
        if (status === 'OK' && results[0]) {
            input.value = results[0].formatted_address;
        }
    });
}

function updateCoordinates(lat, lng) {
    const latField = document.getElementById('id_latitude') || document.querySelector('input[name="latitude"]');
    const lngField = document.getElementById('id_longitude') || document.querySelector('input[name="longitude"]');

    if (latField) latField.value = lat.toFixed(6);
    if (lngField) lngField.value = lng.toFixed(6);

    // Update hidden address field if it exists
    const addressField = document.getElementById('id_address') || document.querySelector('input[name="address"]');
    if (addressField && geocoder) {
        geocoder.geocode({ location: { lat, lng } }, function(results, status) {
            if (status === 'OK' && results[0]) {
                addressField.value = results[0].formatted_address;
            }
        });
    }
}

// Set the callback for Google Maps
window.initIncidentMap = initIncidentMap;

// Also try to initialize if Google Maps is already loaded
if (typeof google !== 'undefined' && google.maps) {
    console.log('Google Maps already loaded, initializing...');
    initIncidentMap();
}
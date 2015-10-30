if (jQuery != undefined) {
    var django = {
        'jQuery': jQuery,
    }
}


(function($) {

    $(document).ready(function() {

        try {
            var _ = google;
        } catch (ReferenceError) {
            console.log('geoposition: "google" not defined.  You might not be connected to the internet.');
            return;
        }

        var mapDefaults = {
            'mapTypeId': google.maps.MapTypeId.ROADMAP,
            'scrollwheel': false,
            'streetViewControl': false,
            'panControl': false
        };

        var markerDefaults = {
            'draggable': true,
            'animation': google.maps.Animation.DROP
        };

        $('.geoposition-widget').each(function() {
            var $container = $(this),
                $mapContainer = $('<div class="geoposition-map" />'),
                // bottom of map, shows "official" address of the marker
                $addressRow = $('<div class="geoposition-address" />'),

                $searchRow = $('<div class="geoposition-search" />'),
                $searchInput = $('<input>', {'type': 'search', 'placeholder': 'Location of incident (Lee Hill Dr, Boulder, CO)'}),
                $latitudeField = $container.find('input.geoposition:eq(0)'),
                $longitudeField = $container.find('input.geoposition:eq(1)'),
                latitude = parseFloat($latitudeField.val()) || null,
                longitude = parseFloat($longitudeField.val()) || null,
                map,
                mapLatLng,
                mapOptions,
                mapCustomOptions,
                markerOptions,
                markerCustomOptions,
                marker;

            $mapContainer.css('height', $container.data('map-widget-height') + 'px');
            mapCustomOptions = $container.data('map-options') || {};
            markerCustomOptions = $container.data('marker-options') || {};
            // $('#div_id_position').attr('label', 'Location of Incident');

            function doSearch() {
                var gc = new google.maps.Geocoder();
                $searchInput.parent().find('ul.geoposition-results').remove();
                gc.geocode({
                    'address': $searchInput.val()
                }, function(results, status) {
                    if (status == 'OK') {
                        var updatePosition = function(result) {
                            if (result.geometry.bounds) {
                                map.fitBounds(result.geometry.bounds);
                            } else {
                                map.panTo(result.geometry.location);
                                map.setZoom(18);
                            }
                            marker.setPosition(result.geometry.location);
                            google.maps.event.trigger(marker, 'dragend');
                        };
                        if (results.length == 1) {
                            updatePosition(results[0]);
                        } else {
                            var $ul = $('<ul />', {'class': 'geoposition-results'});
                            $.each(results, function(i, result) {
                                var $li = $('<li />');
                                $li.text(result.formatted_address);
                                $li.on('click', function() {
                                    updatePosition(result);
                                    $li.closest('ul').remove();
                                });
                                $li.appendTo($ul);
                            });
                            $searchInput.after($ul);
                        }
                    }
                });
            }

            function doGeocode() {
                var gc = new google.maps.Geocoder();
                gc.geocode({
                    'latLng': marker.position
                }, function(results, status) {
                    $addressRow.text('');
                    if (results && results[0]) {
                        $addressRow.text(results[0].formatted_address);
                        // alert(results[0].formatted_address);
                        // MY MODIFICATION TO POPULATE HIDDEN FORM FIELD ADDRESS
                        $("#id_address").val(results[0].formatted_address);
                        // $('#id_position_0').attr('** need to change the "for" label', 'Location of Incident');
                    }
                });
            }


            var autoSuggestTimer = null;
            $searchInput.on('keydown', function(e) {
                if (autoSuggestTimer) {
                    clearTimeout(autoSuggestTimer);
                    autoSuggestTimer = null;
                }

                // if enter, search immediately
                if (e.keyCode == 13) {
                    e.preventDefault();
                    doSearch();
                }
                else {
                    // otherwise, search after a while after typing ends
                    autoSuggestTimer = setTimeout(function(){
                        doSearch();
                    }, 1000);
                }
            }).on('abort', function() {
                $(this).parent().find('ul.geoposition-results').remove();
            });
            $searchInput.appendTo($searchRow);
            $container.append($searchRow, $mapContainer, $addressRow);
            // $container.append($addressRow, $mapContainer, $searchRow);


            // 10.27.15 the map stopped working -- would not display from some people
            // was visible to me on 10.29.15
            // fix was here: https://github.com/philippbosch/django-geoposition/issues/55
            // no longer works with null, so will start it in CO
            //40.0293046,-105.2750825
            // had to adjust the Zoom as well mapOptions['zoom'] = 3;
            latitude = 40.0293046
            longitude = -105.27

            mapLatLng = new google.maps.LatLng(latitude, longitude);



            mapOptions = $.extend({}, mapDefaults, mapCustomOptions);

            if (!(latitude === null && longitude === null && mapOptions['center'])) {
                mapOptions['center'] = mapLatLng;
            }

            if (!mapOptions['zoom']) {
                // mapOptions['zoom'] = latitude && longitude ? 15 : 1;
                mapOptions['zoom'] = 3;
            }

            map = new google.maps.Map($mapContainer.get(0), mapOptions);
            markerOptions = $.extend({}, markerDefaults, markerCustomOptions, {
                'map': map
            });

            if (!(latitude === null && longitude === null && markerOptions['position'])) {
                markerOptions['position'] = mapLatLng;
            }

            marker = new google.maps.Marker(markerOptions);
            google.maps.event.addListener(marker, 'dragend', function() {
                $latitudeField.val(this.position.lat());
                $longitudeField.val(this.position.lng());
                doGeocode();
            });
            if ($latitudeField.val() && $longitudeField.val()) {
                google.maps.event.trigger(marker, 'dragend');
            }

            $latitudeField.add($longitudeField).on('keyup', function(e) {
                var latitude = parseFloat($latitudeField.val()) || 0;
                var longitude = parseFloat($longitudeField.val()) || 0;
                var center = new google.maps.LatLng(latitude, longitude);
                map.setCenter(center);
                map.setZoom(15);
                marker.setPosition(center);
                doGeocode();
            });
        });
    });
})(django.jQuery);

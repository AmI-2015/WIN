    function initialize() {
            var nearest;
            var zoom;
            if (typeof indexPage === 'undefined')
            {
                //set the center of the map to the middle of Politecnico
                nearest = new google.maps.LatLng(restrooms[0].lat, restrooms[0].long);
                zoom = 18;
            }
            else // if (indexPage == true)
            {
                // coordinate of nearest restroom  **selected by user**
                nearest = new google.maps.LatLng(45.06335, 7.660734);
                zoom = 17;
            }

            //set the center of the map to the nearest restroom
            var mapOptions = {
                zoom: zoom,
                center: nearest
            };

            var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
            var marker =[];
	        var infowindow =[];

	        function markerCallback(marker,content,infowindow) {
                return function() {
                    infowindow.setContent(content);
                    infowindow.open(map,marker);
                };
            }

            for (i = 0; i < restrooms.length; i++) {
                //position
                tempPosition = new google.maps.LatLng(restrooms[i].lat, restrooms[i].long);
                //set the color of markers
                if (restrooms[i].wc_available > restrooms[i].people_count && restrooms[i].status === 0)
                    color = 'g';
                else if (restrooms[i].wc_available == restrooms[i].people_count)
                    color = 'y';
                else
                    color = 'r';
                var image = '/static/images/' + restrooms[i].gender.toLowerCase() + color + ".png";

                //create marker
                marker = new google.maps.Marker({
                    position: tempPosition,
                    map: map,
                    title: restrooms[i].name,
                    icon: image
                });

                //create content window
                var contentString = restrooms[i].name + "<br>Toilets: " + (restrooms[i].wc_count - restrooms[i].wc_closed_count) +
                    "<br>People: " + restrooms[i].people_count + "<br>Status: " + restrooms[i].status_str;
                infowindow = new google.maps.InfoWindow();

                //create event in order to show info window
                google.maps.event.addListener(marker,'click', markerCallback(marker,contentString,infowindow));


                // add hallway overlay
                var imageBounds = new google.maps.LatLngBounds(
                        new google.maps.LatLng(45.060240762168780,7.654595375061035),
                        new google.maps.LatLng(45.066787985689180,7.664896811256426));
                var overlayOptions  = {clickable:false};
				var overlay = new google.maps.GroundOverlay(
				"http://www.polito.it/ateneo/sedi/images/sede_overlay.png", imageBounds, overlayOptions);
				overlay.setMap(map);
            }

        }
        google.maps.event.addDomListener(window, 'load', initialize);

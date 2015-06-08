    function initialize() {
            //coordinate of nearest restroom  **selected by user**
            var nearest = new google.maps.LatLng(restrooms[0].lat, restrooms[0].long);

            //set the center of the map to the nearest restroom
            var mapOptions = {
                zoom: 19,
                center: nearest
            }

            var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
            var marker =[];
	        var infowindow =[];
	    
            for (i = 0; i < restrooms.length; i++) {
                //position
                tempPosition = new google.maps.LatLng(restrooms[i].lat, restrooms[i].long);
                //set the color of markers
                if (restrooms[i].wc_available > 0)
                    color = 'g';
                else if (restrooms[i].wc_available == 0)
                    color = 'y';
                else
                    color = 'r';
                var image = '/static/images/' + defaultGender + color + ".png";

                //create marker
                marker = new google.maps.Marker({
                    position: tempPosition,
                    map: map,
                    title: restrooms[i].name,
                    icon: image
                })

                //create content window
                var contentString = restrooms[i].name + "<br>Toilets: " + (restrooms[i].wc_count - restrooms[i].wc_closed_count) + "<br>People: " + restrooms[i].people_count;
                infowindow = new google.maps.InfoWindow();

                //create event in order to show info window                
                google.maps.event.addListener(marker,'click', (function(marker,content,infowindow){ 
                    return function() {
                        infowindow.setContent(content);
                        infowindow.open(map,marker);
                    };
                })(marker,contentString,infowindow));
            };

        }
        google.maps.event.addDomListener(window, 'load', initialize);
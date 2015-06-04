    function initialize() {
            //coordinate of nearest restroom  **selected by user**
            var nearest = new google.maps.LatLng(45.06296, 7.66236);
            //gender to show  **selected by user**
            var defaultGender = 'f';
            //create an array containing data of all restrooms
            var restrooms = [];
            //add data of each restroom **peoplecount and toilets must be retrieved by db**
            restrooms.push({lat: 45.06296, lng: 7.66236, name: 'biblio',toilets: 2,peopleCount:3 , gender: defaultGender});
            restrooms.push({ lat: 45.06239, lng: 7.66203, name: 'ambrogio', toilets: 1, peopleCount: 1, gender: defaultGender });
            restrooms.push({ lat: 45.06244, lng: 7.66097, name: 'magna', toilets: 5, peopleCount: 3, gender: defaultGender });
            restrooms.push({ lat: 45.06208, lng: 7.66076, name: 'katia', toilets: 5, peopleCount: 2, gender: defaultGender });
            restrooms.push({ lat: 45.06410, lng: 7.66208, name: 'cla', toilets: 5, peopleCount: 4, gender: defaultGender });
            restrooms.push({ lat: 45.06444, lng: 7.66220, name: '12', toilets: 5, peopleCount: 2, gender: defaultGender });

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
                tempPosition = new google.maps.LatLng(restrooms[i].lat, restrooms[i].lng);
                //set the color of markers
                if (restrooms[i].toilets > restrooms[i].peopleCount)
                    color = 'g';
                else if (restrooms[i].toilets == restrooms[i].peopleCount)
                    color = 'y';
                else
                    color = 'r';
                var image = 'images/' + defaultGender + color + ".png";

                //create marker
                marker[i] = new google.maps.Marker({
                    position: tempPosition,
                    map: map,
                    title: restrooms[i].name,
                    icon: image
                })

                //create content window
                var contentString = restrooms[i].name + "<br>Toilets: " + restrooms[i].toilets + "<br>People: " + restrooms[i].peopleCount;
                infowindow[i] = new google.maps.InfoWindow({
                    content: contentString
                });

                //create event in order to show info window
                google.maps.event.addListener(marker[i], 'click', function () {
                    infowindow[i].open(map, marker[i]);
                });

            };

            

        }
        google.maps.event.addDomListener(window, 'load', initialize);
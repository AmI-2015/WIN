$(document).ready(function() {
	$("#typeofroom").load(function() {
		$("#typeofroom").change();
	});

	$("#typeofroom").change(function() {
		$("#selectRoomForm").css("display", "block");
		$.getJSON("/placeType/"+ $("#typeofroom").val(), function(result) {
			var select = $("#selectroom");
			select.empty();
			$.each(result.rooms, function(index, value) {
				select.append($("<option />").val(value.id).text(value.name));
			});
			select.val('');
		});
	});

	$("#find").click(function() {
		var id = $("#selectroom").val();
		if (id !== null) {
			window.location = "/place/" + $("#selectroom").val() + "/" + $("input[name='gender']:checked").val() + "/";
		}
	});

	$("#selectroom").change(function() {
		$("#findForm").css("display", "block");
	});

	// Add checkbox event handler for map markers
	$("input[name='gender']").change(function() {
		var checked = $("input[name='gender']:checked").val();
		// Clear markers
		if (checked == 'M') {
			setAllMap(null, markerF);
			setAllMap(map, markerM);
		}
		else {
			setAllMap(null, markerM);
			setAllMap(map, markerF);
		}
	});
});

/* add class 'active' to nav item */
$(document).ready(function() {
    var path = location.pathname; 
	if (path == "/") {
		$(".navbar-nav li:nth-child(1)").addClass("active");
	} 
    if (path == "/about") {
		$(".navbar-nav li:nth-child(2)").addClass("active");
	} 
    
});

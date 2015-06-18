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

	/* add class 'active' to nav item */
	if (location.pathname.substring(1) == "index") {
		$(".navbar-nav li:nth-child(1)").addClass("active");
	} else if (location.pathname.substring(1) == "about") {
		$(".navbar-nav li:nth-child(2)").addClass("active");
	} else if (location.pathname.substring(1) == "contact") {
		$(".navbar-nav li:nth-child(3)").addClass("active");
	}

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
	// Force change at page load
	$("input[name='gender']").change();
});

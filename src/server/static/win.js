$(document).ready(function() {
	$("#typeofroom").load(function() {
		$("#typeofroom").change()
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

});


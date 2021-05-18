$(document).ready(function() {
	$("#save-button").click(function() {		
		var serializedData = $("#profile-settings-form").serialize();
		$.ajax({
			url: $("profile-settings-form").data("url"),
			data: serializedData,
			type: "post"
		})
	});
});
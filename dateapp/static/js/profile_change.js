$(document).ready(function() {
	$("#save-info-button").click(function() {		
		var serializedData = $("#profile-change-form").serialize();
		$.ajax({
			url: $('profile-change-form').data('url'),
			data: serializedData,
			type: 'post'
		})
	});
});
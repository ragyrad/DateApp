$(document).ready(function() {
	var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
	$("#read-matches").click(function() {
		var user_id = JSON.parse(document.getElementById('user_id').textContent);
		$.ajax({
			url: "/notifications/" + user_id + "/read_all/",
			data: {
				csrfmiddlewaretoken: csrfToken,
				id: user_id
			},
			type: 'post',
			success: function() {
				notifications = document.getElementsByClassName('list-group-item-dark');
				$.each(notifications, function() {
					$(this).css('background', '#fff');
				});
				$("#notification-counter").hide();
			}
		})
	});
});
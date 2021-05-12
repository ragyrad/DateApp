$(document).ready(function() {

	function getCookie(name) {
	    let cookieValue = null;
	    if (document.cookie && document.cookie !== '') {
	        const cookies = document.cookie.split(';');
	        for (let i = 0; i < cookies.length; i++) {
	            const cookie = cookies[i].trim();
	            // Does this cookie string begin with the name we want?
	            if (cookie.substring(0, name.length + 1) === (name + '=')) {
	                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                break;
	            }
	        }
	    }
	    return cookieValue;
	}
	

	var csrfToken = getCookie('csrftoken');
	$("#read-matches").click(function() {
		var user_id = JSON.parse(document.getElementById('user_id').textContent);
		$.ajax({
			url: "/notifications/read_all/",
			data: {
				csrfmiddlewaretoken: csrfToken,
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
$(document).ready(function() {
	console.log('test1')
	$("#upload-photo-button").click(function() {		
		var serializedData = $("#upload-photo-form").serialize();
		console.log('test2')
		$.ajax({
			url: $('upload-photo-form').data('url'),
			data: serializedData,
			type: 'post',
			success: function(response){
				console.log('Upload done!')
			}
		})
	});
});
$(document).ready(function(){
	$("#overview img").tooltip({'placement': 'left'});
	$("#overview .panel-heading").tooltip({'placement': 'left'});
	$(".progress").tooltip({'placement': 'left'});

	$('html, body').animate({
		scrollTop: $('#anchor').offset().top
	}, 800);

	$('.progress-bar').each(function() {
		var percent = $(this).attr('value')
		$(this).animate({
			width: percent
		}, 2000);
	});


});

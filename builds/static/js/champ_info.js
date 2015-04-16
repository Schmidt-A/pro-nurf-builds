$(document).ready(function(){
	var animated = false;

	$("#overview img").tooltip({'placement': 'left'});
	$("#overview .panel-heading").tooltip({'placement': 'left'});
	$(".progress").tooltip({'placement': 'left'});

	$('html, body').animate({
		scrollTop: $('#anchor').offset().top
	}, 800);


	table = $('.table').stupidtable();

	table.on("aftertablesort", function (event, data) {
		var th = $(this).find("th");
		th.find(".arrow").remove();
		var dir = $.fn.stupidtable.dir;
		var arrow = data.direction === dir.ASC ? "&uarr;" : "&darr;";
		th.eq(data.column).append('<span class="arrow">' + arrow +'</span>');
	});

        table.find('thead th').eq(1).stupidsort();

	$('.progress-bar-champ').each(function() {
		var percent = $(this).attr('value')
		$(this).animate({
			width: percent
		}, 2000);
	});

	$('#items_tab').click(function(){
		if(animated == false) {
			animated == true;
			$('.progress-bar-item').each(function() {
				var percent = $(this).attr('value')
				$(this).animate({
					width: percent
				}, 1000);
			});
		}
	});
				
});

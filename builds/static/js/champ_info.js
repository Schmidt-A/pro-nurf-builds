$(document).ready(function(){
        // ******************
        // Tooltip setup
        // ******************
        item_tooltip_html = [
                '<div class="tooltip item_tooltip" role="tooltip">',
                '<div class="tooltip-arrow"></div>',
                '<div class="tooltip-inner"></div>',
                '</div>'].join('');

        $("#urf-tab-div .item_icon").tooltip({
            'placement': 'left', 
            'container': 'body',
            'html': true,
            'template': item_tooltip_html
        });

	$("#overview .build_icon").tooltip({'placement': 'left', 'container': 'body'});
	$("#overview .panel-heading").tooltip({'placement': 'left'});
	$(".progress").tooltip({'placement': 'left'});

        $('#urf-tab-div .item_icon').mouseover(function() {
                console.log('test')
                img = $(this).attr('src')
                name = $(this).attr('i_name')
                desc = $(this).attr('i_desc')
                console.log(desc)

                content = [
                        '<div class="row">',
                        '<div class="col-md-3">',
                        '<img src="' + img + '"></img>',
                        '</div>',
                        '<div class="col-md-9">',
                        '<span><b>' + name + '</b><br>' + desc + '</span>',
                        '</div>',
                        '</div>'
                ].join('');

                $(this).attr('data-original-title', content);
                $(this).tooltip('fixTitle').tooltip('show');

        });

        // ******************

        // Move screen down to Champion title
	$('html, body').animate({
		scrollTop: $('#anchor').offset().top
	}, 800);

        // Animate champ stats bars
	$('.progress-bar-champ').each(function() {
		var percent = $(this).attr('value')
		$(this).animate({
			width: percent
		}, 2000);
	});


        // ******************
        // Item breakdown tab
        // ******************
	animated = false;
	table = $('.table').stupidtable();
        table.find('thead th').eq(1).stupidsort();

	table.on("aftertablesort", function (event, data) {
		var th = $(this).find("th");
		th.find(".arrow").remove();
		var dir = $.fn.stupidtable.dir;
		var arrow = data.direction === dir.ASC ? "&uarr;" : "&darr;";
		th.eq(data.column).append('<span class="arrow">' + arrow +'</span>');
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
        // ******************
				
});

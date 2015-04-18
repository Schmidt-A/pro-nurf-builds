$(document).ready(function(){
	$('.img').hover(function(){
		  $(this).toggleClass('hover');
	});

        $('#about_link').click(function(e){
                  $("#about").modal('show');
        });
});

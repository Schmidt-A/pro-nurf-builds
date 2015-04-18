$(document).ready(function(){

        var end = $('#counter').attr('value')
        $({someValue: 0}).animate({someValue: end}, {
                duration: 2000,
                easing:'swing', // can be anything
                step: function() { // called on every step
                        // Update the element's text with rounded-up value:
                        $('#counter').text(Math.round(this.someValue));
                },
		complete: function() {
                        $('#counter').text(end);
		}
        });
});

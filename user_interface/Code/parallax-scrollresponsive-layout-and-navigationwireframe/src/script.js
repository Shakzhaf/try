$(document).ready(function(){
	
	$('.mobile-icon').click( function() {
		$('nav ul').toggleClass("showing");

	});
  
  //disappear nav when a attribute is clicked
	$('nav ul li a').click( function() {
		$('nav ul').toggleClass("showing");
		
	});
  
//parallexscrolling

    $('a.page-scroll').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top - 150
        }, 1500, 'easeInOutExpo');
        event.preventDefault();
    });

});




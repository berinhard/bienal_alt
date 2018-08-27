CAROUSEL_SELECTOR_ID = "#image-carousel"


var getEnabled = function(){
    return $(".carousel_element.active")
}

var hideAndDisplay = function(to_hide, to_display) {
    to_hide.removeClass('active');
    to_display.addClass('active');
}

var displayToPrevious = function(current){
    var prev = current.prev();
    if (prev.length) {
        hideAndDisplay(current, prev)
    }
}

var displayToNext = function(current){
    var next = current.next();
    if (next.length) {
        hideAndDisplay(current, next)
    }
}


var refreshCarousel = function(url){
    $.get(url, displayCarousel);
}


var displayCarousel = function(data){
    console.log('oh o pai');
    $(CAROUSEL_SELECTOR_ID).html(data)

    $(".carousel_text_nav .prev").click(function(){
        var current = getEnabled();
        displayToPrevious(current);
    });
    $(".carousel_text_nav .next").click(function(){
        var current = getEnabled();
        displayToNext(current);
    });
}

$(document).ready(function(){
    $('.text_content a').click(function() {
        window.open($(this).attr('href'));
        return false;
    });

    var carouselDiv = $(CAROUSEL_SELECTOR_ID);
    if (carouselDiv.length >= 1) {
        refreshCarousel(carouselDiv.attr('url'));
    }
});

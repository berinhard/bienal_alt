CAROUSEL_SELECTOR_ID = "#image-carousel"
YEAR_FILTER_ID = "#year-filter"


var getEnabled = function(){
    return $(".carousel_element.active")
}

var hideAndDisplay = function(to_hide, to_display) {
    to_hide.removeClass('active');
    to_display.addClass('active');
    var img = to_display.find('.carousel_image')[0];
    resizeCarouselImageDimension(img);
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
    $(CAROUSEL_SELECTOR_ID).html(data)
    $(CAROUSEL_SELECTOR_ID).show()
    $(YEAR_FILTER_ID).hide()

    var first = $('div[data-position="1"]');
    hideAndDisplay(first, first)

    $(".carousel_text_nav .prev").click(function(){
        var current = getEnabled();
        displayToPrevious(current);
    });
    $(".carousel_text_nav .next").click(function(){
        var current = getEnabled();
        displayToNext(current);
    });
}

var resizeCarouselImageDimension = function(image){
    var width = image.width;
    var height = image.height;
    var is_landscape = width > height;

    if (is_landscape){
        image.className = image.className + ' landscape';
    } else {
        image.className = image.className + ' portrait';
    }

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

    $(".refresh-carousel").click(function(){
        var link = $(this)
        refreshCarousel(link.attr('url'));
    });

    $(".nav").click(function(){
        var link = $(this)
        link.siblings().each(function(){
            $(this).removeClass('active');
        });
        link.addClass('active');
    });

    $('#year-filter-btn').click(function(){
        $(CAROUSEL_SELECTOR_ID).hide();
        $(YEAR_FILTER_ID).show();
    });
});

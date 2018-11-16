CAROUSEL_SELECTOR_ID = "#image-carousel"
YEAR_FILTER_ID = "#year-filter"


var getEnabled = function(){
    return $(".carousel_element.active")
}

var hideAndDisplay = function(to_hide, to_display, add_hash=true) {
    to_hide.removeClass('active');
    to_display.addClass('active');
    var imgs = to_display.find('img[data-src]');

    $.each(imgs, function(index, img) {
      img.setAttribute('src', img.getAttribute('data-src'));
      img.style.visibility = 'hidden';
      img.onload = function() {
        img.removeAttribute('data-src');
        resizeCarouselImageDimension(img);
        img.style.visibility = 'visible';
      };
    });
    if (add_hash){
        location.href = '#' + to_display.attr('id');
    }

}

var displayToPrevious = function(current, add_hash=true){
    displayTo(current, current.prev());
}

var displayToNext = function(current, add_hash=true){
    displayTo(current, current.next());
}

var displayTo = function(current, next, add_hash=true){
    if (next.length) {
        hideAndDisplay(current, next, add_hash=add_hash);
    }
}

var previous = function(){
    var current = getEnabled();
    displayToPrevious(current);
};

var next = function(){
    var current = getEnabled();
    displayToNext(current);
};

var refreshCarousel = function(url){
    $.get(url, displayCarousel);
}


var displayCarousel = function(data){
    $(CAROUSEL_SELECTOR_ID).html(data)
    $(CAROUSEL_SELECTOR_ID).show()
    $(YEAR_FILTER_ID).hide()

    url = location.href
    var hash = url.substring(url.indexOf("#") + 1);
    var first = $('div[data-position="1"]');

    if (hash.length && hash != url) {
        hash = '#' + hash;
        var current = $(hash);
        if (current.length >= 1) {
            hideAndDisplay(current, current, add_hash=false);
        } else {
            hideAndDisplay(first, first, add_hash=false);
        }
    } else {
        hideAndDisplay(first, first, add_hash=false);
    }

    $(".carousel_text_nav .prev").click(function(){previous();});
    $(".carousel_text_nav .next").click(function(){next();});

    $("body").keydown(function(e) {
      console.log('key');
      // left
      if(e.keyCode == 37) {previous();}
      // right
      else if(e.keyCode == 39) {next();}
    });
}

var resizeCarouselImageDimension = function(image){
    var width = image.width;
    var height = image.height;
    var is_landscape = width > height;
    var has_min_diff = (width - height) > 150;

    if (is_landscape && has_min_diff){
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

    var imgs = $('.action_content').find('img');

    $.each(imgs, function(index, img) {
        resizeCarouselImageDimension(img);
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


    var modal = $('#myModal');
    var modalImg = $("#img01");
    var captionText = $("#caption");
    $(".onModal").click(function(){
        var img = $(this).attr('src');
        console.log(img);

        modal.css({'display': 'block'});

        modalImg.attr('src', img);
    });

    $(".close").click(function(){
        modal.css({'display': 'none'});
    });
});

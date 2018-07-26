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

$(document).ready(function(){
    $(".carousel_text_nav .prev").click(function(){
        var current = getEnabled();
        displayToPrevious(current);
    });
    $(".carousel_text_nav .next").click(function(){
        var current = getEnabled();
        displayToNext(current);
    });
});

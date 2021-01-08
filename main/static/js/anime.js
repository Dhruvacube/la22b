function addclassfnc(x) {
    if (x.matches) { // If media query matches
        $('.bx').addClass("bxs-down-arrow-alt");
        $('.bx').removeClass("bxs-right-arrow-alt");
        $('.bx').removeClass("bx-fade-left");
        $('#mt-5').removeClass("mt-5");
        $('.bx').addClass("bx-fade-down");
    } else {
        $('.bx').removeClass("bxs-down-arrow-alt");
        $('.bx').removeClass("bx-fade-down");
        $('.bx').addClass("bxs-right-arrow-alt");
        $('#mt-5').addClass("mt-5");
        $('.bx').addClass("bx-fade-left");
    }
}

var x = window.matchMedia("(max-width: 767px)")
addclassfnc(x) // Call listener function at run time
x.addListener(addclassfnc) // Attach listener function on state changes

jQuery(document).ready(function($) {
    if (x.matches) { // If media query matches
        $('.bx').addClass("bxs-down-arrow-alt");
        $('.bx').addClass("bx-fade-down");
    } else {
        $('.bx').addClass("bxs-right-arrow-alt");
        $('#mt-5').addClass("mt-5");
        $('.bx').addClass("bx-fade-left");
    }
});
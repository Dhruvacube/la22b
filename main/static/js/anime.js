function addclassfnc(x) {
    if (x.matches) { // If media query matches
        $('#arrowbx').addClass("bxs-down-arrow-alt");
        $('#arrowbx').removeClass("bxs-right-arrow-alt");
        $('#arrowbx').removeClass("bx-fade-left");
        $('#mt-5').removeClass("mt-5");
        $('#arrowbx').addClass("bx-fade-down");
    } else {
        $('#arrowbx').removeClass("bxs-down-arrow-alt");
        $('#arrowbx').removeClass("bx-fade-down");
        $('#arrowbx').addClass("bxs-right-arrow-alt");
        $('#mt-5').addClass("mt-5");
        $('#arrowbx').addClass("bx-fade-left");
    }
}

var x = window.matchMedia("(max-width: 767px)")
addclassfnc(x) // Call listener function at run time
x.addListener(addclassfnc) // Attach listener function on state changes

jQuery(document).ready(function($) {
    if (x.matches) { // If media query matches
        $('#arrowbx').addClass("bxs-down-arrow-alt");
        $('#arrowbx').addClass("bx-fade-down");
    } else {
        $('.bx').addClass("bxs-right-arrow-alt");
        $('#mt-5').addClass("mt-5");
        $('#arrowbx').addClass("bx-fade-left");
    }
});
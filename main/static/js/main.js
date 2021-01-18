(function() {
    'use strict'

    document.querySelector('[data-bs-toggle="offcanvas"]').addEventListener('click', function() {
        document.querySelector('.offcanvas-collapse').classList.toggle('open')
    })
})()

function bell_loader() {
    $('#bell').addClass('d-none');
    $('#loader').removeClass('d-none');
    setTimeout(function() {
        location.replace($('#bell').attr('url'));
    }, 2000);
}
function load_loader(number) {
    $('#link' + number).addClass('d-none');
    $('#loader' + number).removeClass('d-none');
    location.replace($('#link').attr('href'));
}
function form_submit() {
    $('#confirmationmodal').modal('hide');
    $('#loadingmodal').modal('show');
    setTimeout(function() {
        $('#confessionform').submit();
    }, 4000);
};

function show_confirmation_form() {
    var confession_input = $('#confession_input');
    if (!confession_input.val() || confession_input.val().length === 0 || confession_input.val() == ' ' || confession_input.val() === ' ') {
        $('#warning_confession').removeClass('d-none');
    } else {
        $('#warning_confession').addClass('d-none');
        $('#confirmationmodal').modal('show');
    }
}
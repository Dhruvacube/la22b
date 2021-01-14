$(document).ready(function() {
    $('#google-forms').children().attr({ 'target': '_blank', 'rel': 'noopener noreferrer' });
    $('#strongele').removeAttr('target');
    $('#strongele').removeAttr('rel');
});
$(document).ready(function() {
    //change selectboxes to selectize mode to be searchable
    $("#id_name").select2();
    $('#id_student_models').select2();
});

function form_submit() {
    $('#confirmationmodal').modal('hide');
    $('#loadingmodal').modal('show');
    setTimeout(function() {
        $('#removenameform').submit();
    }, 4000);
};

function show_confirmation_form() {
    var select_input = $('#id_student_models');
    console.log(select_input.val())
    if (select_input.val() == undefined || select_input.val() == null || select_input.val() == '---------' || select_input.val() == '' || select_input.val() == ' ') {
        $('#nonewarning').removeClass('d-none');
    } else {
        $('#confirmationmodal').modal('show');
    }
}
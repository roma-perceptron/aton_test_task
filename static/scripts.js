/* scripts */

$(document).ready(function(){
    $('.form-select').change(function(){
        update_status(this.id, this.value, this.getAttribute('aria-label'));
    });
});

function set_auth_params(manager, form){
    login_form.inputLogin.value = manager.id;
    login_form.inputPassword.value = "admin";
}

function update_status(customer_id, status, back_status){
    $('#loadingModal').modal('show');
    $.ajax({
        url: `api/update_status?id=${customer_id}&status=${status}&back_status=${back_status}`,
        type: 'GET',
        success: update_status_callback
    });
}

function update_status_callback(data){
    setTimeout(function(){
        $('#loadingModal').modal('hide');
    }, 500);

    if(data.ok) $(`#${data.id}`).attr('aria-label', data.status_rus);
    else {
        $(`#${data.id}`).val(data.back_status);
        // показ уведомления об ошибке
        var toast = document.querySelector('.toast');
        var bsToast = new bootstrap.Toast(toast);
        bsToast.show();
    }
}

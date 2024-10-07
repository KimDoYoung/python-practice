
$(document).ready(function() {

    //toast 에러메세지 표시
    function showToastError(error) {
        const statusCode = error.status;
        const detail = error.detail || error.message;
        $('#toastError').find('#error-status-code').text(statusCode);
        $('#toastError').find('#error-detail').text(detail);
        var toast = new bootstrap.Toast(document.getElementById('toastError'));
        $('.toast').toast({
                animation: false,
                delay: 1000
            });
        $('.toast').toast('show');
    }
    //alsert 에러메세지 표시
    function showAlertError(error) {
        const statusCode = error.status;
        const detail = error.detail || error.message;
        const $alert = $('#alertError')
        $alert.find('#alertErrorStatus').text(statusCode);
        $alert.find('#alertErrorMessage').text(detail);
        $alert.removeClass('d-none');
        setTimeout(() => {
            $alert.addClass('d-none');
        }, 5000);
    }
});
// TODO 주기적으로 router를 호출하여 세션을 체크하고, 만료되면 로그아웃 처리

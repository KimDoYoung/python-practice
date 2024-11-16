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
    //alert 에러메세지 표시
    function showAlertError(error, stopAutoHide = false) {
        const statusCode = error.status;
        const detail = error.detail || error.message;
        const $alert = $('#alertError')
        $alert.find('#alertErrorStatus').text(statusCode);
        $alert.find('#alertErrorMessage').text(detail);
        $alert.removeClass('d-none');
        if (!stopAutoHide){
            setTimeout(() => {
                $alert.addClass('d-none');
            }, 5000);
        }
    }
    //alert 에러메세지 표시
    function showAlertMessage(message) {
        const $alert = $('#alertMessageArea')
        $alert.find('#alertMessage').text(message);
        $alert.removeClass('d-none');
        setTimeout(() => {
            $alert.addClass('d-none');
        }, 5000);
    }
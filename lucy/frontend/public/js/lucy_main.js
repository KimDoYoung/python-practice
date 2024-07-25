$(document).ready(function() {

    let canvasElm = document.getElementById('offcanvasBuySell');
    const offcanvasBuySell = new bootstrap.Offcanvas(canvasElm, {
            // backdrop: 'static',
            // keyboard: false
    });
    //offcanvas가 보여질때 증권사를 선택
    $('#offcanvasBuySell').on('shown.bs.offcanvas', function(){
        const stk_abbr = $('#page_path').val() ;
        const stk_company = String(stk_abbr);
        if(stk_company.startsWith('kis')){
            $('#kisorls1').prop('checked', true);
        }else if(stk_company.startsWith('ls')){
            $('#kisorls2').prop('checked', true);
        }
    })
    //offcanvas를 보이게 하는 함수
    function showBuySellCanvas(stk_company, stk_code, stk_name, which, qty, cost){
        if(qty === undefined) qty = 1;
        if(cost === undefined) cost = 0;
        console.log('btnTest clicked');
        debugger;
        if(stk_company == 'KIS'){
            $('#kisorls1').prop('checked', true);
        }else if(stk_company == 'LS'){
            $('#kisorls2').prop('checked', true);
        }else{
            $('#kisorls1').prop('checked', false);
            $('#kisorls2').prop('checked', false);
        }
        $('#buy-form').find('input[name="pdno"]').val(stk_code);
        $('#buy-form').find('input[name="pdnm"]').val(stk_name);
        $('#buy-form').find('input[name="qty"]').val(qty);
        $('#buy-form').find('input[name="cost"]').val(cost);
        $('#sell-form').find('input[name="pdno"]').val(stk_code);
        $('#sell-form').find('input[name="pdnm"]').val(stk_name);
        $('#sell-form').find('input[name="qty"]').val(qty);
        $('#sell-form').find('input[name="cost"]').val(cost);
        if (which === '매수') {
            $('#sell-form').find('input').val('');
            $('#sell-form').find('input, button, select, textarea').prop('disabled', true);
            $('#buy-form').find('input, button, select, textarea').prop('disabled', false);
        } else if (which === '매도'){
            $('#buy-form').find('input').val('');
            $('#sell-form').find('input, button, select, textarea').prop('disabled', false);
            $('#buy-form').find('input, button, select, textarea').prop('disabled', true);
        }else{
            $('#sell-form').find('input, button, select, textarea').prop('disabled', false);
            $('#buy-form').find('input, button, select, textarea').prop('disabled', false);
        }
        // debugger;;
        offcanvasBuySell.toggle();
    }
    //toast 에러메세지 표시
    function showToastError(error) {
        const statusCode = error.status;
        const detail = error.detail;
        $('#toastError').find('#error-status-code').text(statusCode);
        $('#toastError').find('#error-detail').text(detail);
        var toast = new bootstrap.Toast(document.getElementById('toastError'));
        $('.toast').toast({
                animation: false,
                delay: 1000
            });
        $('.toast').toast('show');
    }
    //global functions
    window.showBuySellCanvas = showBuySellCanvas;
    window.showToastError = showToastError;
    //로그아웃
    $('#logout').click(function() {
        localStorage.removeItem('lucy_token');  // JWT 토큰 삭제
        removeCookie('lucy_token');
        fetch('/logout', {
            method: 'GET'
        }).then(function(response) {
            if (response.ok) {
                location.href = '/login';
            }
        });
    });
    //매수/매도 초기화
    $('.btnClearBuySell').on("click", function() {
        let $form = $(this).closest('form')
        $form.find('input').val('');
    });
    //매수/매도 API 호출
    function order_cash(stk_company,data){
        var url = '';
        debugger;
        if(stk_company === 'KIS'){
            url = '/api/v1/kis/order-cash';
        }else if(stk_company === 'LS'){
            url = '/api/v1/ls/order';
        }else{
            alert('증권사를 선택해주세요.');
            return;
        }

        postFetch(url, data)
            .then(data => {
                console.log(data);
                if(data.msg1){
                    alert(data.msg1);
                }
                debugger;
                var page_path = $('#page_path').val();
                if(page_path === '/main'){
                    window.location.href = '/main'
                }else{
                    window.location.href = `/page?path=${page_path}`;
                }
            }).catch(error => {
                console.error(error);
                $('#buy-sell-message-area').html(error)
            });
    }

    //매수 Form Submit 
    $('#buy-form').on('submit', function(e){
        e.preventDefault();
        console.log('click 매수.... ');
        const stk_company = $('input[name="kisorls"]:checked').val();
        if(!stk_company){
            alert('증권사를 선택해주세요.');
            return;
        }

        const stk_code = $('#buy-form input[name=pdno]').val();
        const qty = $('#buy-form input[name=qty]').val();
        const cost = $('#buy-form input[name=cost]').val();
        let msg = '';
        if( cost == 0){
            msg = '시장가로 매수하시겠습니까?';
        }else{
            msg = `지정가 ${cost}로 매수하시겠습니까?`;
        }
        if(!confirm(msg)) return;
        
        const data = {
            buy_sell_gb : '매수',
            stk_code: stk_code,
            qty: Number(qty),
            cost: Number(cost)
        }
        order_cash(stk_company, data);
    });
    //매도 Form Submit
    $('#sell-form').on('submit', function(e){
        e.preventDefault();
        console.log('click 매도.... ');
        const stk_company = $('input[name="kisorls"]:checked').val();
        if(!stk_company){
            alert('증권사를 선택해주세요.');
            return;
        }
        
        const stk_code = $('#sell-form input[name=pdno]').val();
        const qty = $('#sell-form input[name=qty]').val();
        const cost = $('#sell-form input[name=cost]').val();
        let msg = '';
        if( cost == 0){
            msg = '시장가로 매도하시겠습니까?';
        }else{
            msg = `지정가 ${cost}로 매도하시겠습니까?`;
        }        
        if(!confirm(msg)) return;    
        const data = {
            buy_sell_gb : '매도',
            stk_code: stk_code,
            qty: Number(qty),
            cost: Number(cost)
        }
        
        order_cash(stk_company, data);
    })        
});

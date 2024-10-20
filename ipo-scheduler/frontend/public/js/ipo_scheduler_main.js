
$(document).ready(function() {

    let canvasElm = document.getElementById('offcanvasBuySell');
    const offcanvasBuySell = new bootstrap.Offcanvas(canvasElm, {
            // backdrop: 'static',
            // keyboard: false
    });
    let offCanvasCompanyElm = document.getElementById('offcanvasCompany');
    const offcanvasCompany = new bootstrap.Offcanvas(offCanvasCompanyElm, {
            // backdrop: 'static',
            // keyboard: false
    });    
    $('#offcanvasCompany').on('shown.bs.offcanvas', function(){
        console.log("회사정보 canvas가 보여질때");
    });
    //매수/매도offcanvas가 보여질때 증권사를 선택
    $('#offcanvasBuySell').on('shown.bs.offcanvas', function(){
        const stk_abbr = $('#page_path').val() ;
        const stk_company = String(stk_abbr);
        if(stk_company.startsWith('kis')){
            $('#kisorls1').prop('checked', true);
        }else if(stk_company.startsWith('ls')){
            $('#kisorls2').prop('checked', true);
        }
    })
    /**
     * 하단에 offcanvas로 회사정보를 보여준다.
     * 
     * @param {*} stk_code 
     */
    function showCompanyCanvas(stk_code){
        const url = '/api/v1/mystock/company-info/' + stk_code;
        getFetch(url).then(data => {
            console.log(data); 
            const name_code = data.naver.stk_name + ' (' + data.naver.stk_code + ')';
            const $companyCanvas = $('#offcanvasCompany');
            $companyCanvas.find('#offcanvasCompanyName').text(name_code);
            $companyCanvas.find('#offcanvas-naver-company-summary').text(data.naver.company_summary);
            $companyCanvas.find('#offcanvas-naver-market-cap').text(data.naver.market_cap);
            $companyCanvas.find('#offcanvas-naver-market-cap-rank').text(data.naver.market_cap_rank);
            $companyCanvas.find('#offcanvas-naver-num-of-shares').text(data.naver.num_of_shares);
            //현재가
            let price_data = data.current_price.output;
            $companyCanvas.find('#offcanvas-stck_prpr').text(JuliaUtil.displayMoney(price_data.stck_prpr));
            $companyCanvas.find('#offcanvas-prdy_vrss').text(JuliaUtil.displayMoney(data.current_price.output.prdy_vrss));
            $companyCanvas.find('#offcanvas-prdy_ctrt').text(data.current_price.output.prdy_ctrt);
            $companyCanvas.find('#offcanvas-acml_vol').text(JuliaUtil.displayMoney(data.current_price.output.acml_vol));
            $companyCanvas.find('#offcanvas-acml_tr_pbmn').text(moneyFormat(data.current_price.output.acml_tr_pbmn));
            //candle chart
            const chart_data = data.price_history.output;
            let columns = [];
            let columns1 = ['data1'];
            let columns2 = ['x'];
            //시가,고가,저가,종가
            // debugger;
            for (let i = chart_data.length - 1; i >= 0; i--) {
                let item = chart_data[i];
                columns1.push([Number(item.stck_oprc), Number(item.stck_hgpr), Number(item.stck_lwpr), Number(item.stck_clpr)]);
                columns2.push(item.stck_bsop_date);
            }
            let start_ymd = columns2[1].substring(0, 4) + '-' + columns2[1].substring(4, 6) + '-' + columns2[1].substring(6, 8);
            let end_ymd = columns2[chart_data.length-1].substring(0, 4) + '-' + columns2[chart_data.length-1].substring(4, 6) + '-' + columns2[chart_data.length-1].substring(6, 8);
            let x_name = `${data.naver.stk_name} (${start_ymd}~${end_ymd})`;
            columns.push(columns1);
            //columns.push(columns2);
            
            offcanvasCompany.toggle();
            create_billboard_candle_chart("offcanvas_daily_chart",columns, x_name)
        }).catch(error=> {
            console.error(error.message); 
            showAlertError(error);
        });
        
    }
    //매수/매도offcanvas를 보이게 하는 함수
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
    //----------------------------------------------------------------
    // global functions
    //----------------------------------------------------------------
    window.showBuySellCanvas = showBuySellCanvas;
    window.showToastError = showToastError;
    window.showCompanyCanvas = showCompanyCanvas;
    window.showAlertError = showAlertError;
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
                }else if(data.rsp_msg){
                    alert(data.rsp_msg);
                }
                offcanvasBuySell.toggle();
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
// TODO 주기적으로 router를 호출하여 세션을 체크하고, 만료되면 로그아웃 처리

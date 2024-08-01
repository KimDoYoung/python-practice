/**
 * 주식 실시간 데이터를 파싱하는 클래스
 */
class StkRealDataParser {
    constructor(data) {
        this.rawData = data;
        this.parsedData = null;
        this.type = null;
        this.parseData();
    }

    parseData() {
        // 메시지를 '|'로 분리
        const parts = this.rawData.split('|');
        
        if (parts.length > 4) {
            const type = parts[3];
            // JSON 부분 추출
            const jsonPart = parts.pop();
            try {
                const data = JSON.parse(jsonPart);
                
                if (type === 'KIS' && data.ODER_KIND === '00') {
                    this.type = 'KIS-체결정보';
                    this.parsedData = data;
                } else if (type === 'LS' && data.header.tr_cd === 'SC1') {
                    this.type = 'LS-체결정보';
                    this.parsedData = data;
                } else {
                    this.type = '일반메시지';
                }
            } catch (error) {
                console.error("JSON 디코딩 오류: ", error);
                this.type = '일반메시지';
            }
        } else {
            this.type = '일반메시지';
        }
    }

    static parse(data) {
        return new StkRealDataParser(data);
    }
}

//웹소켓을 연결한다.
//window.ws에 저장하여 전역에서 사용할 수 있도록 한다.
if (!window.ws) {
    window.ws = new WebSocket("ws://localhost:8000/ws");
}

window.ws.onmessage = function(event) {
    //WS으로 메세지를 받음
    console.log(event.data)    
    var $messages = $('#messages');
    if ($messages) {
        var $message = $('<li>');
        var content = document.createTextNode(event.data);
        $message.append(content);
        $messages.append($message);
    }
    var parser = StkRealDataParser.parse(event.data);
        
    if (parser.type === 'KIS-체결정보') {
        displayKISInfo(parser.parsedData);
    }else if(parser.type === 'LS-체결정보') {
        displayLSInfo(parser.parsedData);
    } else {
        // displayMessage(event.data);
        console.log("일반 메시지: ", event.data);
    }

};

function formatTime(timeStr) {
    if (timeStr.length < 6) {
        throw new Error("Invalid time string length");
    }
    const hours = timeStr.substring(0, 2);
    const minutes = timeStr.substring(2, 4);
    const seconds = timeStr.substring(4, 6);
    
    return `${hours}:${minutes}:${seconds}`;
}
function formatWon(numberStr){
    // 숫자 문자열을 숫자로 변환한 후, 다시 문자열로 변환하면서 콤마 추가
    const number = parseInt(numberStr, 10);
    return number.toLocaleString();
}
function buySellTypeKis(s){
    if(s == '01'){
        return '매도체결';
    }else if(s == '02'){
        return '매수체결';
    }else{
        return "";
    }
}
function buySellTypeLs(s){
    if(s == '1'){
        return '매도체결';
    }else if(s == '2'){
        return '매수체결';
    }else{
        return "";
    }
}
function displayLSInfo(response) {
    var data = response.body;
    var $alertContainer = $('#alert-container');
    
    let html = '<table class="table"><tr>';
    html += '<th>증권사</th><td>LS증권</td>';
    html += '<th>체결시간</th><td>' + formatTime(data.exectime) + '</td>';
    html += '<th>주문번호</th><td>' + data.ordno + '</td>';
    html += '<th>계좌번호</th><td>' + data.accno + '</td>';
    html += '<th>주문구분</th><td class="text-danger">' + buySellTypeLs(data.bnstp) + '</td>';
    html += '<th>종목코드</th><td>' + `${data.Isunm}(${data.shtnIsuno.substring(1)})` + '</td>';
    html += '<th>체결수량</th><td>' + formatWon(data.execqty) + '</td>';
    html += '<th>체결가</th><td>' + formatWon(data.mnyexecamt) + '</td>';
    html += '</tr></table>'
    var $alert = $('<div class="alert alert-warning alert-dismissible fade show" role="alert">')
        .html(html)
        .append('<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>');
    $alertContainer.append($alert);        
}
function displayKISInfo(data) {
    var $alertContainer = $('#alert-container');
    
    let html = '<table class="table"><tr>';
    html += '<th>증권사</th><td>한국투자증권(KIS)</td>';
    html += '<th>체결시간</th><td>' + formatTime(data.STCK_CNTG_HOUR) + '</td>';
    html += '<th>주문번호</th><td>' + parseInt(data.ODER_NO, 10) + '</td>';
    html += '<th>계좌번호</th><td>' + data.ACNT_NO + '</td>';
    html += '<th>주문구분</th><td class="text-danger">' + buySellTypeKis(data.SELN_BYOV_CLS) + '</td>';
    html += '<th>종목코드</th><td>' + data.STCK_SHRN_ISCD + '</td>';
    html += '<th>체결수량</th><td>' + formatWon(data.CNTG_QTY) + '</td>';
    html += '<th>체결가</th><td>' + formatWon(data.CNTG_UNPR) + '</td>';
    html += '</tr></table>'
    var $alert = $('<div class="alert alert-warning alert-dismissible fade show" role="alert">')
        .html(html)
        .append('<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>');
    $alertContainer.append($alert);        
}

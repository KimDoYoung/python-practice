/**
 * handlebar-helpers 
 */
//핸들바 템플릿으로 html을 만들어서 리턴한다.
function makeHtmlWithTemplateIdAndData(templateId, data) {
    const template = document.getElementById(templateId).innerHTML;
    const compiledTemplate = Handlebars.compile(template);
    return compiledTemplate(data);
}

// 사용자 함수 inc 등록
Handlebars.registerHelper("inc", function(value, options){
    return parseInt(value) + 1;
});
Handlebars.registerHelper('formatComma', function (number) {
    // 숫자에 콤마 추가
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
});	
Handlebars.registerHelper('formatYmdHms', function(date) {
    // date는 JavaScript Date 객체여야 함
    var year = date.getFullYear();
    var month = ('0' + (date.getMonth() + 1)).slice(-2);
    var day = ('0' + date.getDate()).slice(-2);
    var hours = ('0' + date.getHours()).slice(-2);
    var minutes = ('0' + date.getMinutes()).slice(-2);
    var seconds = ('0' + date.getSeconds()).slice(-2);

    return year + '-' + month + '-' + day + ' ' + hours + ':' + minutes + ':' + seconds;
});
Handlebars.registerHelper('formatDateString', function(dateStr) {
    var months = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ];

    var dateParts = dateStr.split(/[\s,]+/);
    var monthIndex = months.indexOf(dateParts[0]);
    var year = dateParts[2];
    var month = ('0' + (monthIndex + 1)).slice(-2);
    var day = ('0' + dateParts[1]).slice(-2);
    var timeParts = dateParts[3].split(':');
    var hours = ('0' + parseInt(timeParts[0])).slice(-2);
    var minutes = ('0' + parseInt(timeParts[1])).slice(-2);
    var seconds = ('0' + parseInt(timeParts[2])).slice(-2);
    var period = dateParts[4];

    return year + '-' + month + '-' + day + ' ' + hours + ':' + minutes + ':' + seconds + ' ' + period;
}); 
/**
 * 파일 사이즈를 사람이 인식하기 쉽게 표시
 * {{humanFileSize 123456787}}
 */
Handlebars.registerHelper("humanFileSize", function(fileSize){
    var si = true;
    var thresh = si ? 1000 : 1024;
    var bytes = parseInt(fileSize, 10);
    if (bytes < thresh) return bytes + ' B';
    var units = si ? ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'] : ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'];
    var u = -1;
    do {
        bytes /= thresh;
        ++u;
    } while (bytes >= thresh);
    var html =  bytes.toFixed(1) + ' ' + units[u];        
    return new Handlebars.SafeString(html);
});

Handlebars.registerHelper("t", function(exp, options) {
    var context = this;
    var result;

    try {
        var func = new Function('context', 'with(context) { return ' + exp + '; }');
        result = func(context);
    } catch (error) {
        if (typeof logger !== 'undefined' && logger.error) {
            logger.error("gctest : " + error + ' [' + exp + ']');
        } else {
            console.error("gctest : " + error + ' [' + exp + ']');
        }
        return false;
    }

    return result;
});    
/**
 * javascript문법으로 논리식을 판별
 * 
 */       
Handlebars.registerHelper("test", function(expression, options){
    var exp = '(' + expression.replace(/^\s+|\s+$/,'') +')';
    var result = Handlebars.helpers["t"].call(this, exp, options);

    if(result === true){
        return options.fn(this);
    } else {
        return options.inverse(this);
    }
});
/**
 * 소숫점 2자리까지만 표시
 */
Handlebars.registerHelper('displayRate', function(value) {
    // 문자열을 숫자로 변환
    var num = parseFloat(value);

    // NaN 체크 (숫자가 아니면 원래 값을 반환)
    if (isNaN(num)) {
        return value;
    }

    // 소수점 두 자리까지 출력 (정수면 0 추가)
    return num.toFixed(2);
});        
/**
 * displayYmd : 20200101 -> 2020-01-01
 */
Handlebars.registerHelper('displayYmd', function(dateStr) {
    var year = dateStr.slice(0, 4);
    var month = dateStr.slice(4, 6);
    var day = dateStr.slice(6, 8);

    return year + '-' + month + '-' + day;
});

/**
 * displayYmdAd : 20200101 -> 2020-01-01
 * 년도가 올해라면 년도를 표시하지 않음
 */
Handlebars.registerHelper('displayYmdAd', function(dateStr) {
    var year = dateStr.slice(0, 4);
    var month = dateStr.slice(4, 6);
    var day = dateStr.slice(6, 8);
    if(year == new Date().getFullYear()) {
        return month + '-' + day;
    } else {
        return year + '-' + month + '-' + day;
    }
});    
/**
 * displayYmd : 20200101 -> 2020-01-01
 */
Handlebars.registerHelper('naverUrl', function(stockCode) {
    const anchor = "<a href='https://finance.naver.com/item/main.nhn?code=" + stockCode + "' target='_blank'>" + stockCode + "</a>";
    return new Handlebars.SafeString(anchor);
});
//displayJoEok을 12345 -> 1조 2345억으로 변경
Handlebars.registerHelper('displayJoEok', function(number) {
    // 소수점 아래를 잘라내고 정수 부분만 사용
    number = Math.floor(number);

    if (typeof number !== 'number') {
        return number;
    }

    let trillion = Math.floor(number / 10000);
    let remainder = number % 10000;

    let formattedNumber = '';
    if (trillion > 0) {
        formattedNumber += `${trillion}조 `;
    }
    if (remainder > 0 || formattedNumber !== '') {
        formattedNumber += `${remainder.toLocaleString()}억`;
    }

    return formattedNumber.trim();
});

Handlebars.registerHelper('displayJoEok2', function(number) {
    const moneyFormat = (value) => {
        const numbers = [
            numbering(value % 100000000000000000000, 10000000000000000),
            numbering(value % 10000000000000000, 1000000000000),
            numbering(value % 1000000000000, 100000000),
            numbering(value % 100000000, 10000),
            value % 10000
        ]
    
        return setUnitText(numbers)
                .filter(number => !!number)
                .join(' ');
    }
    
    const setUnitText = (numbers) => {
        const unit = ['원', '만', '억', '조', '경'];
        return numbers.map((number, index) => !!number ? numberFormat(number) + unit[(unit.length - 1) - index] : number)
    }
    
    const numbering = (value, division) => {
        const result = Math.floor(value / division);
        return result === 0 ? null : (result % division);
    }
    
    const NUMBER_FORMAT_REGX = /\B(?=(\d{3})+(?!\d))/g;
    
    const numberFormat = (value) => {
        return value.toString().replace(NUMBER_FORMAT_REGX, ",");
    }
    return moneyFormat(number);
});
Handlebars.registerHelper('displayWon', function(number) {
    // 숫자를 int형으로 변환
    var intNumber = parseInt(number, 10);

    // 천 단위로 컴마를 찍어서 문자열로 변환
    return intNumber.toLocaleString();
});

Handlebars.registerHelper('displayPercent', function(value) {
    // 문자열을 숫자로 변환
    const number = parseFloat(value);
    // 소수점 둘째 자리까지 반올림
    const roundedNumber = number.toFixed(2);
    return roundedNumber;
});

// Handlebars helper 등록
Handlebars.registerHelper('displayTime', function(input) {
    // 입력에서 숫자만 추출
    const digits = input.replace(/\D/g, '');

    // 길이가 4 미만이면 앞에 0을 추가하여 4자리로 만듦
    const paddedDigits = digits.padStart(4, '0');

    // 앞 두 자리와 뒤 두 자리를 :로 구분하여 반환
    const formattedTime = `${paddedDigits.slice(0, 2)}:${paddedDigits.slice(2, 4)}`;

    return formattedTime;
});    

Handlebars.registerHelper('goNaver', function(code) {
    const url = `https://finance.naver.com/item/coinfo.naver?code=${code}`;
    return new Handlebars.SafeString(`<a href="${url}" target="_blank" title="naver증권으로 이동" >${code}</a>`);
});

Handlebars.registerHelper('displaySign', function(value) {
    switch(parseInt(value, 10)) {
        case 1:
            return '상한';
        case 2:
            return '상승';
        case 3:
            return '보합';
        case 4:
            return '하한';
        case 5:
            return '하락';
        default:
            return 'Unknown';
    }
});

// 주당차이 value1 평균매입가격, value2 현재가
Handlebars.registerHelper('judang_plus_minus', function(value1, value2) {
    const diff = (value1) - (value2);
    if (diff > 0) {
        const diffInt = Math.floor(diff);
        return "-" +  diffInt.toLocaleString();
    }else{
        const diffInt = Math.floor(diff*-1);
        if(diffInt == 0){
            return 0;
        }
        return diffInt.toLocaleString();
    }
});
/**
    * 숫자를 특정 포맷에 맞게 출력
    * <p>{{displayFmt 50000 "0,000" "-"}}</p>       <!-- 출력: 50,000 -->
    * <p>{{displayFmt 50000 "0.00" "-"}}</p>        <!-- 출력: 50000.00 -->
    * <p>{{displayFmt 50000 "0,000.00" "-"}}</p>    <!-- 출력: 50,000.00 -->
    * <p>{{displayFmt null "0,000.00" "N/A"}}</p>   <!-- 출력: N/A -->
    * <p>{{displayFmt 1234567.89 "0,000.00" "-"}}</p> <!-- 출력: 1,234,567.89 -->
    */
Handlebars.registerHelper('numberFmt', function(value, format, defaultValue) {
    if (value === undefined || value === null || isNaN(value)) {
        return defaultValue || '-';
    }

    // 1. 천단위 구분 (3자리마다 콤마)
    if (format.includes(',')) {
        value = Number(value).toLocaleString();
    }

    // 2. 소수점 자리수 포맷
    if (format.includes('.')) {
        const decimals = format.split('.')[1].length;
        value = Number(value).toFixed(decimals);
    }

    // 3. 천단위 콤마와 소수점 자리수를 동시에 처리
    if (format.includes(',') && format.includes('.')) {
        const parts = format.split('.');
        const decimals = parts[1].length;
        value = Number(value).toLocaleString(undefined, { minimumFractionDigits: decimals, maximumFractionDigits: decimals });
    }

    return value;
});
/*
* 주당차이를 계산하여 표시
* <p>{{displayCha 10000 5000}}</p>  <!-- 출력: 5,000 -->
* <p>{{displayCha 1234567 765432}}</p>  <!-- 출력: 469,135 -->
* <p>{{displayCha 1000000 500000}}</p>  <!-- 출력: 500,000 -->
* <p>{{displayCha 100 200}}</p>  <!-- 출력: -100 -->
* <p>{{displayCha "abc" 500}}</p>  <!-- 출력: - (숫자가 아닐 경우) -->
*/
Handlebars.registerHelper('displayCha', function(a, b) {
    // a와 b가 숫자인지 확인
    if (isNaN(a) || isNaN(b)) {
        return '-';
    }

    // a - b 계산
    const result = a - b;

    // 결과를 3자리마다 콤마를 찍어서 문자열로 변환
    return result.toLocaleString();
});


/**
 * 회사정보 canvas를 보여주는 함수, ipo_scheduler_main.js 을 가지고 어느곳에서나 사용가능하도록함
 * {{toggleCompanyCanvas stk_code stk_name}}
 */
Handlebars.registerHelper('toggleCompanyCanvas', function(stk_code, stk_name) {
    // a 태그 HTML 문자열을 반환
    return new Handlebars.SafeString(
        `<a href="#" class="companycanvas-link" onclick="javascript:showCompanyCanvas('${stk_code}')" title="${stk_name}의 정보보기">${stk_name}</a>`
    );
});


// my_eval 헬퍼: 수식을 처리하는 간단한 헬퍼 함수
// 주의 : 소숫점을 떼어냄, 결과에 콤마를 찍음
//{{my_calc this "*" ../current_cost}}
//{{my_calc (my_calc this "*" ../current_cost) "*" 0.002}}
//{{my_calc (my_calc this "*" ../current_cost) "+" (my_calc (my_calc this "*" ../current_cost) "*" 0.002) }}

Handlebars.registerHelper('my_calc', function(a, operator, b) {
    // 콤마가 포함된 숫자를 처리하기 위해 콤마를 제거하고 숫자로 변환
    let numA = typeof a === 'string' ? Number(a.replace(/,/g, '')) : a;
    let numB = typeof b === 'string' ? Number(b.replace(/,/g, '')) : b;
    
    let result;
    
    // 연산자에 따른 계산
    switch (operator) {
        case '*':
            result = numA * numB;
            break;
        case '+':
            result = numA + numB;
            break;
        case '-':
            result = numA - numB;
            break;
        case '/':
            result = numB !== 0 ? numA / numB : 0;  // 0으로 나누기 방지
            break;
        default:
            result = null;
    }

    // 소수점 이하를 잘라내기 (Math.floor 또는 Math.round도 사용 가능)
    result = Math.floor(result);  // 소수점 이하 버림

    // 최종 결과에 콤마 추가하여 반환
    return result.toLocaleString();  // 콤마가 포함된 형식으로 반환
});

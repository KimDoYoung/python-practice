/**
 * handlebar-helpers 
 */
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
    /**
     * gcTest가 호출하는 함수로 직접 html에는 사용하지 않아야함
     */
    // Handlebars.registerHelper("t", function( exp, options){
    //     // debugger;
    //     // logger.log(this);
    //     var r = (function(){
    //             try {
    //                 var r =  eval(exp);
    //                 return r;
    //             } catch (error) {
    //                 logger.error("gctest : " + error + ' [' + exp +']');
    //             }
    //         }).call(this);
    //     return r;
    // }); 
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
    // Handlebars.registerHelper("test", function(expression, options){
    //     // logger.log(this);
    //     var exp = '(' + expression.replace(/^\s+|\s+$/,'') +')';
        
    //     var result = Handlebars.helpers["t"].call(this, exp, options);
    //     if(result === true){
    //         return options.fn(this);
    //     } else {
    //         return options.inverse(this);
    //     }
    // });    
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


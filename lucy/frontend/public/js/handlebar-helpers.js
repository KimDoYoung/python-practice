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
     * displayYmd : 20200101 -> 2020-01-01
     */
    Handlebars.registerHelper('naverUrl', function(stockCode) {
        const anchor = "<a href='https://finance.naver.com/item/main.nhn?code=" + stockCode + "' target='_blank'>" + stockCode + "</a>";
        return new Handlebars.SafeString(anchor);
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
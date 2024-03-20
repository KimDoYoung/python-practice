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
    Handlebars.registerHelper("t", function( exp, options){
        // debugger;
        // logger.log(this);
        var r = (function(){
                try {
                    var r =  eval(exp);
                    return r;
                } catch (error) {
                    logger.error("gctest : " + error + ' [' + exp +']');
                }
            }).call(this);
        return r;
    }); 
    /**
     * javascript문법으로 논리식을 판별
     */       
    Handlebars.registerHelper("test", function(expression, options){
        // logger.log(this);
        var exp = '(' + expression.replace(/^\s+|\s+$/,'') +')';
        
        var result = Handlebars.helpers["t"].call(this, exp, options);
        if(result === true){
            return options.fn(this);
        } else {
            return options.inverse(this);
        }
    });    
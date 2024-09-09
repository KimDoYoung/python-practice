if (!String.format) {
	String.prototype.format = function() {
        var formatted = this, i = 0;
        while (/%s/.test(formatted))
            formatted = formatted.replace("%s", arguments[i++]);
        return formatted;
	}
}
//console.log("%s + %s = %s".format(4, 5, 9));
if (!String.hashCode) {
	String.prototype.hashCode = function() {
        var hash = 0,
        i, chr;
        if (this.length === 0) return hash;
            for (i = 0; i < this.length; i++) {
            chr = this.charCodeAt(i);
            hash = ((hash << 5) - hash) + chr;
            hash |= 0; // Convert to 32bit integer
        }
        return hash;
	}
}
if (typeof String.prototype.replaceAll != 'function') {
    String.prototype.replaceAll = function(search,replace){
        return this.replace(new RegExp(search, "g"), replace);
    };
}

var JuliaUtil = (function(){
    var isString = function (s) {
        return typeof s === 'string';
    };
    var isNumber = function(s){
        return typeof s === 'number';
    }
    var isEmpty = function(e){
            if( Object.prototype.toString.call( e ) === '[object Array]' ) {
                if(e.length === 0) return true;
                return false;
            }
            if( Object.prototype.toString.call( e ) === '[object Object]' ){
                for(var p in e){
                    if(e.hasOwnProperty(p)) {
                        return false;
                    }
                }
                return true;
            }
            if((typeof e) == 'undefined' ) return true;
            switch(e) {
                case "":
                case null:
                case typeof this == "undefined":
                    return true;
                default : 
                    return false;
            }            
    };
    var dateFormat = function (format, date){
        var weekName1 = ["일요일", "월요일", "화요일", "수요일", "목요일", "금요일", "토요일"],
            weekName2 = ["일", "월", "화", "수", "목", "금", "토"],
            d = date,
            zf = function(n,len){
                var zero = '', n = n+'';
                if(n.length >= len) return n;
                for(var i=0; i < (len-n.length);i++) zero+='0';
                return zero+n;
            };
        return format.replace(/(yyyy|yy|MM|dd|E|hh|mm|ss|a\/p)/gi, function($1) {
            switch ($1) {
                case "yyyy": return d.getFullYear();
                case "yy": return zf( (d.getFullYear() % 1000), 2);
                case "MM": return zf( (d.getMonth() + 1), 2) ;
                case "dd": return zf( d.getDate(), 2) ;
                case "E": return weekName1[d.getDay()];
                case "e": return weekName2[d.getDay()];
                case "HH": return zf( d.getHours(), 2);
                case "hh": return zf( ((h = d.getHours() % 12) ? h : 12), 2);
                case "mm": return zf( d.getMinutes(), 2);
                case "ss": return zf(  d.getSeconds(), 2) ;
                case "a/p": return d.getHours() < 12 ? "오전" : "오후";
                default: return $1;
            }
        }); 
    };
    var diffDays = function (fromDate, toDate) {
        if(!isString(fromDate) || !isString(toDate)) return undefined;
        var fromDate = fromDate.replace(/[-.\/]/gi, ''),// '-'가 있다면 제거
            toDate   = toDate.replace(/[-.\/]/gi, '');
        if(fromDate.length === 8 && toDate.length == 8){
            var date1  = new Date(fromDate.substring(0,4), fromDate.substring(4,6)-1, fromDate.substring(6,8) ),
                date2  = new Date(toDate.substring(0,4), toDate.substring(4,6)-1,toDate.substring(6,8));

            return Math.abs(Math.floor(( date2 - date1 )/86400000));
        }
        return undefined;
    }
    //contextPath
    var contextPath = ()=>{
		let path = window.location.pathname.split('/');
		return window.location.origin + '/' + path[1];
    }
    
    var displayLoading = function(show) {
		const loading_div_id = '#julia-loading-div';
		let loading_div_nm = loading_div_id.substring(1);
		if( $(loading_div_id).length == 0 ){
			var doc = document.documentElement;
			var body = document.body;
			var top = (doc.clientHeight / 2 ) + (doc.scrollTop + body.scrollTop)-190;
			var left = (doc.clientWidth / 2 );
			var path = 'public'; //contextPath();
			var div_html = `<div id='${loading_div_nm}' style='display:none;position:absolute;top:${top}px;left:${left}px'><img src='${path}/images/loading.gif'></div>`;
			$("body").append(div_html);
		} 
		if( show ){
			//$(loading_div_id).show();
			$(loading_div_id).removeClass('d-none');
		}else{
            // $(loading_div_id).hide();
			$(loading_div_id).addClass('d-none');
		}
	}
    var displayComma = function (str){
        // 숫자인지 체크 후 문자열로 변환
        if (!isNaN(str)) {
            str = str.toString();
        }

        // 음수인 경우 처리
        var isNegative = str[0] === '-';
        var numberPart = isNegative ? str.slice(1) : str; // 음수라면 첫 번째 문자는 제외

        // 콤마 붙이기
        var formattedNumber = numberPart.replace(/\B(?=(\d{3})+(?!\d))/g, ",");

        // 음수면 부호 다시 붙여서 반환
        return isNegative ? '-' + formattedNumber : formattedNumber;
    };
    var extendsOptions = function(options, defaults){
        var options = options || {},
            defaults  = defaults || {},
            settings = {};
        for(var opt in options){
            if(options.hasOwnProperty(opt)){
                settings[opt] = options[opt];
            }
        }
        for(var opt in defaults){
            if(defaults.hasOwnProperty(opt) && !options.hasOwnProperty(opt)){
                settings[opt] = defaults[opt];
            }
        }
        return settings;
    }
    var Ajax = function(url, data, options){
		var baseUrl = contextPath();
        var options = extendsOptions(options, 
            {
                method:'GET', processData: true, contentType: 'application/json;charset=utf-8', dataType:'json',
                beforeSend : ()=> { 
					console.log('beforeSend...');
                },
                success : (response, status, xhr) => {
					console.log(`status:${status}, response: ${response}, xhr:${xhr}`);
				},
                error : (xhr, status, error) => {
					console.error('Error fetching template:', error);
				},
                complete: (xhr, status)=>{
					console.log(`xhr:${xhr}, status:${status}`);
				}
            }
        );
        //console.log('data:' + JSON.stringify(data));
        //console.log(options);
        data = JSON.stringify(data);
        $.ajax({
            type	: options.method, //요청 메소드 타입
            url		: baseUrl +  url, //요청 경로
            async : true, //비동기 여부
            data  : data, //요청 시 포함되어질 데이터
            processData : true, //데이터를 컨텐트 타입에 맞게 변환 여부
            cache : options.processData, //캐시 여부
            contentType : options.contentType, //요청 컨텐트 타입 "application/x-www-form-urlencoded; charset=UTF-8"
            dataType	: options.dataType, //응답 데이터 형식 명시하지 않을 경우 자동으로 추측
            beforeSend  : options.beforeSend,// XHR Header를 포함해서 HTTP Request를 하기전에 호출됩니다.
            success	: options.success,
            error	: options.error,
            complete : options.complete
        });
    }
    var formSubmit = function(method, action, dataObject){
        var method = method || 'GET' ;
        var action = action || '/';
        var data = dataObject || {};
        var $form = $(`<form action="${action}"></form>`).appendTo('body');
        $.each( data, function( key, val ) {
            $form.append($('<input/>', {type: 'hidden', name: key, value: val }));
        });
        //debugger;
        $form.submit();
    }
    var popupWindow = function popupWin(url, name, prop, pWidth, pHeight){
		if( pWidth == null ) pWidth = 0;
		if( pHeight == null ) pHeight = 0;
		var winL = (screen.width - pWidth) / 2;
        var winT = (screen.height - pHeight) / 2;
		prop+= ", top=" + winT + ", left=" + winL + ", width=" + pWidth + ", height=" + pHeight;
		return window.open(url,name,prop);
	}
	var formToJson = function($form){
        var unindexed_array = $form.serializeArray();
        var obj = {};
		
        $.map(unindexed_array, function(n, i){
            obj[n['name']] = n['value'];
        });
		
        return obj;
	}
    var displayYmd = function(ymd, gubun){
        if(ymd == false || ymd.length < 8) return ymd;
        var ymd = (""+ymd).replace(/\D/g, '');
        var gubun = gubun || '-';
        return ymd.substring(0,4) + gubun + ymd.substring(4,6) + gubun + ymd.substring(6);
    }
    var toNumber = function(str) {
        var str = (""+str).replace(/[^0-9.+-]/g,'');
        return Number(str);
    }
    var addRemoveStickyAtTable = function(){
		$('.dropdown').on('show.bs.dropdown',function(){
            console.log('drop down show')
            $('table thead').removeClass('sticky-top').removeClass('top-0');
        });
        $('.dropdown').on('hide.bs.dropdown',function(){
            console.log('drop down hide')
            $('table thead').addClass('sticky-top').addClass('top-0');
        });
		$('#frYmd, #toYmd').on('show',function(){
            console.log('drop down show')
            $('table thead').removeClass('sticky-top').removeClass('top-0');
        });
		$('#frYmd, #toYmd').on('hide',function(){
            console.log('drop down show')
            $('table thead').addClass('sticky-top').addClass('top-0');
        });
	}  
	/*
    var copyToClipboard = function(text) {
        try {
            navigator.clipboard.writeText(text);
            //console.log('Content copied to clipboard');
        } catch (err) {
            console.error('Failed to copy: ', err);
        }
    } 
    */
    var tableToString= (tableId) => {
        var $table = $('#'+tableId);
        if($table == false) return "";
        var s = '';
        var headers = $table.find('thead tr th').each( (idx,th)=>{
            console.log(th);
            s += $(th).text() + "\t";
        });
        if(s) s+= "\n";
        var rows = $table.find('tbody tr').each( (idx,tr) => {
            $(tr).find('td').each( (idx,td) => {
                var $td = $(td);
                var colspan = $td.attr('colspan');
                if(colspan){
                    for(var i=0; i<colspan;i++){
                        s += "" + "\t";
                    }  
                }else{
                    s += $(td).text().trim() + "\t";
                }	
            });
            s += "\n";
        });
        //copyToClipboard(s);
        return s;
    }  
    var isValidYmd = (dateStr) => {
        var d = (dateStr+"").replace(/\D/g,'');
        d = JuliaUtil.displayYmd(d);
        return !isNaN(new Date(d));
    }

    var navigateTo = function navigateToURL(url) {
        window.location.href = url;
    }
    /**
     * javascript object객체에서 key에 해당하는 속성을 제거한다.
     */
    var removeElement = function (obj,key) {
        if (obj.hasOwnProperty(key)) {
            delete obj[key];
        }
        return obj;
    }
    
    var objectFromFrom = function($form){
        const formArray = $form.serializeArray();
        const formObject = {};

        $.map(formArray, function(item) {
            if (formObject[item.name]) {
                if (!Array.isArray(formObject[item.name])) {
                    formObject[item.name] = [formObject[item.name]];
                }
                formObject[item.name].push(item.value);
            } else {
                formObject[item.name] = item.value;
            }
        });

        //console.log(formObject);
        return formObject;
    }

    // 사용 예시
    // const today = '2024-09-04';  // 'yyyy-MM-dd' 형식
    // console.log(addDate(today, 'month', -1));  // '2024-08-04' (한 달 빼기)

    // const customDate = '20240904';  // 숫자만 있는 경우
    // console.log(addDate(customDate, 'day', 3));  // '2024-09-07' (3일 더하기)

    // const customDateWithSymbols = '2024/09/04';  // 다른 형식 (기호 포함)
    // console.log(addDate(customDateWithSymbols, 'day', 3));  // '2024-09-07'

    var addDate = function (dateStr, unit, value) {
        // 'yyyy-MM-dd' 형식이 아니어도 숫자만 추출해서 8자리로 처리
        const cleanedDateStr = dateStr.replace(/\D/g, ''); // 숫자가 아닌 문자는 모두 제거
    
        // 8자리 숫자에서 연, 월, 일을 추출
        const year = parseInt(cleanedDateStr.substring(0, 4), 10);  // 처음 4자리: 연도
        const month = parseInt(cleanedDateStr.substring(4, 6), 10) - 1;  // 5~6번째 자리: 월 (0부터 시작하므로 -1)
        const day = parseInt(cleanedDateStr.substring(6, 8), 10);  // 7~8번째 자리: 일
    
        // Date 객체 생성
        const date = new Date(year, month, day);
    
        // 단위에 따라 날짜 변경
        switch (unit) {
            case 'day':
                date.setDate(date.getDate() + value);
                break;
            case 'month':
                date.setMonth(date.getMonth() + value);
                break;
            case 'year':
                date.setFullYear(date.getFullYear() + value);
                break;
            default:
                console.error('지원하지 않는 단위입니다.');
                return null;
        }
    
        // 변경된 날짜를 'yyyy-MM-dd' 형식으로 반환
        const newYear = date.getFullYear();
        const newMonth = String(date.getMonth() + 1).padStart(2, '0');  // 월은 0부터 시작하므로 +1
        const newDay = String(date.getDate()).padStart(2, '0');
    
        return `${newYear}-${newMonth}-${newDay}`;
    }
    

    return {
        isString : isString,
        isNumber : isNumber,
        isEmpty  : isEmpty,
        dateFormat :dateFormat ,
        today : (dateformat)=>{
            return isEmpty(dateformat) ? dateFormat('yyyy-MM-dd', new Date()) : dateFormat(dateformat, new Date());
        },
        //두날짜사이의 일수
        diffDays : diffDays,        
        //금액표시
        displayMoney : displayComma,
        //option 확장
        extendsOptions : extendsOptions,
        // 로딩이미지를 보여준다 
        displayLoading : displayLoading,
        ajax : Ajax,
        submitGet: function(action, dataObject){
            formSubmit('GET', action, dataObject);
        },
        submitPost: function(action, dataObject){
            formSubmit('POST', action, dataObject);
        },
        navigateTo : navigateTo,
        popupWindow : popupWindow,
        formToJson : formToJson,
        displayYmd : displayYmd, 
        toNumber   : toNumber,
        addRemoveStickyAtTable: addRemoveStickyAtTable, /* dropdown이 펼쳐졌을 때 테이블에서 sticky 제거*/
        tableToString : tableToString, /* table html을  string으로 */
        isValidYmd : isValidYmd,
        contextPath : contextPath,
        removeElement : removeElement,
        objectFromForm : objectFromFrom,
        addDate : addDate
    };    
})();

const unsecuredCopyToClipboard = (text) => { const textArea = document.createElement("textarea"); textArea.value=text; document.body.appendChild(textArea); textArea.focus();textArea.select(); try{document.execCommand('copy')}catch(err){console.error('Unable to copy to clipboard',err)}document.body.removeChild(textArea)};

/**
 * Copies the text passed as param to the system clipboard
 * Check if using HTTPS and navigator.clipboard is available
 * Then uses standard clipboard API, otherwise uses fallback
*/
const copyToClipboard = (content) => {
    var isShowAlert = true;
    if (window.isSecureContext && navigator.clipboard) {
    navigator.clipboard.writeText(content)
        .then(() => {
            if(isShowAlert){
                if(bootbox){
                    bootbox.alert("Table data has been copied to the clipboard.<br/>You can paste it in Excel");
                }else{
                    alert("Table data has been copied to the clipboard.\nYou can paste it in Excel");
                }
            }
		})
		.catch((err) => {
		        //alert("something went wrong");
            console.error('Failed to copy: ', err);
        });	    
    } else {
        unsecuredCopyToClipboard(content);
    }
};
function triggerExportTable(){
	//excel client
	$('#btnTableExportToExcel').on('click', (e)=>{
		e.stopPropagation(); 
	var tableName = $('#btnTableExportToExcel').data('table-id');
	var excelName = $('#btnTableExportToExcel').data('excel-name') + "_" +JuliaUtil.dateFormat("yyyy_MM_dd_HHmmss", new Date());
	const table = $('#'+tableName).get(0);
	const workbook = XLSX.utils.table_to_book(table, { sheet: excelName });
	XLSX.writeFile(workbook, excelName +'.xlsx'); 			
	});
	$('#btnTableExportToClipboard').on('click', ()=>{
        var isShowAlert = true;
        var tableName = $('#btnTableExportToClipboard').data('table-id');
        var s = JuliaUtil.tableToString(tableName);
        copyToClipboard(s);
       //unsecuredCopyToClipboard(s);
	});	
}
//----------------------------------------
function setCookie(key, value, expire_min) {
    const date = new Date();
    date.setTime(date.getTime() + (expire_min * 60 * 1000));
    const expires = "expires=" + date.toUTCString();
    document.cookie = key + "=" + value + ";" + expires + ";path=/";
}

function getCookie(key) {
    const name = key + "=";
    const decodedCookie = decodeURIComponent(document.cookie);
    const cookieArray = decodedCookie.split(';');
    for(let i = 0; i < cookieArray.length; i++) {
        let cookie = cookieArray[i];
        while (cookie.charAt(0) == ' ') {
            cookie = cookie.substring(1);
        }
        if (cookie.indexOf(name) == 0) {
            return cookie.substring(name.length, cookie.length);
        }
    }
    return "";
}

function removeCookie(name) {
    document.cookie = name + '=; Max-Age=-99999999;';  
}

//------------------------------------------------------
// moneyFormat(12345)
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
// Handlebars 헬퍼 등록
Handlebars.registerHelper('ifFuture', function(dateString, options) {
    if (dateString) {
        // 숫자가 아닌 문자를 모두 제거
        var cleanedDateString = dateString.replace(/\D/g, '');
        
        // 결과가 8글자인지 확인
        if (cleanedDateString.length === 8) {
            // yyyy-mm-dd 형식으로 변환
            var formattedDateString = cleanedDateString.slice(0, 4) + '-' + cleanedDateString.slice(4, 6) + '-' + cleanedDateString.slice(6, 8);
            var inputDate = new Date(formattedDateString);
        } else {
            var inputDate = new Date(dateString);
        }

        var today = new Date();
        today.setHours(0, 0, 0, 0); // 오늘 날짜의 시간을 00:00:00로 설정

        if (!isNaN(inputDate.getTime()) && inputDate > today) {
            return options.fn(this);
        } else {
            return options.inverse(this);
        }
    } else {
        return options.inverse(this);
    }
});

Handlebars.registerHelper('anchorHome', function(hp_url) {
    if (hp_url && hp_url.trim() !== "") {
        let url = hp_url.trim();
        if (!hp_url.startsWith('http://') && !hp_url.startsWith('https://')) {
            url = 'http://' + hp_url;
        }
        
        return new Handlebars.SafeString(`<a href="${url}" target="_blank"><i class="bi bi-house-door"></i></a>`);
    } else {
        return "";
    }
});

console.log('ipo helpers registered');
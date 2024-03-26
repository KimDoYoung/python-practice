/**
 * merian-keyboard.js
 * 
 */
console.log('merian-keyboard.js loaded');
var MappingInfo = {
    "keyboard-list": {
        method:'GET',
        url: "/keyboard",
        handlebarTemplate: "#keyboard-list-template",
        init_function : init_keyboard_list
    },
    "keyboard-insert": {
        method:'GET',
        url: "/keyboard/insert",
        handlebarTemplate: "#keyboard-insert-template",
        init_function : init_keyboard_insert
    },
    "keyboard-edit": {
        url: "/keyboard/edit",
        handlebarTemplate: "#keyboard-edit-template"
    },
    "keyboard-view": {
        url: "/keyboard/view",
        handlebarTemplate: "#keyboard-view-template"
    }
};
            
function displayError(xhr) {
    var message = xhr.status + ' ' + xhr.statusText;
    $('#error-message-area').text(message);
    $('#error-area').show();
}
function hideError() {
    var message = '';
    $('#error-message-area').text(message);
    $('#error-area').hide();
}
function generateHtml(pageId,data) {
    
    var handlebarId = MappingInfo[pageId].handlebarTemplate;
    var templateHtml = $(handlebarId).html()
    var template = Handlebars.compile(templateHtml);
    var html = template(data);
    return html;
}
function displayWorkspace(pageId) {
    hideError();
    var url = MappingInfo[pageId].url;
    var method = MappingInfo[pageId].method;
    var initFunc = MappingInfo[pageId].init_function;
    var data = {};
    
    JuliaUtil.ajax(url,data,{
        method : method,
        success: function (data) {
            var html = generateHtml(pageId,data);
            $('#workspace').html(html);
            initFunc();
        },error:function(xhr){
            displayError(xhr);
        }
    })
}

function init_keyboard_list(){
    $('#workspace').on('click', '#btnAddKeyboard', function(e) {
        e.stopPropagation();
        
        var html = generateHtml('keyboard-insert',{});
        $('#workspace').html(html);
        init_keyboard_insert();
    });    

}
function init_keyboard_insert(){
    console.log('init_keyboard_insert');
    $('#workspace').on('submit', '#keyboardInsertForm', function(e) {
        e.preventDefault(); // 폼의 기본 제출 동작을 방지

        formData = new FormData();
        var data = JuliaUtil.formToJson($(this));
        console.log(data);
        formData.append('keyboardData',  JSON.stringify(data));
        var $fileTag = $('#file_uploads');
        $.each($fileTag.get(0).files, function(i, file) {
            formData.append('files', file); // 'files' 키로 각 파일 추가
        });

        console.log(formData);     
        var token = localStorage.getItem('token');
        // Ajax 요청 설정
        $.ajax({
            url: '/keyboard/insert', // 요청을 보낼 서버의 URL
            type: 'POST', // HTTP 요청 방식 (GET, POST 등)
            enctype: 'multipart/form-data',  
            data: formData, // 전송할 데이터
            processData: false, // jQuery가 데이터를 처리하지 않도록 설정
            contentType: false, // jQuery가 Content-Type 헤더를 설정하지 않도록 설정
            headers: { // 요청에 헤더를 추가
                'Authorization': 'Bearer ' + token
            },            
            success: function(response) {
                // 요청이 성공하면 실행될 코드
                displayWorkspace('keyboard-list');
            },
            error: function(xhr, status, error) {
                // 요청이 실패하면 실행될 코드
                console.error('실패:', xhr, status, error);
                displayError(xhr);
            }
        });

        return false;
    });
}
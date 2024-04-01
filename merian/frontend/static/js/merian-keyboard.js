/**
 * merian-keyboard.js
 * 
 */

console.log('merian-keyboard.js loaded');
var PageData = {
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
        handlebarTemplate: "#keyboard-edit-template",
        init_function : init_keyboard_edit
    },
    "keyboard-view": {
        url: "/keyboard/view",
        handlebarTemplate: "#keyboard-view-template",
        init_function : init_keyboard_view
    }
};
            
function showError(xhr) {
    var message = "에러 발생";
    if(xhr.status){
        message = xhr.status + ' ' + xhr.statusText;
    }else{
        message = typeof(xhr) == 'object' ? xhr.toString() : xhr;
    }
    document.getElementById('error-message-area').textContent = message;
    document.getElementById('error-area').style.display = 'block';
}

function hideError() {
    document.getElementById('error-message-area').textContent = '';
    document.getElementById('error-area').style.display = 'none';
}

// pageId로 templte를 찾고 data로 만들어서 화면에 보여준다.
function changeWorkspace(pageId, data) {
    hideError();
    var handlebarId = PageData[pageId].handlebarTemplate;
    var templateHtml = document.querySelector(handlebarId).innerHTML;
    var template = Handlebars.compile(templateHtml);
    var html = template(data);
    
    document.getElementById('workspace').innerHTML = html;
    var initFunc = PageData[pageId].init_function;
    if(initFunc){
        initFunc();
    }
} 

function logout() {
    // JWT를 저장하는 방식에 따라 다름 (예: localStorage, sessionStorage)
    localStorage.removeItem('token');
    // 사용자를 로그인 페이지로 리다이렉트
    window.location.href = '/';
}
async function fetchWorkspace(pageId, detailUrl) {
    hideError();
    const url = detailUrl || PageData[pageId].url;
    const method = PageData[pageId].method;
    const token = localStorage.getItem('token');

    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const responseData = await response.json();
        changeWorkspace(pageId, responseData)
    } catch (error) {
        console.error('에러 발생:', error);
        if (error.message.includes('401')) {
            alert('로그인이 필요합니다.');
            window.location.href = '/';
        } else {
            showError(error);
        }
    }
}

// view 화면 초기화
function init_keyboard_view(){
    console.log('init_keyboard_view....');
    addDelegatedEvent('#workspace', '#btnGoEdit', 'click', function(e, target) {
        const id = target.getAttribute('data-id');
        fetchWorkspace('keyboard-edit', '/keyboard/' + id);
    });
    addDelegatedEvent('#workspace', '#btnGoList', 'click', function(e, target) {
        fetchWorkspace('keyboard-list');
    });
}


// list화면 초기화
function init_keyboard_list(){
    //추가버튼
    addDelegatedEvent('#workspace', '#btnAddKeyboard', 'click', function(e, target) {
        e.stopPropagation();
        changeWorkspace('keyboard-insert');
    });

    //보기버튼
    addDelegatedEvent('#workspace', '.btnView', 'click', function(e, target) {
        e.stopPropagation();
        const id = target.getAttribute('data-id');
        fetchWorkspace('keyboard-view', '/keyboard/' + id);
    });
    
    //수정버튼
    addDelegatedEvent('#workspace', '.btnEdit', 'click', function(e, target) {
        e.stopPropagation();
        const id = target.getAttribute('data-id');
        fetchWorkspace('keyboard-edit', '/keyboard/' + id);
    });
    
    //삭제버튼 동작
    addDelegatedEvent('#workspace', '.btnDelete', 'click', async function(e, target) {
        e.stopPropagation();
        if(confirm('삭제하시겠습니까?') == false){
            return;
        }
        const id = target.getAttribute('data-id');
        var token = localStorage.getItem('token');
        var url = '/keyboard/' + id;
        try {
            const response = await fetch(url, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + token
                }
            });
            if(!response.ok){
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            fetchWorkspace('keyboard-list');
        } catch (error) {
            showError(error);
        }
    });
    //page이동
    addDelegatedEvent('#workspace', '.btnPageJump', 'click', function(e, target) {
        e.stopPropagation();
        const page = target.getAttribute('data-page-no');
        var pageSize = document.getElementById('pageSize').value;
        var searchText = document.getElementById('searchText').value;
        var currentPageNo = page
        fetchWorkspace('keyboard-list', `/keyboard?pageSize=${pageSize}&searchText=${searchText}&currentPageNo=${currentPageNo}`);
    });
    //btnSearch 검색 버튼
    addDelegatedEvent('#workspace', '#btnSearch', 'click', function(e, target) {
        e.stopPropagation();
        var pageSize = document.getElementById('pageSize').value;
        var searchText = document.getElementById('searchText').value;
        fetchWorkspace('keyboard-list', `/keyboard?pageSize=${pageSize}&searchText=${searchText}`);
    });
    //resetSearchText 검색 리셋 버튼
    addDelegatedEvent('#workspace', '#btnResetSearchText', 'click', function(e, target) {
        e.stopPropagation();
        document.getElementById('searchText').value = '';
        fetchWorkspace('keyboard-list', "/keyboard");
    });
}
// insert화면 초기화
function init_keyboard_insert(){
    console.log('init_keyboard_insert');

    // 취소 버튼 동작
    addDelegatedEvent('#workspace', '#btnInsertCancel', 'click', function(e, target) {
        e.stopPropagation();
        fetchWorkspace('keyboard-list');
    });

    // 추가버튼 동작
    addDelegatedEvent('#workspace', '#keyboardInsertForm', 'submit', function (e, form) {
        e.preventDefault(); // 폼의 기본 제출 동작을 방지
//  debugger;
        const formData = new FormData(form);
        var data = formToJson(formData);
        delete data.file_uploads; // 파일은 제외
        formData.append('keyboardData', JSON.stringify(data)); // JSON 문자열로 변환하여 추가

        // 파일 처리
        const fileTag = document.getElementById('file_uploads');
        if (fileTag && fileTag.files.length > 0) {
            Array.from(fileTag.files).forEach((file) => {
                formData.append('files', file); // 'files' 키로 각 파일 추가
            });
        }
        // JWT를 헤더에 추가
        const token = localStorage.getItem('token');

        // Fetch API를 사용하여 서버로 비동기 POST 요청 보냄
        fetch('/keyboard/insert', {
            method: 'POST',
            body: formData,
            headers: {
                'Authorization': 'Bearer ' + token
            },
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // 요청이 성공하면 view로 이동
            fetchWorkspace('keyboard-view', '/keyboard/' + data.id);
        })
        .catch(error => {
            console.error('실패:', error);
            showError(error);
        });
    });
}
// edit(수정)화면 초기화
function init_keyboard_edit(){
    console.log('init_keyboard_edit....');
    const form = document.getElementById('keyboardEditForm');
    if(!form){
        return;
    }
    form.addEventListener('submit', async function(e) {
        e.preventDefault(); // 폼의 기본 제출 동작을 방지
        e.stopPropagation();
        const keyboardId = document.getElementById('keyboardId').value;
        const formData = new FormData(this);

        // delete_file_ids 처리
        const deleteFileIds = [];
        document.querySelectorAll('input[type="checkbox"][name="delete_file_ids"]:checked').forEach(function(checkbox) {
            deleteFileIds.push(Number(checkbox.value));
        });

        const data = Object.fromEntries(formData.entries());
        delete data.file_uploads; // 파일은 제외
        data.delete_file_ids = deleteFileIds;

        // 파일 처리
        const fileTag = document.getElementById('file_uploads');
        if (fileTag && fileTag.files.length > 0) {
            Array.from(fileTag.files).forEach((file) => {
                formData.append('files', file); // 'files' 키로 각 파일 추가
            });
        }

        // JSON 데이터를 'keyboardFormData' 키에 추가합니다.
        formData.append('keyboardFormData', JSON.stringify(data));

        const token = localStorage.getItem('token');

        try {
            const response = await fetch(`/keyboard/${keyboardId}`, {
                method: 'PUT',
                body: formData, 
                headers: {
                    // 'Content-Type': 'multipart/form-data'는 자동으로 설정됩니다. Token만 직접 설정.
                    'Authorization': 'Bearer ' + token
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            // 요청이 성공하면 view로 이동
            fetchWorkspace('keyboard-view', '/keyboard/' + keyboardId);

        } catch (error) {
            // 요청이 실패하면 실행될 코드
            console.error('실패:', error);
            showError(error); 
        }
    });
}    
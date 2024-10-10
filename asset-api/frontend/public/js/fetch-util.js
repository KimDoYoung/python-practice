
/**
 * fetch API 호출시 server로 부터 받은 response가 에러인 경우 
 * status와 detail을 저장하는 Error클래스
 */
class LucyError extends Error {
    constructor(status, detail, server_time) {
        super(detail);
        this.status = status;
        this.server_time =server_time;
    }
    toString() {
        return `Error ${this.status}: ${this.message} (Server Time: ${this.server_time})`;
    }    
}
/**
 * 공통 fetch 함수
 * 
 * @param {string} url - 요청할 URL
 * @param {string} method - HTTP 메서드 ('GET', 'POST', 'PUT', 'DELETE')
 * @param {Object} [data] - 요청에 포함할 데이터 (옵션)
 * @returns {Promise<Object>} - 응답 데이터
 */
async function callLucyApi(url, method, data = null) {
    const token = localStorage.getItem('lucy_token');

    try {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            }
        };

        if (data) {
            options.body = JSON.stringify(data);
        }
        const response = await fetch(url, options);
        
        // 세션 타임아웃으로 인해 401 상태 코드가 반환되었는지 체크
        if (response.status === 401) {
            console.error('세션이 만료되었습니다.');
            // 사용자에게 로그인 페이지로 리다이렉트하도록 처리
            window.location.href = '/';
            return;
        }

        if (!response.ok) {
            console.error('에러 발생:', response);
            // 응답이 JSON인지 체크하여 에러 데이터 처리
            const contentType = response.headers.get('content-type');            
            if (contentType && contentType.includes('application/json')) {
                const errorData = await response.json();
                //errorData.detail이 배열이면 배열을 문자열로 변환
                if (Array.isArray(errorData.detail)){
                    errorData.detail = errorData.detail.join(', ');
                }
                throw new LucyError(response.status, errorData.detail, errorData.server_time);
            } else {
                throw new LucyError(response.status, 'Unexpected response format');
            }            
        }

        const responseData = await response.json();
        return responseData;
    } catch (error) {
        let errorStr = error.toString();
        if (errorStr.includes('SyntaxError: Unexpected end of JSON input')) {
            alert("세션 종료되었습니다. 서버와의 통신이 원활하지 않습니다. 다시 로그인해주세요.");
            window.location.href = '/';
        }else{
            throw new LucyError(error.status, error.message, error.server_time);
        }
    }
}

/**
 * GET 요청 함수
 * 
 * @param {string} url - 요청할 URL
 * @returns {Promise<Object>} - 응답 데이터
 */
async function getFetch(url) {
    return callLucyApi(url, 'GET');
}

/**
 * POST 요청 함수
 * 
 * @param {string} url - 요청할 URL
 * @param {Object} data - 요청에 포함할 데이터
 * @returns {Promise<Object>} - 응답 데이터
 */
async function postFetch(url, data) {
    return callLucyApi(url, 'POST', data);
}

/**
 * PUT 요청 함수
 * 
 * @param {string} url - 요청할 URL
 * @param {Object} data - 요청에 포함할 데이터
 * @returns {Promise<Object>} - 응답 데이터
 */
async function putFetch(url, data) {
    return callLucyApi(url, 'PUT', data);
}

/**
 * DELETE 요청 함수
 * 
 * @param {string} url - 요청할 URL
 * @param {Object} data - 요청에 포함할 데이터
 * @returns {Promise<Object>} - 응답 데이터
 */
async function deleteFetch(url, data) {
    return callLucyApi(url, 'DELETE', data);
}

/**
 * 서버로부터 handlebar template을 가져온다.
 * @param {*} hbs_file_path 
 * @returns 
 */
async function fetch_handlebar(hbs_file_path) {
    const response = await fetch(`/template?path=${hbs_file_path}`);
    if (!response.ok) {
        throw new LucyError(500, "Network response was not ok " + response.statusText);
    }
    const data = await response.json();
    return data.template;
}
/**
 * @param {*} hbs_file_path 
 * @returns 
 */
async function fetch_handlebar_and_compile(hbs_file_path) {
    const data = await fetch_handlebar(hbs_file_path);
    return Handlebars.compile(data);
}
/*
    사용법
    const pageCache = new TemplateCache();
    const template = await pageCache.getTemplate('example.html');
*/
class TemplateCache {
    constructor() {
        this.cacheTemplate = {};
    }

    async get(path) {
        if (!this.cacheTemplate[path]) {
            this.cacheTemplate[path] = fetch_handlebar_and_compile(path);
        }else{
            console.log("template cache 에 있는 것을 사용합니다."+path);
        }
        return this.cacheTemplate[path];
    }

    clearCache() {
        this.cacheTemplate = {};
    }
}

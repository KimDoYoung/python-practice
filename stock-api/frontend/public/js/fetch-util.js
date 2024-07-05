
/**
 * fetch API 호출시 server로 부터 받은 response가 에러인 경우 
 * status와 detail을 저장하는 Error클래스
 */
class StockApiError extends Error {
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
async function callStockApi(url, method, data = null) {
    // const token = localStorage.getItem('lucy_token');

    // try {

    // } catch (error) {
    //     console.error('에러 발생:', error.detail);
    //     throw error;
    // }
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
            // 'Authorization': 'Bearer ' + token
        }
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    const response = await fetch(url, options);

    if (!response.ok) {
        debugger;
        const errorData = await response.json();
        throw new StockApiError(response.status, errorData.detail, errorData.server_time);
    }

    const responseData = await response.json();
    return responseData;    
}

/**
 * GET 요청 함수
 * 
 * @param {string} url - 요청할 URL
 * @returns {Promise<Object>} - 응답 데이터
 */
async function getFetch(url) {
    return callStockApi(url, 'GET');
}

/**
 * POST 요청 함수
 * 
 * @param {string} url - 요청할 URL
 * @param {Object} data - 요청에 포함할 데이터
 * @returns {Promise<Object>} - 응답 데이터
 */
async function postFetch(url, data) {
    return callStockApi(url, 'POST', data);
}

/**
 * PUT 요청 함수
 * 
 * @param {string} url - 요청할 URL
 * @param {Object} data - 요청에 포함할 데이터
 * @returns {Promise<Object>} - 응답 데이터
 */
async function putFetch(url, data) {
    return callStockApi(url, 'PUT', data);
}

/**
 * DELETE 요청 함수
 * 
 * @param {string} url - 요청할 URL
 * @param {Object} data - 요청에 포함할 데이터
 * @returns {Promise<Object>} - 응답 데이터
 */
async function deleteData(url, data) {
    return callStockApi(url, 'DELETE', data);
}

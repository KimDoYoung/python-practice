import json

import requests
from backend.app.core.configs import KOREA_INVESTMENT_APP_KEY, KOREA_INVESTMENT_APP_SECRET,KOREA_INVESTMENT_URL_BASE


#
# 한국투자증권 API에서 access_token을 받아오는 함수
#
def get_access_token():
    print(f"APP_KEY:{KOREA_INVESTMENT_APP_KEY}")
    print(f"APP_SECRET:{KOREA_INVESTMENT_APP_SECRET}")
    
    APP_KEY = KOREA_INVESTMENT_APP_KEY
    APP_SECRET = KOREA_INVESTMENT_APP_SECRET
    URL_BASE = KOREA_INVESTMENT_URL_BASE

    headers = {"content-type":"application/json"}
    body = {"grant_type":"client_credentials",
            "appkey":APP_KEY, 
            "appsecret":APP_SECRET}
    PATH = "oauth2/tokenP"

    URL = f"{URL_BASE}/{PATH}"
    print(URL)
    
    res = requests.post(URL, headers=headers, data=json.dumps(body))
    print(res.text)
    access_token = res.json().get("access_token")
    print(access_token)
    return access_token

# 해시키 조회
def get_hashkey(datas):
    APP_KEY = KOREA_INVESTMENT_APP_KEY
    APP_SECRET = KOREA_INVESTMENT_APP_SECRET
    URL_BASE = KOREA_INVESTMENT_URL_BASE
    PATH = "uapi/hashkey"
    URL = f"{URL_BASE}/{PATH}"
    headers = {
        'content-Type' : 'application/json',
        'appKey' : APP_KEY,
        'appSecret' : APP_SECRET,
    }
    res = requests.post(URL, headers=headers, data=json.dumps(datas))
    hashkey = res.json()["HASH"]
    print(hashkey)
    return hashkey

# 현재 시장가 조회
def get_market_price(mrkt_div_code:str, stock_code:str):
    APP_KEY = KOREA_INVESTMENT_APP_KEY
    APP_SECRET = KOREA_INVESTMENT_APP_SECRET
    URL_BASE = KOREA_INVESTMENT_URL_BASE
    
    PATH = "uapi/domestic-stock/v1/quotations/inquire-price"
    URL = f"{URL_BASE}/{PATH}"
    print(URL)
    ACCESS_TOKEN = get_access_token()
    headers = {"Content-Type":"application/json", 
           "authorization": f"Bearer {ACCESS_TOKEN}",
           "appKey":APP_KEY,
           "appSecret":APP_SECRET,
           "tr_id":"FHKST01010100"}
    params = {
        "fid_cond_mrkt_div_code":mrkt_div_code,
        "fid_input_iscd": stock_code
    }
    json = {}
    res = requests.get(URL, headers=headers, params=params)
    json = res.json()
    return json
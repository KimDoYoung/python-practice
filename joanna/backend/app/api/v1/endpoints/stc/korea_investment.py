
import json
from fastapi import APIRouter
import requests

from backend.app.domains.stc.korea_investment.korea_investment_service import get_access_token, get_hashkey

from backend.app.core.logger import get_logger
from backend.app.core.configs import KOREA_INVESTMENT_APP_KEY, KOREA_INVESTMENT_APP_SECRET, KOREA_INVESTMENT_URL_BASE
logger = get_logger(__name__)

router = APIRouter()

@router.get("/stc/korea_investment/test1")
async def korea_investment_test1():
    '''
    한국투자증권을 통해서 얻은 현재시세
    '''
    # ACCESS_TOKEN = get_access_token();
    ACCESS_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6ImZhNDhjOWQ2LWFhMWUtNDQ4NS05ZGUxLWYyZmNkNDU5OGM5MCIsImlzcyI6InVub2d3IiwiZXhwIjoxNzEyMzgzMDM1LCJpYXQiOjE3MTIyOTY2MzUsImp0aSI6IlBTRVZ3QWY3alRya28wYkJlNklUNFhSVTdGOVFKdEpoa2ZPNSJ9.n1cWAWAlVlMshRcjyBn25BkyOibTK7mVBb9EHOG40Oee8rD5iEzBXNCxJOYe884Eui-o9YDkwCrdoJAJTY-wCQ'
    PATH = "uapi/domestic-stock/v1/quotations/inquire-price"
    URL = f"{KOREA_INVESTMENT_URL_BASE}/{PATH}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "appKey": KOREA_INVESTMENT_APP_KEY,
        "appSecret": KOREA_INVESTMENT_APP_SECRET,
        "tr_id" : "FHKST01010100"}
    params = {
        "fid_cond_mrkt_div_code":"J",
        "fid_input_iscd":"005930"
    }
    logger.debug("=====================================")
    logger.debug(f"URL:[{URL}]")
    logger.debug(f"ACCESS_TOKEN:[{ACCESS_TOKEN}]")
    logger.debug(f"header:[{headers}]")
    logger.debug(f"params:[{params}]")
    logger.debug("=====================================")
    res = requests.get(URL, headers=headers, params=params)  
    json = res.json()
    logger.debug(f"res:[{json}]")
    stck_prpr = json['output']['stck_prpr']    
    return {"message": "한국투자증권을 통해서 얻은 현재시세","stck_prpr":stck_prpr}

@router.get("/stc/korea_investment/test2")
async def korea_investment_test2():
    '''
    한국투자증권 : 주식 현재가 일자별 조회
    '''
    ACCESS_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6ImZhNDhjOWQ2LWFhMWUtNDQ4NS05ZGUxLWYyZmNkNDU5OGM5MCIsImlzcyI6InVub2d3IiwiZXhwIjoxNzEyMzgzMDM1LCJpYXQiOjE3MTIyOTY2MzUsImp0aSI6IlBTRVZ3QWY3alRya28wYkJlNklUNFhSVTdGOVFKdEpoa2ZPNSJ9.n1cWAWAlVlMshRcjyBn25BkyOibTK7mVBb9EHOG40Oee8rD5iEzBXNCxJOYe884Eui-o9YDkwCrdoJAJTY-wCQ'
    PATH = "uapi/domestic-stock/v1/quotations/inquire-daily-price"
    URL = f"{KOREA_INVESTMENT_URL_BASE}/{PATH}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "appKey": KOREA_INVESTMENT_APP_KEY,
        "appSecret": KOREA_INVESTMENT_APP_SECRET,
        "tr_id" : "FHKST01010400"}
    params = {
        "fid_cond_mrkt_div_code":"J", # 시장 구분 코드, 주식/ETF/ETN을 의미하는 'J'
        "fid_input_iscd":"005930", # 종목 코드, 삼성전자의 종목 코드 '005930'
        "fid_org_adj_prc":"0", # 수정주가 원주가, '0'으로 설정해 수정주가 반영
        "fid_period_div_code":"D" # 기간 분류 코드, 일자별 데이터를 의미하는 'D'
    }
    logger.debug("=====================================")
    logger.debug(f"URL:[{URL}]")
    logger.debug(f"ACCESS_TOKEN:[{ACCESS_TOKEN}]")
    logger.debug(f"header:[{headers}]")
    logger.debug(f"params:[{params}]")
    logger.debug("=====================================")    
    res = requests.get(URL, headers=headers, params=params)
    output = res.json()['output']
    logger.debug(f"output:[{output}]")
    logger.debug(f"size of output: [{output.__len__()}]") 
    stck_clpr = res.json()['output'][0]['stck_clpr']
    return {"message": "한국투자증권을 통해서 얻은 일자별 종가","stck_clpr":stck_clpr, "response_json":res.json()}

@router.get("/stc/korea_investment/test3")
async def korea_investment_test3():
    '''
    한국투자증권 : 주식주문(현금) 매수
    '''
    ACCESS_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6ImZhNDhjOWQ2LWFhMWUtNDQ4NS05ZGUxLWYyZmNkNDU5OGM5MCIsImlzcyI6InVub2d3IiwiZXhwIjoxNzEyMzgzMDM1LCJpYXQiOjE3MTIyOTY2MzUsImp0aSI6IlBTRVZ3QWY3alRya28wYkJlNklUNFhSVTdGOVFKdEpoa2ZPNSJ9.n1cWAWAlVlMshRcjyBn25BkyOibTK7mVBb9EHOG40Oee8rD5iEzBXNCxJOYe884Eui-o9YDkwCrdoJAJTY-wCQ'
    PATH = "uapi/domestic-stock/v1/trading/order-cash"
    URL = f"{KOREA_INVESTMENT_URL_BASE}/{PATH}"
    account_no = "50109129"
    account_no_front_8 = account_no[:8]
    account_no_back_2 = account_no[-2:]
   
    data = {
        "CANO": account_no_front_8, # 종합계좌번호, 모의투자계좌 앞 8자리
        "ACNT_PRDT_CD": account_no_back_2, # 계좌상품코드, 계좌번호 뒤 2자리
        "PDNO": "005930", # 상품번호, 삼성전자 종목 코드 '005930'
        "ORD_DVSN": "01", # 주문구분, 시장가 주문을 의미하는 '01'
        "ORD_QTY": "10", # 주문수량,  10주
        "ORD_UNPR": "0", # 주문단가, 시장가 주문 시 '0'으로 설정
    }
    hashkey = get_hashkey(data)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "appKey": KOREA_INVESTMENT_APP_KEY,
        "appSecret": KOREA_INVESTMENT_APP_SECRET,
        "tr_id":"VTTC0802U",
        "custtype":"P",
        "hashkey" : hashkey
    }

    logger.debug("=====================================")
    logger.debug(f"URL:[{URL}]")
    logger.debug(f"ACCESS_TOKEN:[{ACCESS_TOKEN}]")
    logger.debug(f"header:[{headers}]")
    logger.debug("=====================================")    
    res = requests.post(URL, headers=headers, data=json.dumps(data))
    
    output = res.json()
    logger.debug(f"output:[{output}]")
    return {"message": "한국투자증권 현금매수", "response_json":output}
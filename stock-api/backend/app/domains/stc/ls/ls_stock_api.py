# lsapi.py
"""
모듈 설명: 
    - LS에서 제공하는 API를 사용하기 위한 클래스
주요 기능:
/oauth2/tokenP
/uapi/hashkey
/uapi/domestic-stock/v1/quotations/inquire-price 
/uapi/domestic-stock/v1/trading/inquire-balance
/uapi/domestic-stock/v1/trading/order-cash - 
/uapi/domestic-stock/v1/quotations/search-stock-info
/uapi/domestic-stock/v1/quotations/psearch-title
/uapi/domestic-stock/v1/quotations/psearch-result
/uapi/domestic-stock/v1/trading/inquire-daily-ccld
/uapi/domestic-stock/v1/trading/order-rvsecncl
/uapi/domestic-stock/v1/trading/inquire-psbl-rvsecncl
/uapi/domestic-stock/v1/trading/inquire-psbl-order #매수가능조회
/uapi/domestic-stock/v1/trading/inquire-psbl-sell  #매도가능조회
/uapi/domestic-stock/v1/quotations/chk-holiday
에러 :
    -  Access Token은 하루 단위로 만료되므로, 만료되면 다시 발급해야 한다.
    - {'rt_cd': '1', 'msg_cd': 'EGW00123', 'msg1': '기간이 만료된 token 입니다.'}
작성자: 김도영
작성일: 07
버전: 1.0
"""
import json
import requests

from backend.app.core.logger import get_logger
from backend.app.domains.stc.stock_api import StockApi
from backend.app.domains.user.user_model import StkAccount, User
from backend.app.core.dependency import get_user_service
from backend.app.core.exception.stock_api_exceptions import KisAccessTokenExpireException
logger = get_logger(__name__)

class LsStockApi(StockApi):
    # _instance = None

    _BASE_URL = 'https://openapi.koreainvestment.com:9443'
    
    def __init__(self, user: User, account: StkAccount):
        super().__init__(user.user_id, account.account_no)
        self.HTS_USER_ID = self.get_key_value(self.user.key_values,"KIS_HTS_USER_ID")
        self.APP_KEY = self.get_key_value(self.user.key_values,"KIS_APP_KEY")
        self.APP_SECRET = self.get_key_value(self.user.key_values,"KIS_APP_SECRET")
        self.ACCTNO = self.get_key_value(self.user.key_values,"KIS_ACCTNO")
        access_token = self.get_key_value(self.user.key_values,"KIS_ACCESS_TOKEN")
        if access_token:
            self.ACCESS_TOKEN = access_token
        else:
            self.set_access_token_from_kis()


    async def initialize(self) -> bool:
        ''' Access Token 만료 여부 확인 '''
        try:
            cost = self.get_current_price("005930") # 삼성전자
        except KisAccessTokenExpireException as e:
            await self.set_access_token_from_kis()

        return True    

    async def set_access_token_from_kis(self)->str:
        ''' Access Token 발급을 kis 서버로부터 받아서 self에 채우고 users db에 넣는다. '''
        url = f'{self._BASE_URL}/oauth2/tokenP'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        body = {"grant_type":"client_credentials",
                "appkey":self.APP_KEY, 
                "appsecret":self.APP_SECRET}
        res = requests.post(url, headers=headers, data=json.dumps(body))
        
        ACCESS_TOKEN = res.json()["access_token"]
        
        self.ACCESS_TOKEN = ACCESS_TOKEN
        
        logger.debug("----------------------------------------------")
        logger.debug(f"ACCESS_TOKEN : [{ACCESS_TOKEN}]")
        logger.debug("----------------------------------------------")
        self.upsert_key_value(self.user.key_values, "KIS_ACCESS_TOKEN", ACCESS_TOKEN )
        #self.user.key_values["KIS_ACCESS_TOKEN"] = ACCESS_TOKEN
        # db에 저장
        logger.debug(f"self.user : {self.user.to_dict()}")
        user_service = get_user_service()
        await user_service.update_user(self.user.user_id, self.user)
        return ACCESS_TOKEN
    
    def hashkey(self, datas):
        """암호화"""
        url = self.BASE_URL + "/uapi/hashkey" #self._PATHS['암호화']
        headers = {
        'content-Type' : 'application/json',
        'appKey' : self.APP_KEY,
        'appSecret' : self.APP_SECRET
        }
        res = requests.post(url, headers=headers, data=json.dumps(datas))
        hashkey = res.json()["HASH"]
        return hashkey

# ls_stock_api.py
"""
모듈 설명: 
    - LS에서 제공하는 API를 사용하기 위한 클래스
주요 기능:

에러 :
    -  Access Token은 하루 단위로 만료되므로, 만료되면 다시 발급해야 한다.
작성자: 김도영
작성일: 2024-07-08
버전: 1.0
"""

import json
import requests

from backend.app.core.logger import get_logger
from backend.app.domains.stc.stock_api import StockApi
from backend.app.domains.user.user_model import StkAccount, User
from backend.app.core.exception.stock_api_exceptions import AccessTokenExpireException
logger = get_logger(__name__)

class LsStockApi(StockApi):

    _BASE_URL = "https://openapi.ls-sec.co.kr:8080"
    
    def __init__(self, user: User, account: StkAccount):
        super().__init__(user.user_id, account.account_no)
        self.APP_KEY = account.get_value("LS_APP_KEY")
        self.APP_SECRET = account.get_value("LS_APP_SECRET")
        self.ACCTNO = account.account_no
        access_token = account.get_value("LS_ACCESS_TOKEN")
        if access_token:
            self.ACCESS_TOKEN = access_token
        else:
            self.set_access_token_from_ls()


    async def initialize(self) -> bool:
        ''' Access Token 만료 여부 확인 '''
        try:
            cost = self.get_current_price("005930") # 삼성전자
        except AccessTokenExpireException as e:
            await self.set_access_token_from_ls()

        return True    

    async def set_access_token_from_ls(self)->str:
        ''' Access Token 발급을 LS 서버로부터 받아서 self에 채우고 users db에 넣는다. '''
        url = f'{self._BASE_URL}/oauth2/tokenP'
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Accept': 'application/json'
        }
        params = {
                    "grant_type":"client_credentials", 
                    "appkey":self.APP_KEY, 
                    "appsecretkey":self.APP_SECRET,
                    "scope":"oob"
                }        
        PATH = "oauth2/token"
        URL = f"{self._BASE_URL}/{PATH}"
        request = requests.post(URL, verify=False, headers=headers, params=params)
        if request.status_code != 200:
            logger.error(f"LS API Access Token 발급 실패 : {request.json()}")
            raise Exception(f"LS API Access Token 발급 실패 : {request.json()}")
        ACCESS_TOKEN = request.json()["access_token"]
        
        self.ACCESS_TOKEN = ACCESS_TOKEN
        
        logger.debug("----------------------------------------------")
        logger.debug(f"ACCESS_TOKEN : [{ACCESS_TOKEN}]")
        logger.debug("----------------------------------------------")

        self.account.set_value('LS_ACCESS_TOKEN', ACCESS_TOKEN)
        await self.user_service.update_user(self.user.user_id, self.user)
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

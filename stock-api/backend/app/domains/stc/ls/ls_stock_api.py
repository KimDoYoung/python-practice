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
from backend.app.domains.stc.ls.model.cspat00601_model import CSPAT00601_Request, CSPAT00601_Response
from backend.app.domains.stc.ls.model.cspat00701_model import CSPAT00701_Request, CSPAT00701_Response
from backend.app.domains.stc.ls.model.cspat00801_model import CSPAT00801_Request, CSPAT00801_Response
from backend.app.domains.stc.ls.model.t1102_model import T1102_Request, T1102_Response
from backend.app.domains.stc.stock_api import StockApi
from backend.app.domains.user.user_model import StkAccount, User
from backend.app.core.exception.stock_api_exceptions import CurrentCostException, InvalidResponseException
from datetime import datetime, timedelta
logger = get_logger(__name__)

class LsStockApi(StockApi):

    _BASE_URL = "https://openapi.ls-sec.co.kr:8080"
    
    def __init__(self, user: User, account: StkAccount):
        super().__init__(user.user_id, account.account_no)
        self.user = user
        self.account = account
        self.APP_KEY = account.get_value("LS_APP_KEY")
        self.APP_SECRET = account.get_value("LS_APP_SECRET")
        self.ACCTNO = account.account_no
        self.ACCESS_TOKEN = None
        self.ACCESS_TOKEN_TIME = None
        access_token = account.get_value("LS_ACCESS_TOKEN")
        if access_token:
            self.ACCESS_TOKEN = access_token
            self.ACCESS_TOKEN_TIME = account.get_value("LS_ACCESS_TOKEN_TIME")

    def get_access_token_time(self):
        if self.ACCESS_TOKEN_TIME:
            return datetime.strptime(self.ACCESS_TOKEN_TIME, "%Y-%m-%d %H:%M:%S")
        else:
            return None

    async def initialize(self) -> bool:
        ''' Access Token 만료 여부 확인 '''
        if self.ACCESS_TOKEN is None or self.ACCESS_TOKEN_TIME is None: # Access Token이 없으면 발급
            self.ACCESS_TOKEN = await self.set_access_token_from_ls()
            return True
        else: # Access Token이 있으면 12시간이 지났는지 체크 지났다면 다시 발급
            token_time = datetime.strptime(self.ACCESS_TOKEN_TIME, "%Y-%m-%d %H:%M:%S")
            if (datetime.now() - token_time) > timedelta(hours=12):
                self.ACCESS_TOKEN = await self.set_access_token_from_ls()
                self.ACCESS_TOKEN_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return True

    async def set_access_token_from_ls(self)->str:
        ''' Access Token 발급을 LS 서버로부터 받아서 self에 채우고 users db에 넣는다. '''
        PATH = "oauth2/token"
        URL = f"{self._BASE_URL}/{PATH}"
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
        self.account.set_value('LS_ACCESS_TOKEN_TIME', datetime.now().strftime("%Y-%m-%d %H:%M:%S")) # 하루로 설정
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

    async def current_cost(self, req: T1102_Request) -> T1102_Response:
        ''' 현재가 조회 : [주식] 시세-주식현재가(시세)조회 t'''
        PATH = "/stock/market-data"        
        url = f'{self._BASE_URL}/{PATH}'

        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization" : "Bearer " + self.ACCESS_TOKEN, 
            "tr_cd" : "t1102", #LS증권 거래코드
            "tr_cont" : req.tr_cont, #연속거래 여부 Y:연속○ N:연속×
            "tr_cont_key" : req.tr_cont_key, #연속일 경우 그전에 내려온 연속키 값 올림
            "mac_address" : req.mac_address, #법인인 경우 필수 세팅
        }

        data = {
            "t1102InBlock" : { 
                "shcode" : req.stk_code
            }
        }
        try:
            response = requests.post(url, verify=False, headers=headers, data=json.dumps(data))
            response.raise_for_status()  # HTTPError 발생 시 예외 처리
            response_data = response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"LS API 현재가 조회 실패: {e}")
            raise CurrentCostException(f"LS API 현재가 조회 실패: {e}")
        except json.JSONDecodeError:
            logger.error("응답이 JSON 형식이 아닙니다.")
            raise InvalidResponseException("응답이 JSON 형식이 아닙니다.")

        return T1102_Response(**response_data)


    async def order(self, req: CSPAT00601_Request) -> CSPAT00601_Response:
        ''' 현물 주문 '''
        PATH = "/stock/order"        
        url = f'{self._BASE_URL}/{PATH}'

        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization" : "Bearer " + self.ACCESS_TOKEN, 
            "tr_cd" : "CSPAT00601", #LS증권 거래코드
            "tr_cont" : req.tr_cont, #연속거래 여부 Y:연속○ N:연속×
            "tr_cont_key" : req.tr_cont_key, #연속일 경우 그전에 내려온 연속키 값 올림
            "mac_address" : req.mac_address, #법인인 경우 필수 세팅
        }

        data = {
            "CSPAT00601InBlock1" : req.CSPAT00601InBlock1.model_dump()
        }
        try:
            response = requests.post(url, verify=False, headers=headers, data=json.dumps(data))
            response.raise_for_status()  # HTTPError 발생 시 예외 처리
            response_data = response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"LS API 현재가 조회 실패: {e}")
            raise CurrentCostException(f"LS API 현재가 조회 실패: {e}")
        except json.JSONDecodeError:
            logger.error("응답이 JSON 형식이 아닙니다.")
            raise InvalidResponseException("응답이 JSON 형식이 아닙니다.")

        return CSPAT00601_Response(**response_data)

    async def modify_cash(self, req: CSPAT00701_Request) -> CSPAT00701_Response:
        ''' 현물 정정 주문'''
        PATH = "/stock/order"        
        url = f'{self._BASE_URL}/{PATH}'

        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization" : "Bearer " + self.ACCESS_TOKEN, 
            "tr_cd" : "CSPAT00701", #LS증권 거래코드
            "tr_cont" : req.tr_cont, #연속거래 여부 Y:연속○ N:연속×
            "tr_cont_key" : req.tr_cont_key, #연속일 경우 그전에 내려온 연속키 값 올림
            "mac_address" : req.mac_address, #법인인 경우 필수 세팅
        }

        data = {
            "CSPAT00701InBlock1" : req.CSPAT00701InBlock1.model_dump()
        }
        try:
            response = requests.post(url, verify=False, headers=headers, data=json.dumps(data))
            response.raise_for_status()  # HTTPError 발생 시 예외 처리
            response_data = response.json()
            logger.debug(f"response_data : {response_data}")
        except requests.exceptions.RequestException as e:
            logger.error(f"LS API 현재가 조회 실패: {e}")
            raise CurrentCostException(f"LS API 현재가 조회 실패: {e}")
        except json.JSONDecodeError:
            logger.error("응답이 JSON 형식이 아닙니다.")
            raise InvalidResponseException("응답이 JSON 형식이 아닙니다.")

        return CSPAT00701_Response(**response_data)

    async def cancel_cash(self, req: CSPAT00801_Request) -> CSPAT00801_Response:
        ''' 현물 취소 주문 '''
        PATH = "/stock/order"        
        url = f'{self._BASE_URL}/{PATH}'

        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization" : "Bearer " + self.ACCESS_TOKEN, 
            "tr_cd" : "CSPAT00601", #LS증권 거래코드
            "tr_cont" : req.tr_cont, #연속거래 여부 Y:연속○ N:연속×
            "tr_cont_key" : req.tr_cont_key, #연속일 경우 그전에 내려온 연속키 값 올림
            "mac_address" : req.mac_address, #법인인 경우 필수 세팅
        }

        data = {
            "CSPAT00801InBlock1" : req.CSPAT00801InBlock1.model_dump()
        }
        try:
            response = requests.post(url, verify=False, headers=headers, data=json.dumps(data))
            response.raise_for_status()  # HTTPError 발생 시 예외 처리
            response_data = response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"LS API 현재가 조회 실패: {e}")
            raise CurrentCostException(f"LS API 현재가 조회 실패: {e}")
        except json.JSONDecodeError:
            logger.error("응답이 JSON 형식이 아닙니다.")
            raise InvalidResponseException("응답이 JSON 형식이 아닙니다.")

        return CSPAT00801_Response(**response_data)
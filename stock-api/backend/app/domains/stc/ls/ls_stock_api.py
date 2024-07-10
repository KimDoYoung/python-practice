# ls_stock_api.py
"""
모듈 설명: 
    - LS에서 제공하는 API를 사용하기 위한 클래스
주요 기능:

에러 :
    - Access Token은 하루 단위로 만료되므로, 만료되면 다시 발급해야 한다.
작성자: 김도영
작성일: 2024-07-08
버전: 1.0
"""

import json
import requests
from datetime import datetime, timedelta

from backend.app.core.logger import get_logger
from backend.app.domains.stc.ls.model.cdpcq04700_model import CDPCQ04700_Request, CDPCQ04700_Response
from backend.app.domains.stc.ls.model.cspaq13700_model import CSPAQ13700_Request, CSPAQ13700_Response
from backend.app.domains.stc.ls.model.cspat00601_model import CSPAT00601_Request, CSPAT00601_Response
from backend.app.domains.stc.ls.model.cspat00701_model import CSPAT00701_Request, CSPAT00701_Response
from backend.app.domains.stc.ls.model.cspat00801_model import CSPAT00801_Request, CSPAT00801_Response
from backend.app.domains.stc.ls.model.t0425_model import T0425_Request, T0425_Response
from backend.app.domains.stc.ls.model.t1102_model import T1102_Request, T1102_Response
from backend.app.domains.stc.stock_api import StockApi
from backend.app.domains.user.user_model import StkAccount, User
from backend.app.core.exception.stock_api_exceptions import CurrentCostException, InvalidResponseException

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
        self.ACCESS_TOKEN = account.get_value("LS_ACCESS_TOKEN")
        self.ACCESS_TOKEN_TIME = account.get_value("LS_ACCESS_TOKEN_TIME")

    def get_access_token_time(self):
        if self.ACCESS_TOKEN_TIME:
            return datetime.strptime(self.ACCESS_TOKEN_TIME, "%Y-%m-%d %H:%M:%S")
        return None

    async def initialize(self) -> bool:
        ''' Access Token 만료 여부 확인 '''
        if not self.ACCESS_TOKEN or not self.ACCESS_TOKEN_TIME:
            self.ACCESS_TOKEN = await self.set_access_token_from_ls()
        else:
            token_time = self.get_access_token_time()
            if token_time and (datetime.now() - token_time) > timedelta(hours=12):
                self.ACCESS_TOKEN = await self.set_access_token_from_ls()
                self.ACCESS_TOKEN_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return True

    async def set_access_token_from_ls(self) -> str:
        ''' Access Token 발급을 LS 서버로부터 받아서 self에 채우고 users db에 넣는다. '''
        PATH = "oauth2/token"
        URL = f"{self._BASE_URL}/{PATH}"
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Accept': 'application/json'
        }
        params = {
            "grant_type": "client_credentials",
            "appkey": self.APP_KEY,
            "appsecretkey": self.APP_SECRET,
            "scope": "oob"
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
        url = self._BASE_URL + "/uapi/hashkey"
        headers = {
            'content-Type': 'application/json',
            'appKey': self.APP_KEY,
            'appSecret': self.APP_SECRET
        }
        res = requests.post(url, headers=headers, data=json.dumps(datas))
        return res.json()["HASH"]

    async def send_request(self, request_dict: dict):
        ''' LS증권으로 요청을 보내고 응답을 받는다.'''
        url = f'{self._BASE_URL}/{request_dict["path"]}'
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": "Bearer " + self.ACCESS_TOKEN,
            "tr_cd": request_dict["tr_cd"],
            "tr_cont": request_dict["tr_cont"],
            "tr_cont_key": request_dict["tr_cont_key"],
            "mac_address": request_dict["mac_address"]
        }
        data = request_dict["data"]
        logger.debug(f"-------------------------------------------------------------")
        logger.debug(f"API 요청 : URL=[{url}], Headers=[{headers}], Data=[{data}]")
        logger.debug(f"-------------------------------------------------------------")
        try:
            response = requests.post(url, verify=False, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            response_data = response.json()
            logger.debug(f"-------------------------------------------------------------")
            logger.debug(f"API 응답 {request_dict["tr_cd"]} : [{response_data}]")
            logger.debug(f"-------------------------------------------------------------")
        except requests.exceptions.RequestException as e:
            logger.error(f"API 요청 실패: {e}")
            raise CurrentCostException(f"API 요청 실패: {e}")
        except json.JSONDecodeError:
            logger.error("응답이 JSON 형식이 아닙니다.")
            raise InvalidResponseException("응답이 JSON 형식이 아닙니다.")

        return response_data

    async def current_cost(self, req: T1102_Request) -> T1102_Response:
        ''' 현재가 조회 : [주식] 시세-주식현재가(시세)조회 t'''
        req_dict = {
            "path": "/stock/market-data",
            "tr_cd": "t1102",
            "tr_cont": req.tr_cont,
            "tr_cont_key": req.tr_cont_key,
            "mac_address": req.mac_address,
            "data": {
                "t1102InBlock": {
                    "shcode": req.stk_code
                }
            }
        }
        response_data = await self.send_request(req_dict)
        return T1102_Response(**response_data)

    async def order(self, req: CSPAT00601_Request) -> CSPAT00601_Response:
        ''' 현물 주문 '''
        req_dict = {
            "path": "/stock/order",
            "tr_cd": "CSPAT00601",
            "tr_cont": req.tr_cont,
            "tr_cont_key": req.tr_cont_key,
            "mac_address": req.mac_address,
            "data": {
                "CSPAT00601InBlock1": req.CSPAT00601InBlock1.model_dump()
            }
        }
        response_data = await self.send_request(req_dict)
        return CSPAT00601_Response(**response_data)

    async def modify_cash(self, req: CSPAT00701_Request) -> CSPAT00701_Response:
        ''' 현물 정정 주문'''
        req_dict = {
            "path": "/stock/order",
            "tr_cd": "CSPAT00701",
            "tr_cont": req.tr_cont,
            "tr_cont_key": req.tr_cont_key,
            "mac_address": req.mac_address,
            "data": {
                "CSPAT00701InBlock1": req.CSPAT00701InBlock1.model_dump()
            }
        }
        response_data = await self.send_request(req_dict)
        return CSPAT00701_Response(**response_data)

    async def cancel_cash(self, req: CSPAT00801_Request) -> CSPAT00801_Response:
        ''' 현물 취소 주문 '''
        req_dict = {
            "path": "/stock/order",
            "tr_cd": "CSPAT00801",
            "tr_cont": req.tr_cont,
            "tr_cont_key": req.tr_cont_key,
            "mac_address": req.mac_address,
            "data": {
                "CSPAT00801InBlock1": req.CSPAT00801InBlock1.model_dump()
            }
        }
        response_data = await self.send_request(req_dict)
        return CSPAT00801_Response(**response_data)

    async def acct_history(self, req: CDPCQ04700_Request) -> CDPCQ04700_Response:
        ''' 계좌별 거래내역 및 잔고 등 계좌에 관련된 서비스를 확인'''
        req_dict = {
            "path": "/stock/accno",
            "tr_cd": "CDPCQ04700",
            "tr_cont": req.tr_cont,
            "tr_cont_key": req.tr_cont_key,
            "mac_address": req.mac_address,
            "data": {
                "CDPCQ04700InBlock1": req.CDPCQ04700InBlock1.model_dump()
            }
        }
        response_data = await self.send_request(req_dict)
        return CDPCQ04700_Response(**response_data)

    async def fulfill_list(self, req: T0425_Request) -> T0425_Response:
        '''체결/미체결'''
        req_dict = {
            "path": "/stock/accno",
            "tr_cd": "t0425",
            "tr_cont": req.tr_cont,
            "tr_cont_key": req.tr_cont_key,
            "mac_address": req.mac_address,
            "data": {
                "t0425InBlock": req.t0425InBlock.model_dump()
            }
        }
        response_data = await self.send_request(req_dict)
        return T0425_Response(**response_data)

    async def fulfill_api_list(self, req: CSPAQ13700_Request) -> CSPAQ13700_Response:
        '''OPENAPI용 체결/미체결 조회 '''
        req_dict = {
            "path": "/stock/accno",
            "tr_cd": "CSPAQ13700",
            "tr_cont": req.tr_cont,
            "tr_cont_key": req.tr_cont_key,
            "mac_address": req.mac_address,
            "data": {
                "CSPAQ13700InBlock1": req.CSPAQ13700InBlock1.model_dump()
            }
        }
        response_data = await self.send_request(req_dict)
        return CSPAQ13700_Response(**response_data)

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
from backend.app.domains.stc.ls.model.cspaq12300_model import CSPAQ12300_Request, CSPAQ12300_Response
from backend.app.domains.stc.ls.model.cspaq13700_model import CSPAQ13700_Request, CSPAQ13700_Response
from backend.app.domains.stc.ls.model.cspat00601_model import CSPAT00601_Request, CSPAT00601_Response
from backend.app.domains.stc.ls.model.cspat00701_model import CSPAT00701_Request, CSPAT00701_Response
from backend.app.domains.stc.ls.model.cspat00801_model import CSPAT00801_Request, CSPAT00801_Response
from backend.app.domains.stc.ls.model.t0424_model import T0424_Request, T0424_Response
from backend.app.domains.stc.ls.model.t0425_model import T0425_Request, T0425_Response
from backend.app.domains.stc.ls.model.t1102_model import T1102_Request, T1102_Response
from backend.app.domains.stc.ls.model.t1441_model import T1441_Request, T1441_Response
from backend.app.domains.stc.ls.model.t1452_model import T1452_Request, T1452_Response
from backend.app.domains.stc.ls.model.t1463_model import T1463_Request, T1463_Response
from backend.app.domains.stc.ls.model.t1466_model import T1466_Request, T1466_Response
from backend.app.domains.stc.ls.model.t1481_model import T1481_Request, T1481_Response
from backend.app.domains.stc.ls.model.t1482_model import T1482_Request, T1482_Response
from backend.app.domains.stc.ls.model.t1489_model import T1489_Request, T1489_Response
from backend.app.domains.stc.ls.model.t1492_model import T1492_Request, T1492_Response
from backend.app.domains.stc.ls.model.t8407_model import T8407_Request, T8407_Response
from backend.app.domains.stc.ls.model.t9945_model import T9945_Response
from backend.app.domains.stc.stock_api import StockApi
from backend.app.domains.user.user_model import StkAccount, User
from backend.app.core.exception.stock_api_exceptions import LsApiException, InvalidResponseException

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

    async def send_request(self, request_dict: dict):
        ''' LS증권으로 요청을 보내고 응답을 받는다.'''
        url = f'{self._BASE_URL}/{request_dict["path"]}'
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": "Bearer " + self.ACCESS_TOKEN,
            "tr_cd": request_dict["tr_cd"],
            "tr_cont": request_dict.get("tr_cont","N"),
            "tr_cont_key":request_dict.get("tr_cont_key",""),
            "mac_address": request_dict.get("mac_address","")
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
            raise LsApiException(f"API 요청 실패: {e}")
        except json.JSONDecodeError:
            logger.error("응답이 JSON 형식이 아닙니다.")
            raise InvalidResponseException("응답이 JSON 형식이 아닙니다.")

        return response_data

    async def current_cost(self, req: T1102_Request) -> T1102_Response:
        ''' 현재가 조회 : [주식] 시세-주식현재가(시세)조회 t'''
        req_dict = {
            "path": "/stock/market-data",
            "tr_cd": "t1102",
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
            "data": {
                "CSPAQ13700InBlock1": req.CSPAQ13700InBlock1.model_dump()
            }
        }
        response_data = await self.send_request(req_dict)
        return CSPAQ13700_Response(**response_data)

    async def master_api(self, gubun:str) -> T9945_Response:
        '''  [주식] 시세-주식마스터조회API용 '''
        req_dict = {
            "path": "/stock/market-data",
            "tr_cd": "t9945",
            "data": {
                "t9945InBlock": {
                    "gubun" : gubun
                }
            }
        }
        response_data = await self.send_request(req_dict)
        return T9945_Response(**response_data)

    async def multi_current_cost(self, req:T8407_Request) -> T8407_Response:
        ''' [주식] 시세-API용주식멀티현재가조회 '''
        req_dict = {
            "path": "/stock/market-data",
            "tr_cd": "t8407",
            "data": {
                "t8407InBlock": req.t8407InBlock.model_dump()
            }
        }
        response_data = await self.send_request(req_dict)
        return T8407_Response(**response_data)

    async def jango2(self, req:T0424_Request) -> T0424_Response:
        '''[주식] 계좌-주식잔고2  '''
        req_dict = {
            "path": "/stock/accno",
            "tr_cd": "t0424",
            "data": {
                "t0424InBlock": req.t0424InBlock.model_dump()
            }
        }
        response_data = await self.send_request(req_dict)
        return T0424_Response(**response_data)
    
    async def bep_danga(self, req:CSPAQ12300_Request) -> CSPAQ12300_Response:
        '''[주식] 계좌-BEP단가조회'''
        req_dict = {
            "path": "/stock/accno",
            "tr_cd": "CSPAQ12300",
            "data": {
                "CSPAQ12300InBlock1": req.CSPAQ12300InBlock1.model_dump()
            }
        }
        response_data = await self.send_request(req_dict)
        return CSPAQ12300_Response(**response_data)

#--------------------------------------------------------------------------------------
# 상위랭크 route
#--------------------------------------------------------------------------------------
    async def rank_range(self, req:T1441_Request) -> T1441_Response:
        '''[주식] 상위종목 : 등락률'''
        req_dict = {
            "path": "/stock/high-item",
            "tr_cd": "t1441",
            "tr_cont": req.tr_cont,
            "data": {
                "t1441InBlock": req.t1441InBlock.model_dump()
            }
        }
        response_data = await self.send_request(req_dict)
        return T1441_Response(**response_data)
    
    async def rank_volumn(self, req:T1452_Request) -> T1452_Response:
        '''[주식] 상위종목-거래량상위'''
        req_dict = {
            "path": "/stock/high-item",
            "tr_cd": "t1452",
            "data": {
                "t1452InBlock": req.t1452InBlock.model_dump()
            }
        }
        response_data = await self.send_request(req_dict)
        return T1452_Response(**response_data)
    
    async def rank_rapidup(self, req:T1466_Request) -> T1466_Response:
        '''[주식] 상위종목-전일동시간대비거래급증 '''
        req_dict = {
            "path": "/stock/high-item",
            "tr_cd": "t1466",
            "data": {
                "t1466InBlock": req.t1466InBlock.model_dump()
            }
        }
        response_data = await self.send_request(req_dict)
        return T1466_Response(**response_data)
    
    async def rank_timeout_range(self, req:T1481_Request) -> T1481_Response:
        '''[주식] 상위종목-시간외등락율상위 '''
        req_dict = {
            "path": "/stock/high-item",
            "tr_cd": "t1481",
            "data": {
                "t1481InBlock": req.t1481InBlock.model_dump()
            }
        }
        response_data = await self.send_request(req_dict)
        return T1481_Response(**response_data)
    
    async def rank_timeout_volume(self, req:T1482_Request) -> T1482_Response:
        '''[주식] 상위종목-시간외거래량상위 '''
        req_dict = {
            "path": "/stock/high-item",
            "tr_cd": "t1482",
            "data": {
                "t1481InBlock": req.t1482InBlock.model_dump()
            }
        }
        response_data = await self.send_request(req_dict)
        return T1482_Response(**response_data)
    
    async def rank_expect_filfull(self, req:T1489_Request) -> T1489_Response:
        '''[주식]  상위종목-예상체결량상위조회 '''
        req_dict = {
            "path": "/stock/high-item",
            "tr_cd": "t1489",
            "data": {
                "t1489InBlock": req.t1489InBlock.model_dump()
            }
        }
        response_data = await self.send_request(req_dict)
        return T1489_Response(**response_data)    

    async def rank_expect_danilga_range(self, req:T1492_Request) -> T1492_Response:
        '''[주식]  상위종목-단일가예상등락율상위 '''
        req_dict = {
            "path": "/stock/high-item",
            "tr_cd": "t1492",
            "data": {
                "t1492InBlock": req.t1492InBlock.model_dump()
            }
        }
        response_data = await self.send_request(req_dict)
        return T1492_Response(**response_data)

    async def rank_purchase_cost(self, req:T1463_Request) -> T1463_Response:
        '''[주식]  상위종목-거래대금상위  '''
        req_dict = {
            "path": "/stock/high-item",
            "tr_cd": "t1463",
            "tr_cont": req.tr_cont,
            "data": {
                "t1463InBlock": req.t1463InBlock.model_dump()
            }
        }
        response_data = await self.send_request(req_dict)
        return T1463_Response(**response_data)
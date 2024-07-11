# ls_ws_task.py
"""
모듈 설명: 
    - LS증권 Websocket Client Task
주요 기능:
    -   기능을 넣으시오

작성자: 김도영
작성일: 2024-07-11
버전: 1.0
"""
import asyncio
from datetime import datetime, timedelta

import websockets
from backend.app.managers.client_ws_manager import ClientWsManager
from backend.app.utils.ls_ws_util import LS_WSReq, ls_ws_response_factory, new_ls_ws_request
from backend.app.core.dependency import get_user_service
from backend.app.core.logger import get_logger
logger = get_logger(__name__)

class LSTask:
    def __init__(self, user_id:str, acctno:str, client_ws_manager: ClientWsManager):        
        self.client_ws_manager = client_ws_manager
        self.user_id = user_id
        self.url = "wss://openapi.ls-sec.co.kr:9443/websocket"
        self.abbr = 'LS'
        self.user_service = get_user_service()
        self.stk_websocket = None
        self.user = None
        self.acctno = acctno
        self.account = None
        logger.debug(f"{self.user_id}/{self.acctno}/{self.abbr} 증권사 웹소켓 생성")
        self.request_data = None

    async def fill_request_data(self):
        self.request_data = {
            LS_WSReq.뉴스: {
                "tr_cd": "NWS",
                "tr_key": "NWS001"
            },
            LS_WSReq.주식주문체결: {
                "tr_cd": "SC1",
                "tr_key": ""
            },
        }

    async def initialize(self):
        await self.fill_request_data()
        self.user = await self.user_service.get_1(self.user_id)
        if self.user is not None:
            self.account = self.user.find_account(self.acctno)
            #TODO 만약 없다면 또는 이미 expire되었다면
            access_token = self.user.get_value_in_accounts("LS_ACCESS_TOKEN")
            access_token_time = self.user.get_value_in_accounts("LS_ACCESS_TOKEN_TIME")
            if access_token is None:
                #TODO access_token 발급
                access_token, access_token_time = await self.get_new_access_token()
            else:
                access_token_time = self.user.get_value_in_accounts("LS_ACCESS_TOKEN_TIME")
                if access_token_time is not None:
                    access_token_time_dt = datetime.strptime(access_token_time, "%Y-%m-%d %H:%M:%S")                    
                    # access_token_time_dt와 현재 시간 비교
                    if access_token_time_dt + timedelta(hours=12) < datetime.now():
                        access_token, access_token_time = await self.get_new_access_token()

            self.ACCESS_TOKEN = access_token
            self.LS_ACCESS_TOKEN_TIME = access_token_time
            logger.info(f"LS access_token: {self.ACCESS_TOKEN}")
            logger.info(f"LS access_token_time: {self.LS_ACCESS_TOKEN_TIME}")
        else:
            return{"code":"14", "detail": f"{self.user_id}/{self.acctno}/{self.abbr} 사용자가 없습니다."}

        logger.debug(f"{self.user_id}/{self.acctno}/{self.abbr} 증권사 웹소켓 초기화 완료")
        return {"code":"00", "detail": f"{self.user_id}/{self.acctno}/{self.abbr} 증권사 웹소켓 초기화 완료"}

    async def get_new_access_token(self):
        #TODO access_token 발급
        return "access_token", datetime.now()

    async def create_ls_ws_request(self, tr_type:str, data:dict):
        req = new_ls_ws_request()
        req.header.token = self.ACCESS_TOKEN
        req.header.tr_type = tr_type
        req.body.tr_cd = data['tr_cd']
        req.body.tr_key = data['tr_key']
        senddata = req.model_dump_json()
        return senddata

    async def subscribe(self, req: LS_WSReq):
        if req == LS_WSReq.뉴스:
            return await self.create_ls_ws_request("3", self.request_data[req])
        elif req == LS_WSReq.주식주문체결:
            return await self.create_ls_ws_request("1", self.request_data[req])

    async def on_open(self):

        #고객체결발생통보 등록
        websocket = self.stk_websocket
        senddata = await self.subscribe(LS_WSReq.뉴스)
        
        await websocket.send(senddata)
        logger.debug(f"{self.user_id}/{self.acctno}/{self.abbr} 체결통보 등록 senddata: [{senddata}]")
        await asyncio.sleep(0.5)

    async def run(self, user_id: str):
        logger.debug(f"{self.user_id}/{self.acctno}/{self.abbr} 증권사 웹소켓 시작")
        try:
            async with websockets.connect(self.url, ping_interval=None) as websocket:
                self.stk_websocket = websocket
                await self.on_open()
                if self.stk_websocket is None:
                    raise Exception("korea_investment_websocket 웹소켓 연결이 안됨")

                while True:
                    received_text = await websocket.recv()
                    ls_response = ls_ws_response_factory(received_text)
                    #TODO ls_response.data_for_client_ws(self)를 만들자.
                    logger.info("웹소켓(KIS로부터 받은데이터) : [" + received_text + "]")
                    
                    
        except websockets.exceptions.ConnectionClosed as e:
            logger.error(f"{self.user_id}/{self.acctno}/{self.abbr} 웹소켓 연결이 닫혔습니다: {e}")
        except Exception as e:
            logger.error(f"{self.user_id}/{self.acctno}/{self.abbr} 웹소켓 연결 중 에러 발생: {e}")
        finally:
            logger.debug(f"{self.user_id}/{self.acctno}/{self.abbr} finally 증권사 웹소켓 close")
            self.stk_websocket = None

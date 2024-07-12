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
import json

import requests
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
            self.APP_KEY = self.account.get_value("LS_APP_KEY")
            self.APP_SECRET = self.account.get_value("LS_APP_SECRET")            
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
        ''' LS API Access Token 발급 '''
        URL = f"https://openapi.ls-sec.co.kr:8080/oauth2/token"
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
        ACCESS_TOKEN_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")      
        logger.debug("----------------------------------------------")
        logger.debug(f"ACCESS_TOKEN : [{ACCESS_TOKEN}]")
        logger.debug("----------------------------------------------")

        self.account.set_value('LS_ACCESS_TOKEN', ACCESS_TOKEN)
        self.account.set_value('LS_ACCESS_TOKEN_TIME',ACCESS_TOKEN_TIME) # 하루로 설정
        await self.user_service.update_user(self.user.user_id, self.user)
        return ACCESS_TOKEN, ACCESS_TOKEN_TIME

    async def create_ls_ws_request(self, tr_type:str, data:dict):
        ''' LS 웹소켓 요청 문자열(json형태의 문자열) 생성 '''
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
        
    async def unsubscribe(self, req: LS_WSReq):
        if req == LS_WSReq.뉴스:
            return await self.create_ls_ws_request("4", self.request_data[req])
        elif req == LS_WSReq.주식주문체결:
            return await self.create_ls_ws_request("2", self.request_data[req])

    async def on_open(self):

        #고객체결발생통보 등록
        websocket = self.stk_websocket
        # senddata = await self.subscribe(LS_WSReq.뉴스)
        senddata = await self.subscribe(LS_WSReq.주식주문체결)
        await websocket.send(senddata)
        logger.debug(f"{self.user_id}/{self.acctno}/{self.abbr} 체결통보 등록 senddata: [{senddata}]")
        await asyncio.sleep(0.5)

    async def broadcast(self, message: str):
        #msg = await self.make_message(message)
        msg = message
        logger.debug(msg)
        await self.client_ws_manager.send_to_client(msg, self.user_id)

    async def run(self):
        logger.debug(f"{self.user_id}/{self.acctno}/{self.abbr} 증권사 웹소켓 시작")
        try:
            async with websockets.connect(self.url, ping_interval=30) as websocket:
                self.stk_websocket = websocket
                await self.on_open()
                if self.stk_websocket is None:
                    raise Exception("LS증권 웹소켓 연결이 안됨")

                while True:
                    try:
                        received_text = await websocket.recv()
                        logger.info("웹소켓(KIS로부터 받은데이터) : [" + received_text + "]")

                        real_model = ls_ws_response_factory(received_text)
                        real_data_dict = real_model.data_for_client_ws()
                        message_str = json.dumps(real_data_dict, ensure_ascii=False)
                        await self.broadcast(message_str)
                        await asyncio.sleep(0.5)
                    except json.JSONDecodeError as e:
                            logger.error(f"{self.user_id}/{self.acctno}/{self.abbr} JSON decoding error: {e}")
                    except websockets.ConnectionClosed as e:
                            logger.error(f"{self.user_id}/{self.acctno}/{self.abbr}  WebSocket connection closed: {e}")
                            break
                    except Exception as e:
                            logger.error(f"Unexpected error: {e}")                        
                    
        except websockets.exceptions.ConnectionClosed as e:
            logger.error(f"{self.user_id}/{self.acctno}/{self.abbr} 웹소켓 연결이 닫혔습니다: {e}")
        except Exception as e:
            logger.error(f"{self.user_id}/{self.acctno}/{self.abbr} 웹소켓 연결 중 에러 발생: {e}")
        finally:
            msg = f"{self.user_id}/{self.acctno}/{self.abbr} finally 증권사 웹소켓 close"
            logger.debug(msg)
            await self.broadcast(msg)
            self.stk_websocket = None

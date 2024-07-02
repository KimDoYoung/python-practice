import asyncio
from datetime import datetime
import json

import websockets
from backend.app.background.design.managers.client_ws_manager import ClientWsManager
from backend.app.core.logger import get_logger
from backend.app.domains.stc.kis.model.kis_websocket_model import KisWsResponse
from backend.app.utils.kis_ws_util import KIS_WSReq, get_ws_approval_key, is_real_data, kis_ws_real_data_parsing, new_kis_ws_request
from backend.app.core.dependency import get_user_service

logger = get_logger(__name__)

#TODO BASE가 있어야하지않을까?
class KISTask:
    def __init__(self, user_id:str, acctno:str, client_ws_manager: ClientWsManager):
        self.client_ws_manager = client_ws_manager
        self.user_id = user_id
        self.url = "ws://ops.koreainvestment.com:21000"
        self.abbr = 'KIS'
        self.user_service = get_user_service()
        self.stk_websocket = None
        self.user = None
        self.acctno = acctno
        self.account = None
        logger.debug(f"{self.user_id}/{self.acctno}/{self.abbr} 증권사 웹소켓 생성")

    async def initialize(self) -> dict:
        self.user = await self.user_service.get_1(self.user_id)
        if self.user is not None:
            self.account = self.user.find_account(self.acctno)
            self.APP_KEY = self.user.get_value_in_accounts("KIS_APP_KEY")
            self.APP_SECRET = self.user.get_value_in_accounts("KIS_APP_SECRET")
            self.HTS_USER_ID = self.user.get_value_in_accounts("KIS_HTS_USER_ID")
            self.APPROVAL_KEY = None
            self.AES_IV = None
            self.AES_KEY = None

            #필요한 변수들 체크 
            if self.APP_KEY is None :
                return{"code":"11", "detail": f"{self.user_id}/{self.acctno}/{self.abbr} APP_KEY 가 없습니다."}
            elif self.APP_SECRET is None:
                return{"code":"12", "detail": f"{self.user_id}/{self.acctno}/{self.abbr} APP_SECRET 가 없습니다."}
            elif self.HTS_USER_ID is None:
                return{"code":"13", "detail": f"{self.user_id}/{self.acctno}/{self.abbr} HTS_USER_ID 가 없습니다."}
        else:
            return{"code":"14", "detail": f"{self.user_id}/{self.acctno}/{self.abbr} 사용자가 없습니다."}

        logger.debug(f"{self.user_id}/{self.acctno}/{self.abbr} 증권사 웹소켓 초기화 완료")
        return {"code":"00", "detail": f"{self.user_id}/{self.acctno}/{self.abbr} 증권사 웹소켓 초기화 완료"}

    async def make_message(self, message:str):
        now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return  f"{now_time}|{self.user_id}|{self.acctno}|{self.abbr}|{message}"
    
    async def broadcast(self, message: str):
        msg = await self.make_message(message)
        logger.debug(msg)
        await self.client_ws_manager.send_to_client(msg, self.user_id)

    async def create_kis_ws_request(self, tr_id, tr_type, tr_key):
        ''' KIS에 요청을 보내기 위한 데이터 생성'''
        approval_key = self.APPROVAL_KEY
        if not approval_key:

            approval_key = get_ws_approval_key(self.APP_KEY, self.APP_SECRET)    
            self.APPROVAL_KEY = approval_key

        req = new_kis_ws_request()
        req.header.approval_key = approval_key
        req.header.personalseckey = self.APP_SECRET
        req.header.tr_type = tr_type
        req.body.input.tr_id = tr_id
        req.body.input.tr_key = tr_key
        senddata = req.model_dump_json()
        
        logger.debug(f"{self.user_id}/{self.acctno}/{self.abbr} : 증권사에 보낸 데이터[{senddata}]")
        
        return senddata

    async def subscribe(self, tr_id, stock_code):

        if tr_id in [KIS_WSReq.BID_ASK, KIS_WSReq.CONTRACT]:
            return await self.create_kis_ws_request(tr_id, '1', stock_code)
        elif tr_id == KIS_WSReq.NOTICE:
            return await self.create_kis_ws_request(tr_id, '1', self.HTS_USER_ID)

    async def unsubscribe(self, tr_id, stock_code):

        if tr_id in [KIS_WSReq.BID_ASK, KIS_WSReq.CONTRACT]:
            return await self.create_kis_ws_request(tr_id, '2', stock_code)
        elif tr_id == KIS_WSReq.NOTICE:
            return await self.create_kis_ws_request(tr_id, '2', self.HTS_USER_ID)
        
    async def on_open(self):

        #고객체결발생통보 등록
        websocket = self.stk_websocket
        senddata = await self.subscribe(KIS_WSReq.NOTICE, None)
        
        await websocket.send(senddata)
        logger.debug(f"{self.user_id}/{self.acctno}/{self.abbr} 체결통보 등록 senddata: [{senddata}]")
        await asyncio.sleep(0.5)

    # TODO 여기서 오류가 나면 task가 종료되어야함 그것을 어떻게 처리할지 생각해보자
    async def run(self):
        logger.debug(f"{self.user_id}/{self.acctno}/{self.abbr} 증권사 웹소켓 시작")
        try:
            async with websockets.connect(self.url, ping_interval=None) as websocket:
                self.stk_websocket = websocket
                await self.on_open()
                if self.stk_websocket is None:
                    raise Exception("korea_investment_websocket 웹소켓 연결이 안됨")

                while True:
                    received_text = await websocket.recv()  
                    logger.info("웹소켓(KIS로부터 받은데이터) : [" + received_text + "]")
                    if is_real_data(received_text): # 실시간 데이터인 경우
                        aes_iv = self.AES_IV
                        aes_key = self.AES_KEY
                        header, real_model = kis_ws_real_data_parsing(received_text, aes_key, aes_iv)
                        logger.info(f"header: {header}")
                        logger.info(f"real_model: {real_model}")
                        #model_str = real_model.to_str()
                        real_data_dict = real_model.data_for_client_ws()
                        message_str = json.dumps(real_data_dict)
                        await self.broadcast(message_str)
                        await asyncio.sleep(0.5)
                    else: # 실시간 데이터가 아닌 경우
                        try:
                            kis_response = KisWsResponse.from_json_str(received_text)
                            if kis_response.is_pingpong(): # PINGPONG 데이터인 경우
                                await websocket.pong(received_text)  # 웹소켓 클라이언트에서 pong을 보냄
                                logger.debug(f"PINGPONG 데이터 전송: [{received_text}]")
                            elif kis_response.is_error():
                                self.broadcast(kis_response.get_error_message())
                                logger.warning(f"{self.user_id} {self.abbr} Websocket Response 에러발생: {kis_response.get_error_message()}")
                            else: 
                                self.AES_IV = kis_response.get_iv()
                                self.AES_KEY = kis_response.get_key()
                                event_log = kis_response.get_event_log()
                                logger.debug(f"event_log: {event_log}")
                                await self.broadcast(event_log)
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
            logger.debug(f"{self.user_id}/{self.acctno}/{self.abbr} finally 증권사 웹소켓 close")
            self.stk_websocket = None
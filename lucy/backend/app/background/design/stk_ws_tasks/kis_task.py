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
    def __init__(self, user_id:str, client_ws_manager: ClientWsManager):
        self.client_ws_manager = client_ws_manager
        self.user_id = user_id
        self.url = "ws://ops.koreainvestment.com:21000"
        self.abbr = 'KIS'
        self.stk_websocket = None


    async def broadcast(self, message: str):
        logger.debug(message)
        now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = f"{self.user_id}|{self.abbr}|{now_time}|{message}"
        await self.client_ws_manager.send_personal_message(msg, self.user_id)

    # async def run(self):
    #     while True:
    #         # KIS 회사의 WebSocket 통신 로직
    #         await asyncio.sleep(1)
    #         await self.to_client_msg("실시간 WS 동작중...")

    async def create_kis_ws_request(self, tr_id, tr_type, tr_key):
        approval_key = self.user.get_value_by_key("KIS_WS_APPROVAL_KEY")
        if not approval_key:
            KIS_APP_KEY = self.user.get_value_by_key("KIS_APP_KEY")
            KIS_APP_SECRET = self.user.get_value_by_key("KIS_APP_SECRET")

            approval_key = get_ws_approval_key(KIS_APP_KEY, KIS_APP_SECRET)    
            self.user.set_value_by_key("KIS_WS_APPROVAL_KEY", approval_key)
            # db에 저장
            self.user.save()

        # ws_approval_key = self.user.get_value_by_key("KIS_WS_APPROVAL_KEY")
        KIS_APP_SECRET = self.user.get_value_by_key("KIS_APP_SECRET")
        req = new_kis_ws_request()
        req.header.approval_key = approval_key
        req.header.personalseckey = KIS_APP_SECRET
        req.header.tr_type = tr_type
        req.body.input.tr_id = tr_id
        req.body.input.tr_key = tr_key
        senddata = req.model_dump_json()
        
        logger.debug(f"{self.abbr}, {self.user_id} : 증권사에 보낸 데이터[{senddata}]")
        
        return senddata

    async def subscribe(self, tr_id, stock_code):
        user = self.user

        if tr_id in [KIS_WSReq.BID_ASK, KIS_WSReq.CONTRACT]:
            return await self.create_kis_ws_request(tr_id, '1', stock_code)
        elif tr_id == KIS_WSReq.NOTICE:
            KIS_HTS_USER_ID = user.get_value_by_key("KIS_HTS_USER_ID")
            return await self.create_kis_ws_request(tr_id, '1', KIS_HTS_USER_ID)

    async def unsubscribe(self, tr_id, stock_code):
        user = self.user

        if tr_id in [KIS_WSReq.BID_ASK, KIS_WSReq.CONTRACT]:
            return await self.create_kis_ws_request(tr_id, '2', stock_code)
        elif tr_id == KIS_WSReq.NOTICE:
            KIS_HTS_USER_ID = user.get_value_by_key("KIS_HTS_USER_ID")
            return await self.create_kis_ws_request(tr_id, '2', KIS_HTS_USER_ID)
        
    async def on_open(self):

        #고객체결발생통보 등록
        websocket = self.stk_websocket
        senddata = await self.subscribe(KIS_WSReq.NOTICE, None)
        await websocket.send(senddata)
        await asyncio.sleep(0.5)

    async def run(self):
        try:
            user_service = get_user_service()
            user = await user_service.get_1(self.user_id)        
            self.user = user            
            # KIS_APP_KEY = user.get_value_by_key("KIS_APP_KEY")
            # KIS_APP_SECRET = user.get_value_by_key("KIS_APP_SECRET")

            # ws_approval_key = get_ws_approval_key(KIS_APP_KEY, KIS_APP_SECRET)    
            # user.set_value_by_key("KIS_WS_APPROVAL_KEY", ws_approval_key)

            async with websockets.connect(self.url, ping_interval=None) as websocket:
                self.stk_websocket = websocket
                await self.on_open()
                if self.stk_websocket is None:
                    raise Exception("korea_investment_websocket 웹소켓 연결이 안됨")
                # aes_key = None
                # aes_iv = None

                while True:
                    received_text = await websocket.recv()  
                    logger.info("웹소켓(KIS로부터 받은데이터) : [" + received_text + "]")
                    if is_real_data(received_text): # 실시간 데이터인 경우
                        aes_key = user.get_value_by_key("KIS_WS_AES_KEY")
                        aes_iv = user.get_value_by_key("KIS_WS_AES_IV")
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
                                logger.warning(f"Kis Websocket Response 에러발생: {kis_response.get_error_message()}")
                            else: 
                                iv = kis_response.get_iv()
                                key = kis_response.get_key()
                                user.set_value_by_key("KIS_WS_AES_IV", iv)
                                user.set_value_by_key("KIS_WS_AES_KEY", key)
                                event_log = kis_response.get_event_log()
                                logger.debug(f"event_log: {event_log}")
                                await self.broadcast(event_log)
                        except json.JSONDecodeError as e:
                                logger.error(f"JSON decoding error: {e}")
                        except websockets.ConnectionClosed as e:
                                logger.error(f"WebSocket connection closed: {e}")
                                break
                        except Exception as e:
                                logger.error(f"Unexpected error: {e}")
        except websockets.exceptions.ConnectionClosed as e:
            logger.error(f"웹소켓 연결이 닫혔습니다: {e}")
        except Exception as e:
            logger.error(f"웹소켓 연결 중 에러 발생: {e}")
        finally:
            logger.debug(f"finally.....")
            self.stk_websocket = None
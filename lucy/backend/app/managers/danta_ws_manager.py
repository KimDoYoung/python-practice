# danta_ws_manager.py
"""
모듈 설명: 
    - 단타머신에서 연결된 웹소켓데이터를 받아서 처리하는 클래스
주요 기능:
    -   기능을 넣으시오

작성자: 김도영
작성일: 2024-08-07
버전: 1.0
"""
# danta_ws_manager.py
import json
from typing import Dict, List
from fastapi import WebSocket
from backend.app.background.chegeolga_datas import CheGealGaDatas
from backend.app.background.hoga_datas import HogaDatas
from backend.app.core.logger import get_logger
from backend.app.core.dependency import get_log_service, get_mystock_service
from .ws_manager import WsManager
from datetime import datetime

logger = get_logger(__name__)

class DantaWsManager(WsManager):
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DantaWsManager, cls).__new__(cls)
        return cls._instance    

    def __init__(self, event_queue=None):
        if not hasattr(self, 'initialized'):
            self.active_connections: Dict[str, List[WebSocket]] = {}
            self.custom_data: Dict[str, Dict] = {}
            self.event_queue = event_queue
            logger.debug("DantaWsManager 초기화 완료")
            self.initialized = True
            self.hogaDatas = HogaDatas() # 호가데이터 클래스 생성
            self.chegeolDatas = CheGealGaDatas() # 체결가데이터 클래스 생성
            
            self.log = get_log_service()
            self.mystock_service = get_mystock_service()
            self.hoga_count = 0
            self.chegeol_count = 0

    def setEventQueue(self, event_queue):
            self.event_queue = event_queue

    async def connect(self, websocket: WebSocket, user_id: str):
        # await websocket.accept()
        # if user_id not in self.active_connections:
        #     self.active_connections[user_id] = []
        #     logger.debug(f"새 사용자 연결 생성: {user_id}")

        # if websocket not in self.active_connections[user_id]:
        #     self.active_connections[user_id].append(websocket)
        #     msg = f"사용자 {user_id}의 WebSocket 연결 추가: 현재 연결 수 {len(self.active_connections[user_id])}"
        # else:
        #     msg = f"사용자 {user_id}의 WebSocket 연결은 이미 존재함: 현재 연결 수 {len(self.active_connections[user_id])}"

        # if user_id not in self.custom_data:
        #     self.custom_data[user_id] = {"extra_info": "default_value"}
        #     logger.debug(f"사용자 {user_id}의 추가 데이터 생성")
        msg = f"증권사 WebSocket 연결 추가: {user_id}"
        await self.send_to_client(msg, user_id)
        return msg

    def disconnect(self, user_id: str, websocket: WebSocket):
        pass
        # if user_id in self.active_connections:
        #     self.active_connections[user_id].remove(websocket)
        #     logger.debug(f"사용자 {user_id}의 WebSocket 연결 제거: 현재 연결 수 {len(self.active_connections[user_id])}")
        #     if not self.active_connections[user_id]:
        #         del self.active_connections[user_id]
        #         logger.debug(f"사용자 {user_id}의 모든 WebSocket 연결 제거")

        # if user_id in self.custom_data and not self.active_connections.get(user_id):
        #     del self.custom_data[user_id]
        #     logger.debug(f"사용자 {user_id}의 추가 데이터 제거")

    def is_hoga_data(self, message: str):
        ''' 호가데이터인지 판별 '''
        if "H0STASP0" in message:
            if len(message.split("|")) > 3:
                return True
        return False
    def is_chegeol_data(self, message: str):
        ''' 체결가 데이터인지 판별 '''
        if "H0STCNT0" in message and "MKSC_SHRN_ISCD" in message:
            if len(message.split("|")) > 3:
                return True
        return False
    def is_buy_ok_notice(self, message: str):
        ''' 매수알림인지 판별 '''
        if "H0STCNI0" in message and "CNTG_YN" in message:
            if len(message.split("|")) > 3:
                return True
        return False
    
    async def send_to_client(self, message: str, user_id: str):
        logger.debug("---------------------------------------------------------")
        logger.debug(f"단타 웹소켓 데이터 : {message}")
        logger.debug("---------------------------------------------------------")
        if self.is_hoga_data(message):
            self.hogaDatas.append(message)
            self.hoga_count += 1
            if self.hoga_count % 10 == 0:
                today = datetime.now()
                ymd = today.strftime("%Y%m%d")
                self.hogaDatas.save_to_excel(f'c:/tmp/hoga_datas_{ymd}.xlsx')
                
            sell_stk_codes = self.hogaDatas.get_sell_stk_codes()
            if self.event_queue and sell_stk_codes:
                data = {
                    "type" : "SELL_SIGNAL",
                    "data" : {
                        "stk_codes" : sell_stk_codes
                    }
                }
                self.event_queue.put_nowait(data)
                logger.debug("★★★★★★★★★★★★")
                logger.debug(f"이벤트 큐에 데이터 추가 : {data}")
                logger.debug("★★★★★★★★★★★★")
        elif self.is_chegeol_data(message):
            self.chegeolDatas.append(message)
            self.chegeol_count += 1
            if self.chegeol_count % 10 == 0:
                today = datetime.now()
                ymd = today.strftime("%Y%m%d")
                self.chegeolDatas.save_to_excel(f'c:/tmp/chegeol_datas_{ymd}.xlsx')            
                
        elif self.is_buy_ok_notice(message):
            data = message.split("|")[-1]
            h0stcni0 = json.loads(data)
            if h0stcni0.CNTG_YN == '2':
                buy_stk_code = h0stcni0.STK_CODE
                buy_qty = h0stcni0.CNTG_QTY
                buy_price = h0stcni0.CNTG_UNPR
                stk_name = h0stcni0.CNTG_ISNM
                MyStockDto = MyStockDto(stk_code=buy_stk_code, stk_types=['단타'], stk_name=stk_name)
                await self.mystock_service.upsert(MyStockDto)
                await self.log.danta_info(f"{buy_stk_code} {stk_name} {buy_qty}주 {buy_price}원 매수완료")

    async def broadcast(self, message: str):
        logger.debug("---------------------------------------------------------")
        logger.debug(f"단타 웹소켓 데이터 : {message}")
        logger.debug("---------------------------------------------------------")
        
    def reset(self):
        logger.debug("모든 WebSocket 연결 초기화 시작")
        self.active_connections.clear()
        self.custom_data.clear()
        logger.debug("모든 WebSocket 연결 초기화 완료")

    def reset_user(self, user_id: str):
        if user_id in self.active_connections:
            logger.debug(f"사용자 {user_id}의 모든 WebSocket 연결 초기화 시작")
            del self.active_connections[user_id]
            logger.debug(f"사용자 {user_id}의 모든 WebSocket 연결 초기화 완료")
        if user_id in self.custom_data:
            del self.custom_data[user_id]
            logger.debug(f"사용자 {user_id}의 추가 데이터 제거 완료")

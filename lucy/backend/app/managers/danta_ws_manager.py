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
from typing import Dict, List
from fastapi import WebSocket
from backend.app.core.logger import get_logger
from .ws_manager import WsManager

logger = get_logger(__name__)

class DantaWsManager(WsManager):
    _instance = None

    # def __new__(cls, *args, **kwargs):
    #     if cls._instance is None:
    #         cls._instance = super(DantaWsManager, cls).__new__(cls, *args, **kwargs)
    #     return cls._instance
    
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

    async def send_to_client(self, message: str, user_id: str):
        logger.debug("---------------------------------------------------------")
        logger.debug(f"단타 웹소켓 데이터 : {message}")
        logger.debug("---------------------------------------------------------")
        if self.event_queue:
            data = {
                "type" : "SELL_SIGNAL",
                "data" : {
                    "stk_code" : "005930",
                    "stk_name" : "삼성전자",
                    "cost" : 100000,
                }
            }
            self.event_queue.put_nowait(data)
            logger.debug("★★★★★★★★★★★★")
            logger.debug(f"이벤트 큐에 데이터 추가 : {data}")
            logger.debug("★★★★★★★★★★★★")
        # if user_id in self.active_connections:
        #     for websocket in self.active_connections[user_id][:]:
        #         try:
        #             await websocket.send_text(message)
        #             logger.debug(f"사용자 {user_id}에게 메시지 전송 성공: {message}")
        #         except Exception as e:
        #             self.disconnect(user_id, websocket)
        #             logger.debug(f"사용자 {user_id}에게 메시지 전송 실패, 연결 제거: {e}")

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

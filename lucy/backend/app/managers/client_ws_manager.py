# client_ws_manager.py
"""
모듈 설명: 
    - user_id별로 WebSocket 연결을 관리하는 클래스
주요 기능:
    - 

작성자: 김도영
작성일: 05
버전: 1.0
"""
from typing import Dict, List
from fastapi import WebSocket
from backend.app.core.logger import get_logger
from .ws_manager import WsManager

logger = get_logger(__name__)

class ClientWsManager(WsManager):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ClientWsManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.active_connections: Dict[str, List[WebSocket]] = {}
            logger.debug("ClientWsManager 초기화 완료")
            self.initialized = True

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
            logger.debug(f"새 사용자 연결 생성: {user_id}")
        
        if websocket not in self.active_connections[user_id]:
            self.active_connections[user_id].append(websocket)
            msg = f"사용자 {user_id}의 WebSocket 연결 추가: 현재 연결 수 {len(self.active_connections[user_id])}"
        else:
            msg = f"사용자 {user_id}의 WebSocket 연결은 이미 존재함: 현재 연결 수 {len(self.active_connections[user_id])}"
        
        await self.send_to_client(msg, user_id)
        return msg

    def disconnect(self, user_id: str, websocket: WebSocket):
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            logger.debug(f"사용자 {user_id}의 WebSocket 연결 제거: 현재 연결 수 {len(self.active_connections[user_id])}")
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
                logger.debug(f"사용자 {user_id}의 모든 WebSocket 연결 제거")

    async def send_to_client(self, message: str, user_id: str):
        if user_id in self.active_connections:
            for websocket in self.active_connections[user_id][:]:
                try:
                    await websocket.send_text(message)
                    logger.debug(f"사용자 {user_id}에게 메시지 전송 성공: {message}")
                except Exception as e:
                    self.disconnect(user_id, websocket)
                    logger.debug(f"사용자 {user_id}에게 메시지 전송 실패, 연결 제거: {e}")

    async def broadcast(self, message: str):
        for user_id, connections in self.active_connections.items():
            for websocket in connections[:]:
                try:
                    await websocket.send_text(message)
                    logger.debug(f"브로드캐스트 메시지 전송 성공: {message}")
                except Exception as e:
                    self.disconnect(user_id, websocket)
                    logger.debug(f"브로드캐스트 메시지 전송 실패, 연결 제거: {e}")

    def reset(self):
        logger.debug("모든 WebSocket 연결 초기화 시작")
        self.active_connections.clear()
        logger.debug("모든 WebSocket 연결 초기화 완료")

    def reset_user(self, user_id: str):
        if user_id in self.active_connections:
            logger.debug(f"사용자 {user_id}의 모든 WebSocket 연결 초기화 시작")
            del self.active_connections[user_id]
            logger.debug(f"사용자 {user_id}의 모든 WebSocket 연결 초기화 완료")




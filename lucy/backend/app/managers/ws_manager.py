# ws_manager.py
from abc import ABC, abstractmethod
from typing import Dict, List
from fastapi import WebSocket

class WsManager(ABC):
    @abstractmethod
    async def connect(self, websocket: WebSocket, user_id: str):
        pass

    @abstractmethod
    def disconnect(self, user_id: str, websocket: WebSocket):
        pass

    @abstractmethod
    async def send_to_client(self, message: str, user_id: str):
        pass

    @abstractmethod
    async def broadcast(self, message: str):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def reset_user(self, user_id: str):
        pass

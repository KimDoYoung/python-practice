from typing import Dict
import asyncio
from backend.app.background.design.stk_ws_tasks.kis_task import KISTask
from backend.app.background.design.stk_ws_tasks.kb_task import KBTask
from backend.app.core.logger import get_logger
logger = get_logger(__name__)

class StockWsManager:
    def __init__(self):
        self.stock_connections: Dict[str, Dict[str, asyncio.Task]] = {}
        logger.debug("StockWsManager 초기화 완료")

    async def connect(self, user_id: str, stk_company_abbr: str):
        if user_id not in self.stock_connections:
            self.stock_connections[user_id] = {}
            logger.debug(f"새 사용자 연결 생성: {user_id}")
        if stk_company_abbr not in self.stock_connections[user_id]:
            task = asyncio.create_task(self.stock_ws_task(user_id, stk_company_abbr))
            self.stock_connections[user_id][stk_company_abbr] = task
            logger.debug(f"{stk_company_abbr} 회사에 대한 WebSocket 작업 시작: {user_id}")

    async def disconnect(self, user_id: str, stk_company_abbr: str):
        if user_id in self.stock_connections and stk_company_abbr in self.stock_connections[user_id]:
            task = self.stock_connections[user_id][stk_company_abbr]
            task.cancel()
            del self.stock_connections[user_id][stk_company_abbr]
            logger.debug(f"{stk_company_abbr} 회사에 대한 WebSocket 작업 종료: {user_id}")
            if not self.stock_connections[user_id]:
                del self.stock_connections[user_id]
                logger.debug(f"사용자 {user_id}의 모든 WebSocket 작업 종료")

    async def stock_ws_task(self, user_id: str, stk_company_abbr: str):
        logger.debug(f"WebSocket 작업 시작: {user_id} -> {stk_company_abbr}")
        if stk_company_abbr == "kis":
            kis_task = KISTask()
            await kis_task.run(user_id)
            logger.debug(f"KIS 작업 완료: {user_id}")
        elif stk_company_abbr == "kb":
            kb_task = KBTask()
            await kb_task.run(user_id)
            logger.debug(f"KB 작업 완료: {user_id}")
        else:
            logger.debug(f"알 수 없는 회사: {stk_company_abbr}")

    def is_connected(self, user_id: str, stk_company_abbr: str) -> bool:
        connected = user_id in self.stock_connections and stk_company_abbr in self.stock_connections[user_id]
        logger.debug(f"연결 상태 확인: {user_id} -> {stk_company_abbr}: {connected}")
        return connected

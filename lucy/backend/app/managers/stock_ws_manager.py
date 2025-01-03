# stock_ws_manager.py
"""
모듈 설명: 
    - 사용자별로 증권사 WebSocket 연결을 관리하는 클래스
주요 기능:
    - 사용자별로 증권사 WebSocket 연결을 생성 및 제거

작성자: 김도영
작성일: 05
버전: 1.0
"""
from typing import Dict
import asyncio
from backend.app.managers.client_ws_manager import ClientWsManager
from backend.app.domains.stc.kis.kis_ws_task import KISTask
from backend.app.domains.stc.ls.ls_ws_task import LSTask
from backend.app.core.logger import get_logger
from backend.app.core.dependency import get_user_service

logger = get_logger(__name__)

class StockWsManager:
    _instance = None

    def __new__(cls, client_ws_manager: ClientWsManager, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(StockWsManager, cls).__new__(cls, *args, **kwargs)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self, client_ws_manager: ClientWsManager):
        if self.__initialized:
            return
        self.client_ws_manager = client_ws_manager    
        self.user_service = get_user_service()
        self.stock_connections: Dict[str, Dict[str, asyncio.Task]] = {}
        logger.debug("StockWsManager 초기화 완료")
        self.__initialized = True

    async def validate_account(self, user_id: str, acctno: str):
        ERROR_USER_NOT_FOUND = {"code": "02", "detail": f"사용자 {user_id}를 찾을 수 없습니다."}
        ERROR_ACCOUNT_NOT_FOUND = {"code": "03", "detail": f"계좌 {acctno}를 찾을 수 없습니다."}
        ERROR_UNKNOWN_ACCOUNT = {"code": "04", "detail": f"알 수 없는 계좌: {acctno}, not KIS or LS"}
        
        user = await self.user_service.get_1(user_id)
        if user is None:
            return ERROR_USER_NOT_FOUND
        
        account = user.find_account(acctno)
        if account is None:
            return ERROR_ACCOUNT_NOT_FOUND
        
        abbr = account.abbr.upper()
        if abbr not in {'KIS', 'LS'}:
            return ERROR_UNKNOWN_ACCOUNT

        return {"code": "00", "account": account}
    
    async def connect(self, user_id: str, acctno: str):

        validation_result = await self.validate_account(user_id, acctno)
        if validation_result["code"] != "00":
            return validation_result
        
        account = validation_result["account"]
        abbr = account.abbr.upper()

        if user_id not in self.stock_connections:
            self.stock_connections[user_id] = {}
            logger.debug(f"새 사용자 연결 생성: {user_id}")

        if acctno not in self.stock_connections[user_id]:
            try:
                # task = asyncio.create_task(self.stock_ws_task(user_id, acctno, abbr))
                task = await self.stock_ws_task(user_id, acctno, abbr)
                self.stock_connections[user_id][acctno] = task
                await task.run()
                logger.debug(f"{acctno} 계좌에 대한 WebSocket 작업 생성: {user_id}")
            except Exception as e:
                logger.error(f"에러 발생: {e}")
                if acctno in self.stock_connections.get(user_id, {}):
                    del self.stock_connections[user_id][acctno]
                    if not self.stock_connections[user_id]:
                        del self.stock_connections[user_id]                
                return {"code": "06", "detail": f"{acctno} 계좌에 대한 WebSocket 작업 실패: {user_id}"}
        
        logger.debug(f"{acctno} 계좌에 대한 WebSocket 작업 시작: {user_id}")
        return {"code" : "00", "detail": f"{acctno} 계좌에 대한 WebSocket 작업 시작: {user_id}"}

    async def disconnect(self, user_id: str, acctno: str):
        
        validation_result = await self.validate_account(user_id, acctno)
        if validation_result["code"] != "00":
            return validation_result
        
        if user_id in self.stock_connections and acctno in self.stock_connections[user_id]:
            task = self.stock_connections[user_id][acctno]
            task.cancel()
            del self.stock_connections[user_id][acctno]
            logger.debug(f"{acctno} 계좌에 대한 WebSocket 작업 종료: {user_id}")
            if not self.stock_connections[user_id]:
                del self.stock_connections[user_id]
            
            await self.client_ws_manager.send_to_client(f"사용자 {user_id}의 모든 증권 계좌 WebSocket 작업 종료", user_id)
            return {"code": "00", "detail": f"{user_id}/{acctno} 계좌에 대한 WebSocket 작업 종료"}
        else:
            return {"code": "05", "detail": f"{user_id}/{acctno} 계좌에 대한 WebSocket 작업이 이미 종료되었습니다."}

    async def stock_ws_task(self, user_id: str, acctno: str, abbr: str):
        logger.debug(f"WebSocket 작업 시작: {user_id}/{acctno}/{abbr}")

        if abbr == "KIS":
            kis_task = KISTask(user_id, acctno, self.client_ws_manager)
            result = await kis_task.initialize()
            if result["code"] != "00":
                raise Exception(result["detail"])
            try:
                #await kis_task.run()
                logger.debug(f"KIS 작업 완료: {user_id}/{acctno}/{abbr} ")
                return kis_task
            except Exception as e:
                logger.error(f"KIS WebSocket 작업 중 에러 발생: {e}")
                raise Exception(f"KIS WebSocket 작업 중 에러 발생: {e}")
            
        elif abbr == "LS":
            ls_task = LSTask(user_id, acctno, self.client_ws_manager)
            await ls_task.initialize()
            #await ls_task.run()
            logger.debug(f"LS 작업 완료: {user_id}")
            return ls_task
        else:
            logger.error(f"알 수 없는 증권사: {abbr}")        

    def is_connected(self, user_id: str, acctno: str) -> bool:
        connected = user_id in self.stock_connections and acctno in self.stock_connections[user_id]
        logger.debug(f"연결 상태 확인: {user_id} -> {acctno}: {connected}")
        return connected

    def status(self):
        status_info = {}
        for user_id, connections in self.stock_connections.items():
            user_status = {}
            for acctno, task in connections.items():
                user_status[acctno] = str(task.get_coro().__name__)
            status_info[user_id] = user_status
        logger.debug(f"현재 연결 상태: {status_info}")
        return status_info

    async def get_task(self, user_id: str, acctno: str):
        ''' user_id의 acctno에 대한 WebSocket Task를 반환한다 '''
        # user_id가 존재하는지 확인하고 없으면 초기화
        if user_id not in self.stock_connections:
            logger.error(f"ws_manager : 사용자 {user_id}를 찾을 수 없음")
            return None
        
        # 계좌 번호가 존재하지 않으면 기본값 추가
        if acctno not in self.stock_connections[user_id]:
            logger.error(f"ws_manager : 계좌 {acctno}를 찾을 수 없음")
            return None

        task =  self.stock_connections[user_id][acctno]
        if task is None:
            logger.error(f"ws_manager : {user_id}/{acctno}에 대한 Task를 찾을 수 없음")
            return None
        logger.info(f"ws_manager : {user_id}/{acctno}에 대한 Task 반환")
        return task

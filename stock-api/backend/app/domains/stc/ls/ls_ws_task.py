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
from backend.app.managers.client_ws_manager import ClientWsManager
from dependency import get_user_service
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

    async def initialize(self):
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


    async def run(self, user_id: str):
        while True:
            # LS 회사의 WebSocket 통신 로직
            await asyncio.sleep(1)
            print(f"KB WebSocket task for user {user_id}")

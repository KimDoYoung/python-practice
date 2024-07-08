# stock_api_manager.py
"""
모듈 설명: 
    - KisStockApi, LsStockApi를 관리하는 Manager
주요 기능:
    - 각 증권사들의 주식 API를 통합적으로 관리하는 Manager
    - cache기능을 갖는다.
    - 싱글레톤드로 구현
    - kis_api = StockApiManager(user_service).stock_api(user_id, acctno,'KIS') 로 사용

작성자: 김도영
작성일: 04
버전: 1.0
"""
from backend.app.domains.stc.kis.kis_stock_api import KisStockApi
from backend.app.domains.stc.ls.ls_stock_api import LsStockApi
class StockApiManager:
    _instance = None
    _cache = {}
    _user_service = None

    def __new__(cls, user_service=None):
        if cls._instance is None:
            cls._instance = super(StockApiManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, user_service=None):
        if not self._initialized:
            self._user_service = user_service
            self._initialized = True

    async def stock_api(self, user_id, acctno, stk_abbr):
        # cache에 있으면 cache에서 반환
        key = (user_id, acctno, stk_abbr)
        if key in self._cache:
            stock_api =  self._cache[key]
            # TODO cache에 있는것이 만약 ACCESS_KEY가 만료되었으면 다시 초기화
            return stock_api

        user = await self._user_service.get_1(user_id)
        if user is None:
            raise ValueError(f"User not found: {user_id}")
        
        account = user.find_account(acctno)
        if account is None:
            raise ValueError(f"Account not found: {acctno}")
        
        if stk_abbr == 'KIS':
            api = KisStockApi(user, account)
        elif stk_abbr == 'LS':
            api = LsStockApi(user, account)
        else:
            raise ValueError(f"Unsupported stock company: {stk_abbr}")

        api.set_user_service(self._user_service)
        
        b = await api.initialize()
        if not b:
            raise ValueError(f"Stock API initialization failed: {acctno}")

        self._cache[key] = api
        return api

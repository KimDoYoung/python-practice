# stock_api_manager.py
"""
모듈 설명: 
    - KisStockApi, LsStockApi를 관리하는 Manager
    - 원래 여러명의 사용자, 여러개의 계좌용으로 작성되었지만, 여기서는 단일사용자, 단일계좌만을 지원한다.
주요 기능:
    - 각 증권사들의 주식 API를 통합적으로 관리하는 Manager
    - cache기능을 갖는다.
    - 싱글레톤드로 구현
    - kis_api = StockApiManager(user_service).stock_api(user_id, acctno,'KIS') 로 사용

작성자: 김도영
작성일: 04
버전: 1.0
"""
from datetime import datetime, timedelta
from backend.app.domains.stc.kis.kis_stock_api import KisStockApi
from backend.app.domains.stc.ls.ls_stock_api import LsStockApi
from backend.app.core.dependency import get_user_service
from backend.app.core.config import config

class StockApiManager:
    _instance = None
    _cache = {}
    _user_service = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StockApiManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._user_service = get_user_service() # user_service
            self._initialized = True

    async def stock_api(self, stk_abbr):
        ''' 1인 1계좌만 지원 '''
        # cache에 있으면 cache에서 반환
        key = (stk_abbr)
        if key in self._cache:
            stock_api =  self._cache[key]
            access_token_time = stock_api.get_access_token_time()
            if access_token_time is not None:
                if (datetime.now() - access_token_time) > timedelta(hours=12):
                    await stock_api.initialize()
            else:
                await stock_api.initialize()
                        
            return stock_api
        # 기본사용자ID
        user_id = config.DEFAULT_USER_ID
        user = await self._user_service.get_1(user_id)
        if user is None:
            raise ValueError(f"User not found: {user_id}")

        account = user.find_account_by_abbr(stk_abbr)
        if stk_abbr == 'KIS':
            api = KisStockApi(user, account)
        elif stk_abbr == 'LS':
            api = LsStockApi(user, account)
        else:
            raise ValueError(f"지원하지 않는 증권사입니다: {stk_abbr}")

        api.set_user_service(self._user_service)
        
        b = await api.initialize()
        if not b:
            raise ValueError(f"Stock API 생성에 실패했습니다: {stk_abbr}:{account.account_no}")

        self._cache[key] = api
        return api
    
    async def kis_api(self):
        return await self.stock_api('KIS')
    
    async def ls_api(self):
        return await self.stock_api('LS')
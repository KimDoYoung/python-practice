from backend.app.domains.stc.kis.kis_stock_api import KisStockApi
from backend.app.domains.stc.ls.ls_stock_api import LsStockApi


class StockApiManager:
    _instance = None
    _cache = {}
    _user_service = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StockApiManager, cls).__new__(cls)
        return cls._instance

    def set_user_service(self, user_service):
        self._user_service = user_service

    async def stock_api(self, user_id, acctno, stk_abbr):

        #cache에 있으면 cache에서 반환
        key = (user_id, acctno, stk_abbr)
        if key in self._cache:
            return self._cache[key]

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
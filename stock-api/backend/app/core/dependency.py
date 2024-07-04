from functools import lru_cache


from backend.app.core.mongodb import MongoDb
from backend.app.core.config import config
from backend.app.domains.user.user_service import UserService


@lru_cache()
def get_user_service():
    db_name = config.DB_NAME
    return UserService(MongoDb.get_client()[db_name])

# 각 증권사들의  주식 API를 통합적으로 관리하는 Manager
# @lru_cache()
# def get_api_manager(user_service: UserService = Depends(get_user_service)):
#     from backend.app.managers.stock_api_manager import StockApiManager
#     api_manager = StockApiManager()
#     api_manager.set_user_service(user_service)
#     return api_manager

# client 즉 AssetErp와 통신하는 WebSocketManager
# @lru_cache()
# def get_client_ws_manager() -> ClientWsManager:
#     return ClientWsManager()

# # KIS,LS 등 증권사의 체결통보(실시간)를 받기위한 WebSocketManager
# @lru_cache()
# def get_stock_ws_manager(client_ws_manager: ClientWsManager = Depends(get_client_ws_manager)) -> StockWsManager:
#     return StockWsManager(client_ws_manager)

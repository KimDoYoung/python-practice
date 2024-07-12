from backend.app.managers.client_ws_manager import ClientWsManager
from backend.app.core.dependency import get_user_service
from backend.app.core.logger import get_logger

logger = get_logger(__name__)

class StockTask:
    def __init__(self, user_id: str, acctno: str, client_ws_manager: ClientWsManager, url: str, abbr: str):
        self.client_ws_manager = client_ws_manager
        self.user_id = user_id
        self.url = url
        self.abbr = abbr
        self.user_service = get_user_service()
        self.stk_websocket = None
        self.user = None
        self.acctno = acctno
        self.account = None
        logger.debug(f"{self.user_id}/{self.acctno}/{self.abbr} 증권사 웹소켓 생성")

    async def initialize(self):
        pass
from backend.app.core.logger import get_logger
from backend.app.domains.system.stk_info_model import StkInfo

logger = get_logger(__name__)

class StockInfoService:
    
    async def create(self, data: dict):
        stk_info = StkInfo(**data)
        await stk_info.create()
        return stk_info

    async def get_all(self):
        try:
            stk_infos = await StkInfo.find().to_list()
            return stk_infos
        except Exception as e:
            logger.error(f"Failed to retrieve all StkInfos: {e}")
            raise e
    
    async def delete_all(self):
        await StkInfo.delete_all()
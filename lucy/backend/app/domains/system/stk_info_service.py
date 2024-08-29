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
        
    async def get_by_stk_code(self, stk_code: str):
        try:
            stk_info = await StkInfo.find_one({"stk_code": stk_code})
            return stk_info
        except Exception as e:
            logger.error(f"Failed to retrieve StkInfo by stk_code: {e}")
            raise e
    
    async def list_by_name(self, stk_name: str):
        try:
            filter_query = {"stk_name": {"$regex": stk_name}}
            stk_infos = await StkInfo.find(filter_query).to_list()
            return stk_infos
        except Exception as e:
            logger.error(f"Failed to retrieve StkInfo by stk_name: {e}")
            raise e
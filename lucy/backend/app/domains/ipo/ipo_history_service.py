
from beanie import PydanticObjectId
from backend.app.core.logger import get_logger
from backend.app.domains.ipo.ipo_history_model import IpoHistory

logger = get_logger(__name__)

class IpoHistoryService:
    
    async def create(self, keyvalue: dict):
        history = IpoHistory(**keyvalue)
        await history.save()
        return history
    
    async def get_all(self):
        return await IpoHistory.all().to_list()
    
    async def get_1(self, ipo_id: str):
        object_id = PydanticObjectId(ipo_id)
        ipo = await IpoHistory.find_one(IpoHistory.id == object_id)
        return ipo

    async def delete_1(self, ipo_id: str):
        object_id = PydanticObjectId(ipo_id)
        ipo = await IpoHistory.find_one(IpoHistory.id == object_id)
        if ipo:
            deleted_ipo = await ipo.delete()
            return deleted_ipo
        else:
            return None
    
    async def update_1(self, ipo_history: IpoHistory):
        await ipo_history.save()
        return ipo_history
    
    #TODO : 체결예상가를 만드는 수식을 만들어서 저장해야한다.

from backend.app.core.logger import get_logger
from backend.app.domains.ipo.ipo_history_model import IpoHistory

logger = get_logger(__name__)

class IpoHistoryService:
    
    async def create(self, keyvalue: dict):
        ipo = IpoHistory(**keyvalue)
        await ipo.save()
        return ipo
    
    async def get_all(self):
        return await IpoHistory.all().to_list()

    async def delete_1(self, ipo_id: str):
        ipo = await IpoHistory.find_one(IpoHistory.ipo_id == ipo_id)
        if ipo:
            deleted_ipo = await ipo.delete()
            return deleted_ipo
        else:
            return None
    
    async def update_1(self, ipo_history: IpoHistory):
        await ipo_history.save()
        return ipo_history
    
    #TODO : 체결예상가를 만드는 수식을 만들어서 저장해야한다.
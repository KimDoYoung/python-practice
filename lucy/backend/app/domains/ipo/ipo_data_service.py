

from backend.app.core.logger import get_logger
from backend.app.domains.ipo.ipo_data_model import IpoData

logger = get_logger(__name__)


class IpoDataService:
    
    async def create(self, keyvalue: dict):
        ipo = IpoData(**keyvalue)
        await ipo.save()
        return ipo
    
    #TODO CRUD 와 수식 계산 로직을 만들어야 한다.
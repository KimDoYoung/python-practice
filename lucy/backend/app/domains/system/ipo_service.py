from typing import Any, Dict, List, Optional
from beanie import PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from backend.app.domains.system.config_model import DbConfig
import logging

from backend.app.domains.system.eventdays_model import EventDays
from backend.app.domains.system.ipo_model import Ipo

logger = logging.getLogger(__name__)

class IpoService:
    # _instance = None
    def __init__(self, db_client: AsyncIOMotorClient):
        self.db_client = db_client

    async def create(self, keyvalue: dict):
        ipo = Ipo(**keyvalue)
        await ipo.create()
        return ipo

    async def get_all(self) -> List[Ipo]:
        try:
            ipos = await Ipo.find_all().to_list()
            return ipos
        except Exception as e:
            logger.error(f"Failed to retrieve all Ipos: {e}")
            raise e
    
    async def update_by_id(self, id: PydanticObjectId, data: Dict[str, Any]) -> Optional[Ipo]:
        ipo = await Ipo.get(id)
        if ipo:
            await ipo.set(data)
            await ipo.save()
            return ipo
        else:
            logger.error(f"Ipo with id {id} not found")
            return None

    async def update_by_stk_name(self, stk_name: str, data: Dict[str, Any]) -> Optional[Ipo]:
        ipo = await Ipo.find_one(Ipo.stk_name == stk_name)
        if ipo:
            return await self.update_by_id(id=ipo.id, data=data)
        else:
            logger.error(f"Ipo with stk_name {stk_name} not found")
            return None

    async def delete(self, id: PydanticObjectId) -> Ipo:
        ipo = await Ipo.get(id)
        if ipo:
            ipo = await ipo.delete()
            return ipo


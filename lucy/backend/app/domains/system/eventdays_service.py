from typing import Any, Dict, List, Optional
from beanie import PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from backend.app.domains.system.config_model import DbConfig
import logging

from backend.app.domains.system.eventdays_model import EventDays

logger = logging.getLogger(__name__)

class EventDaysService:
    # _instance = None
    def __init__(self, db_client: AsyncIOMotorClient):
        self.db_client = db_client

    async def create(self, keyvalue: dict):
        eventday = EventDays(**keyvalue)
        await eventday.create()
        return eventday

    async def get_all(self, yyyymm:str) -> List[EventDays]:
        try:
            if yyyymm == 'all':
                eventdays = await EventDays.find().to_list()
            else:
                eventdays = await EventDays.find({"locdate": {"$regex": f'^{yyyymm}'}}).to_list()
            return eventdays            
 #           return eventdays            
            return eventdays
        except Exception as e:
            logger.error(f"Failed to retrieve all EventDays: {e}")
            raise e
    
    async def update(self, event_id: PydanticObjectId, update_eventday: Dict[str, Any]) -> Optional[EventDays]:
        eventday = await EventDays.get(event_id)
        if eventday:
            await eventday.set(update_eventday)
            await eventday.save()
            return eventday
        else:
            logger.error(f"EventDay with id {event_id} not found")
            return None

    async def delete(self, event_id: PydanticObjectId) -> EventDays:
        eventday = await EventDays.get(event_id)
        if eventday:
            eventday = await eventday.delete()
            return eventday


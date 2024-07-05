from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from backend.app.core.logger import get_logger
from backend.app.domains.logs.logs_model import Logs


logger = get_logger(__name__)

class LogsService:
    # _instance = None
    def __init__(self, db_client: AsyncIOMotorClient):
        self.db_client = db_client

    async def create(self, keyvalue: dict):
        setting = Logs(**keyvalue)
        await setting.create()
        return setting

    async def get_all(self) -> List[Logs]:
        try:
            Logs = await Logs.find_all().to_list()
            return Logs
        except Exception as e:
            logger.error(f"Failed to retrieve all dbconfigs: {e}")
            raise e

    async def count(self) -> int:
        result = await Logs.count()
        return result

from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from backend.app.domains.system.config_model import DbConfig
import logging

logger = logging.getLogger(__name__)

class DbConfigService:
    # _instance = None
    def __init__(self, db_client: AsyncIOMotorClient):
        self.db_client = db_client

    async def create_dbconfig(self, keyvalue: dict):
        dbconfig = DbConfig(**keyvalue)
        await dbconfig.create()
        return dbconfig

    async def get_all_users(self) -> List[DbConfig]:
        try:
            dbconfigs = await DbConfig.find_all().to_list()
            return dbconfigs
        except Exception as e:
            logger.error(f"Failed to retrieve all dbconfigs: {e}")
            raise e
    
    async def get_dbconfig(self,key: str) -> DbConfig:
        dbconfig = await DbConfig.find_one(DbConfig.key == key)
        return dbconfig

    async def update_user(self, update_data:dict) -> DbConfig:
        user = await DbConfig.find_one(DbConfig.key == update_data.key)
        if user:
            await user.set(update_data)
            await user.save()
            return user
        else:
            return None

    async def delete_user(self, key: str) -> DbConfig:
        dbconfig = await DbConfig.find_one(DbConfig.key == key)
        if dbconfig:
            dbconfig = await dbconfig.delete()
            return dbconfig

    async def count(self) -> int:
        result = await DbConfig.count()
        return result

from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from backend.app.domains.system.config_model import DbConfig
from backend.app.core.logger import get_logger

logger = get_logger(__name__)

class DbConfigService:
    # _instance = None
    def __init__(self, db_client: AsyncIOMotorClient):
        self.db_client = db_client

    async def create(self, keyvalue: dict):
        dbconfig = DbConfig(**keyvalue)
        await dbconfig.create()
        return dbconfig

    async def get_all(self) -> List[DbConfig]:
        try:
            dbconfigs = await DbConfig.find_all().to_list()
            return dbconfigs
        except Exception as e:
            logger.error(f"Failed to retrieve all dbconfigs: {e}")
            raise e
    
    async def get_1(self,key: str) -> DbConfig:
        dbconfig = await DbConfig.find_one(DbConfig.key == key)
        return dbconfig

    async def update_1(self, key:str, update_data:dict) -> DbConfig:
        user = await DbConfig.find_one(DbConfig.key == key)
        if user:
            await user.set(update_data)
            await user.save()
            return user
        else:
            return None

    async def delete_1(self, key: str) -> DbConfig:
        dbconfig = await DbConfig.find_one(DbConfig.key == key)
        if dbconfig:
            await dbconfig.delete()
            return dbconfig
        return None

    async def count(self) -> int:
        result = await DbConfig.count()
        return result

    async def get_process_status(self, process_id: str) -> DbConfig:
        ''' 백그라운드 상태를 가져온다. running or stopped '''
        dbconfig = await self.get_dbconfig(process_id)
        if dbconfig:
            return dbconfig
        else:
            return None

    async def set_process_status(self, data: dict):
        ''' 백그라운드 상태를 설정한다. running or stopped '''
        data['mode'] = 'System'
        dbconfig = await self.get_dbconfig(data.key)
        if dbconfig:
            await dbconfig.set(data)
            await dbconfig.save()
            return dbconfig
        else:
            self.create_dbconfig(data)
    
    async def remove_process_status(self, key: str) -> None:
        ''' 백그라운드 상태를 삭제한다. '''
        dbconfig = await self.get_dbconfig(key)
        if dbconfig:
            await dbconfig.delete()
            return None
        else:
            return None
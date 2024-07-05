from typing import List
from backend.app.core.logger import get_logger
from backend.app.domains.settings.settings_model import Settings


logger = get_logger(__name__)

class SettingsService:

    async def create(self, keyvalue: dict):
        setting = Settings(**keyvalue)
        await setting.create()
        return setting

    async def get_all(self) -> List[Settings]:
        try:
            settings = await Settings.find_all().to_list()
            return settings
        except Exception as e:
            logger.error(f"Failed to retrieve all dbconfigs: {e}")
            raise e
    
    async def get_1(self,key: str) -> Settings:
        setting = await Settings.find_one(Settings.key == key)
        return setting

    async def update_1(self, key:str, update_data:dict) -> Settings:
        setting = await Settings.find_one(Settings.key == key)
        if setting:
            await setting.set(update_data)
            await setting.save()
            return setting
        else:
            return None

    async def delete_1(self, key: str) -> Settings:
        dbconfig = await Settings.find_one(Settings.key == key)
        if dbconfig:
            await dbconfig.delete()
            return dbconfig
        return None

    async def count(self) -> int:
        result = await Settings.count()
        return result

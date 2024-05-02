from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.domain.users.user_model import User
import logging

logger = logging.getLogger(__name__)

class UserService:
    # _instance = None
    def __init__(self, db_client: AsyncIOMotorClient):
        self.db_client = db_client

    # @classmethod
    # async def create_instance(cls, db_client: AsyncIOMotorClient):
    #     if cls._instance is None:
    #         cls._instance = cls(db_client=db_client)
    #         await cls._instance.init_beanie()
    #     return cls._instance
    
    # async def init_beanie(self):
    #     await init_beanie(database=self.db_client.stockdb, document_models=[User]) 

    async def create_user(self, user_data: dict):
        user = User(**user_data)
        await user.create()
        return user

    async def get_all_users(self) -> List[User]:
        try:
            users = await User.find_all().to_list()
            return users
        except Exception as e:
            logger.error(f"Failed to retrieve all users: {e}")
            raise e
    
    async def get_user(self, user_id: str) -> User:
        user = await User.find_one(User.user_id == user_id)
        return user

    async def update_user(self, user_id: str, update_data: dict) -> User:
        user = await User.find_one(User.user_id == user_id)
        if user:
            await user.set(update_data)
            await user.save()
            return user
        else:
            return None

    async def delete_user(self, user_id: str) -> User:
        user = await User.find_one(User.user_id == user_id)
        if user:
            deleted_user = await user.delete()
            return deleted_user  

    async def count(self) -> int:
        result = await User.count()
        return result

# DB 클라이언트 설정
#db_client = AsyncIOMotorClient("mongodb://localhost:27017")
#user_service = UserService(db_client=db_client)

from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from backend.app.domains.user.user_model import User
from backend.app.core.logger import get_logger

logger = get_logger(__name__)

class UserService:
    # _instance = None
    def __init__(self, db_client: AsyncIOMotorClient):
        self.db_client = db_client

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

    async def authenticate_user(self, user_id, password) -> User:
        user = await self.get_user(user_id)
        if user:
            if user.password == password:
                return user
        else:
            return None    
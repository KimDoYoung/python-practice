from typing import List
from fastapi import HTTPException
from pydantic import ValidationError
from backend.app.domains.user.user_model import User
from backend.app.core.logger import get_logger

logger = get_logger(__name__)

class UserService:
    # _instance = None
    # def __init__(self, db_client: AsyncIOMotorClient):
    #     self.db_client = db_client

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
    
    async def get_1(self, user_id: str) -> User:
        user = await User.find_one(User.user_id == user_id)
        if user is None:
            raise ValueError(f"User {user_id} not found")
        return user

    async def update_user(self, user_id: str, update_data: dict) -> User:
        user = await self.get_1(user_id)
        if user:
            try:
                updated_data = user.model_dump()
                updated_data.update(update_data)
                updated_user = User(**updated_data)  # 유효성 검사를 위해 새 인스턴스 생성                
                await updated_user.save()
                return updated_user
            except ValidationError as e:
                logger.error(f"Validation error: {e}")
                raise HTTPException(status_code=400, detail=str(e))
        else:
            raise ValueError("User not found")

    async def delete_user(self, user_id: str) -> User:
        user = await User.find_one(User.user_id == user_id)
        if user:
            deleted_user = await user.delete()
            return deleted_user  

    async def count(self) -> int:
        result = await User.count()
        return result

    async def authenticate_user(self, user_id, password) -> User:
        user = await self.get_1(user_id)
        if user:
            if user.password == password:
                return user
        else:
            return None    
from functools import lru_cache
from backend.app.core.mongodb import MongoDb
from backend.app.domains.user.user_service import UserService

@lru_cache()
def get_user_service() -> UserService:
    return UserService(MongoDb.get_client()["stockdb"])


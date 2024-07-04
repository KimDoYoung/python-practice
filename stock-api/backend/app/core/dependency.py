from functools import lru_cache
from backend.app.core.mongodb import MongoDb
from backend.app.domains.user.user_service import UserService
from backend.app.core.config import config

@lru_cache()
def get_user_service() -> UserService:
    db_name = config.DB_NAME
    return UserService(MongoDb.get_client()[db_name])


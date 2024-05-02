

from app.core.mongodb import MongoDb
from app.domain.users.user_service import UserService


def get_user_service() -> UserService:
    return UserService(MongoDb.get_client()["stockdb"])


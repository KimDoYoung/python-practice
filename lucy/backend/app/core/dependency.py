from backend.app.core.mongodb import MongoDb
from backend.app.domains.user.user_service import UserService


def get_user_service() -> UserService:
    return UserService(MongoDb.get_client()["stockdb"])


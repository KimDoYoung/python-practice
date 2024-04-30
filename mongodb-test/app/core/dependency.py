
from app.domain.users.user_service import UserService

def get_user_service() -> UserService:
    from ..main import app
    return app.state.user_service

from sqlalchemy.ext.asyncio import AsyncSession
from typing import  AsyncGenerator

from backend.app.core.database import AsyncSessionLocal
from backend.app.core.logger import get_logger
from backend.app.domains.user.appkey_service import AppKeyService
from backend.app.domains.openapi.dart_service import DartService

logger = get_logger(__name__)

# 데이터베이스 dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    logger.debug("----> Creating DB session.")
    db: AsyncSession = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()
        logger.debug("----> DB session closed.")

# Service dependencies
def get_dart_service() -> DartService:
    return DartService()

def get_appkey_service() -> AppKeyService:
    return AppKeyService()


logger.debug("----> Dependencies created.")

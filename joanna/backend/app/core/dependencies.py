from sqlalchemy.ext.asyncio import AsyncSession
from typing import  AsyncGenerator

from core.database import AsyncSessionLocal
from core.logger import get_logger

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

logger.debug("----> Dependencies created.")

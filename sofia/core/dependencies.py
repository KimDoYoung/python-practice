from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, AsyncGenerator

from core.database import AsyncSessionLocal
from services.image_folders_service import ImageFolderService
from core.logger import get_logger

logger = get_logger(__name__)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    logger.debug("----> Creating DB session.")
    db: AsyncSession = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()
        logger.debug("----> DB session closed.")

def get_folder_service() -> ImageFolderService:
    return ImageFolderService()

logger.debug("----> Dependencies created.")
db_dependency = Annotated[AsyncSession, Depends(get_db)]
folder_service_dependency = Annotated[ImageFolderService, Depends(get_folder_service)]
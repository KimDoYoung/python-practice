from sqlalchemy.ext.asyncio import AsyncSession
from typing import  AsyncGenerator

from core.database import AsyncSessionLocal
from services.image_file_service import ImageFileService
from services.image_folder_service import ImageFolderService
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
def get_folder_service() -> ImageFolderService:
    return ImageFolderService()

def get_file_service() -> ImageFileService:
    return ImageFileService()

logger.debug("----> Dependencies created.")
# db_dependency = Annotated[AsyncSession, Depends(get_db)]
# folder_service_dependency = Annotated[ImageFolderService, Depends(get_folder_service)]
# file_service_dependency = Annotated[ImageFileService, Depends(get_file_service)]
from models.image_file_model import ImageFile, ImageFileCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select  # Import the select function

class ImageFileService:

    async def get(self, db: AsyncSession, id : int) -> ImageFile:
        async with db as session:
            statement = select(ImageFile).where(ImageFile.id == id)
            result = await session.execute(statement)
            return result.scalars().first()

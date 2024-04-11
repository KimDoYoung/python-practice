from fastapi import HTTPException
from models.image_file_model import ImageFile, ImageFileCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select  # Import the select function

class ImageFileService:

    async def get(self, session: AsyncSession, id : int) -> ImageFile:
        statement = select(ImageFile).where(ImageFile.id == id)
        image_file = await session.execute(statement)
        
        if image_file is None:
            raise HTTPException(status_code=404, detail=f"ImageFile with id {id} not found")
    
        return image_file.scalars().first()

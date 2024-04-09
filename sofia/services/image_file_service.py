import asyncio
from sqlmodel import Session

from models.image_file_model import ImageFileCreate

class ImageFileService:
    async def create(self, image_file: ImageFileCreate, db: Session) -> ImageFile:
        db.add(image_file)
        await db.commit()
        await db.refresh(image_file)
        return image_file
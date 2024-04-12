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

    async def get_files(self, session: AsyncSession, ids : list[int]) -> list[ImageFile]:
        statement = select(ImageFile).where(ImageFile.id.in_(ids))
        image_files = await session.execute(statement)
        return image_files.scalars().all()
    
    async def delete_by_folder_id(self, folder_id: int, session: AsyncSession) -> int:
        """ 이미지 파일 테이블에서 folder_id로 이미지 파일 삭제"""
        statement = select(ImageFile).where(ImageFile.folder_id == folder_id)
        image_files = await session.execute(statement)
        i = 0
        for image_file in image_files.scalars().all():
            await session.delete(image_file)
            i += 1
        await session.commit()
        return i
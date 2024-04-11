import asyncio

from fastapi import Depends
from sqlmodel import Session
from sqlalchemy.future import select as async_select
from models.image_file_model import ImageFile
from models.image_folder_model import ImageFolderWithFiles, ImageFolders, ImageFoldersBase, ImageFoldersCreate

class ImageFolderService:

    async def create(self, folder: ImageFoldersCreate, db: Session) -> ImageFolders:
        new_folder = ImageFolders(**folder.model_dump())
        db.add(new_folder)
        await db.commit()
        await db.refresh(new_folder)
        return new_folder
    
    async def get(self, folder_id: int, db: Session) -> ImageFolderWithFiles:
        async with db as session:
            statement = async_select(ImageFolders).where(ImageFolders.id == folder_id)
            result = await session.execute(statement)
            folder = result.scalars().first()
            if folder is not None:
                folder_and_files = ImageFolderWithFiles(**folder.__dict__)
                statement = async_select(ImageFile).where(ImageFile.folder_id == folder_id).order_by(ImageFile.seq.asc())
                files = await session.execute(statement)
                folder_and_files.files = files.scalars().all()
            return folder_and_files

    async def get_all(self, db: Session) -> list[ImageFolders]:
        async with db as session:
            statement = async_select(ImageFolders).order_by(ImageFolders.id.desc()) # 최신순으로 정렬
            result = await session.execute(statement)
            return result.scalars().all()
import asyncio

from sqlalchemy.future import select 
from models.image_file_model import ImageFile
from models.image_folder_model import ImageFolderWithFiles, ImageFolder, ImageFolderCreate

from sqlalchemy.ext.asyncio import AsyncSession

class ImageFolderService:

    async def create(self, folder: ImageFolderCreate, db: AsyncSession) -> ImageFolder:
        new_folder = ImageFolder(**folder.model_dump())
        db.add(new_folder)
        await db.commit()
        await db.refresh(new_folder)
        return new_folder
    
    async def get(self, folder_id: int, db: AsyncSession) -> ImageFolderWithFiles:
        async with db as session:
            statement = select(ImageFolder).where(ImageFolder.id == folder_id)
            result = await session.execute(statement)
            folder = result.scalars().first()
            if folder is not None:
                folder_and_files = ImageFolderWithFiles(**folder.__dict__)
                statement = select(ImageFile).where(ImageFile.folder_id == folder_id).order_by(ImageFile.seq.asc())
                files = await session.execute(statement)
                folder_and_files.files = files.scalars().all()
            return folder_and_files

    async def get_all(self, db: AsyncSession) -> list[ImageFolder]:
        async with db as session:
            statement = select(ImageFolder).order_by(ImageFolder.id.desc()) # 최신순으로 정렬
            result = await session.execute(statement)
            return result.scalars().all()
    
    async def delete(self, folder_id: int, db: AsyncSession) -> ImageFolder:
        async with db.begin():  # 트랜잭션 시작
            result = await db.execute(select(ImageFolder).where(ImageFolder.id == folder_id))
            folder_to_delete = result.scalars().first()

            if not folder_to_delete:
                # 삭제할 데이터가 없으면 예외 처리
                raise ValueError(f"Folder with id {folder_id} not found")

            # 데이터 삭제
            await db.delete(folder_to_delete)

            # 변경 사항을 데이터베이스에 커밋
            await db.commit()

            # 삭제된 폴더 객체 반환
            return folder_to_delete
    
    async def get_folder_path(self, folder_id : int, db: AsyncSession) -> str:
        async with db as session:
            statement = select(ImageFolder.folder_path).where(ImageFolder.id == folder_id)
            result = await session.execute(statement)
            return result.scalars().first()
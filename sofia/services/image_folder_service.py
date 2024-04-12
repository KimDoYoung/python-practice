from fastapi import HTTPException
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
    
    async def get(self, folder_id: int, session: AsyncSession) -> ImageFolderWithFiles:
        """
            folder_id에 해당하는 폴더 정보와 폴더에 속한 파일들을 조회
        """
        statement = select(ImageFolder).where(ImageFolder.id == folder_id)
        result = await session.execute(statement)
        folder = result.scalars().first()
        if not folder:
            raise HTTPException(status_code=404, detail=f"Folder with id {folder_id} not found")
        folder_and_files = ImageFolderWithFiles(**folder.__dict__)
        statement = select(ImageFile).where(ImageFile.folder_id == folder_id).order_by(ImageFile.seq.asc())
        files = await session.execute(statement)
        folder_and_files.files = files.scalars().all()
        return folder_and_files

    async def get_all(self, session: AsyncSession) -> list[ImageFolder]:
        statement = select(ImageFolder).order_by(ImageFolder.id.desc()) # 최신순으로 정렬
        result = await session.execute(statement)
        return result.scalars().all()
    
    async def delete(self, folder_id: int, session: AsyncSession) -> ImageFolder:
        async with session.begin():  # 트랜잭션 시작
            result = await session.execute(select(ImageFolder).where(ImageFolder.id == folder_id))
            folder_to_delete = result.scalars().first()

            if not folder_to_delete:
                raise HTTPException(status_code=404, detail=f"Folder with id {folder_id} not found")

            # 데이터 삭제
            await session.delete(folder_to_delete)

            # 변경 사항을 데이터베이스에 커밋
            await session.commit()

            # 삭제된 폴더 객체 반환
            return folder_to_delete
    
    async def get_folder_path(self, folder_id : int, session: AsyncSession) -> str:
        '''
        folder_id에 해당하는 폴더의 경로를 반환
        '''
        statement = select(ImageFolder.folder_path).where(ImageFolder.id == folder_id)
        result = await session.execute(statement)
        if not result:
            raise HTTPException(status_code=404, detail=f"Folder with id {folder_id} not found")
        return result.scalars().first()
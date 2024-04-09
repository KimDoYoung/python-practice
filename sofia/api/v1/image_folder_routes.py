from fastapi import APIRouter, Depends, Form
import os
from core.exceptions import FolderNotFoundError
from core.dependencies import db_dependency, folder_service_dependency
from models.image_file_model import ImageFile, ImageFileCreate
from models.image_folder_model import ImageFolders, ImageFoldersCreate


router = APIRouter()


def is_image_file(filename):
    # 지원하는 이미지 파일 확장자 리스트
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    # 파일의 확장자를 추출하고 소문자로 변환하여 유효한지 확인
    extension = os.path.splitext(filename)[1].lower()
    return extension in valid_extensions

#C:\Users\deHong\tmp\도서\주식 자동 거래 시스템 구축
@router.post("/folders/add")
async def folders_add(db: db_dependency, service: folder_service_dependency, folder_name: str = Form(...)):
    """
    1. folder_name이 물리적으로 존재하는지 체크
    2. 존재하지 않으면 raise sofia_exceptions.FolderNotFoundError
    3. 존재하면 폴더내의 파일들을 모두 읽어서 파일이 생긴 순서대로 DB image_folders에 저장
    4. DB에 저장된 파일 정보를 반환
    """
    if not os.path.exists(folder_name):
        raise FolderNotFoundError
        
    # 폴더 내의 파일 리스트 얻기 (생성 시간으로 정렬)
    files = sorted(
        [file for file in os.listdir(folder_name) if is_image_file(file)],
        key=lambda x: os.path.getctime(os.path.join(folder_name, x))
    )
    folder = ImageFoldersCreate(folder_name=folder_name)

    # new_folder = await service.create(folder, db)
    async with db.begin():
        new_folder = ImageFolders(**folder.model_dump())
        db.add(new_folder)
        await db.flush()
        await db.refresh(new_folder)
        new_folder_id = new_folder.id
        for idx, file_name in enumerate(files):
            image_file = ImageFile(org_name=file_name, seq=idx+10, folder_id=new_folder_id)
            db.add(image_file)
    # `async with db.begin():` 블록을 벗어나면 자동으로 커밋됩니다.            
    return {"folder_id": new_folder.id}


    
    # statement = text("INSERT INTO image_folders (folder_name) VALUES (:folder_name)")
    # async with db_session.create_async_session() as session:
    #     async with session.begin():  # 트랜잭션 시작
    #         await session.execute(statement=statement, params={"folder_name": folder_name})
    #         # 마지막에 삽입된 행의 ID를 얻기 위한 쿼리
    #         last_id_query = text("SELECT last_insert_rowid()")
    #         last_id_result = await session.execute(last_id_query)
    #         last_folder_id = last_id_result.scalar_one()  # scalar_one()을 사용하여 결과값을 가져옴
    #         # file 추가.
    #         seq = 1
    #         for file_name in files:
    #             file_path = os.path.join(folder_name, file_name)
    #             image_file = ImageFileSchema(
    #                 org_name=file_name,
    #                 seq=seq,
    #                 folder_id=last_folder_id
    #             )
    #             seq += 10
    #             session.add(image_file)
    #         session.commit()    
    
    # return {"folder_id": last_folder_id}

@router.get("/folders/{folder_id}")
async def get_folder(folder_id: int, thumb: bool = False):
    # Logic to retrieve the list of images in the specified folder
    # If thumb is True, display the images in thumbnail style
    return {"message": f"Retrieving images in folder {folder_id}"}

@router.delete("/folders/delete/{folder_id}")
async def delete_folder(folder_id: int):
    # Logic to delete the specified folder and its associated image files
    return {"message": f"Folder {folder_id} deleted along with its image files"}
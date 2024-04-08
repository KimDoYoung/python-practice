from fastapi import APIRouter
import os
from core.sofia_exceptions import FolderNotFoundError

router = APIRouter()

@router.post("/folders/load")
async def create_folder(folder_name: str):
    """
    1. folder_name이 물리적으로 존재하는지 체크
    2. 존재하지 않으면 raise sofia_exceptions.FolderNotFoundError
    3. 존재하면 폴더내의 파일들을 모두 읽어서 파일이 생긴 순서대로 DB image_folders에 저장
    4. DB에 저장된 파일 정보를 반환
    """
    # 폴더가 없으면 FolderNotFoundError 예외 발생
    if not os.path.exists(folder_name):
        raise FolderNotFoundError
    
    query = "INSERT INTO image_folders (folder_name) VALUES (:folder_name)"
    await db_connection.execute(query=query, values={"folder_name": folder_name})

    # 마지막에 삽입된 행의 ID를 얻기 위한 쿼리
    last_id_query = "SELECT last_insert_rowid();"
    last_id = await db_connection.fetch_val(query=last_id_query)


    # Logic to read all files in the folder and save them to the image_folders DB
    # Return the file information from the DB
@router.get("/folders/{folder_id}")
async def get_folder(folder_id: int, thumb: bool = False):
    # Logic to retrieve the list of images in the specified folder
    # If thumb is True, display the images in thumbnail style
    return {"message": f"Retrieving images in folder {folder_id}"}

@router.delete("/folders/delete/{folder_id}")
async def delete_folder(folder_id: int):
    # Logic to delete the specified folder and its associated image files
    return {"message": f"Folder {folder_id} deleted along with its image files"}
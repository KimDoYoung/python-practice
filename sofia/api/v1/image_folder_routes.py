from fastapi import APIRouter, Depends, Form, Request
import os

from fastapi.responses import HTMLResponse, RedirectResponse
from core.exceptions import FolderNotFoundError
from core.dependencies import db_dependency, folder_service_dependency
from core.logger import get_logger
from core.template_engine import render_template
from core.util import is_image_file
from models.image_file_model import ImageFile, ImageFileCreate
from models.image_folder_model import ImageFolders, ImageFoldersCreate
from starlette.status import HTTP_303_SEE_OTHER

router = APIRouter()

logger = get_logger(__name__)

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
    
    short_folder_name = os.path.basename(folder_name)
    note = f"org folder name : {folder_name}"
    folder = ImageFoldersCreate(folder_name=short_folder_name, note=note)

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
    # return {"folder_id": new_folder.id}
    return RedirectResponse(f"/folders/{new_folder.id}", status_code=HTTP_303_SEE_OTHER)

# folder_id에 해당하는 폴더의 이미지 목록을 조회
@router.get("/folders/{folder_id}", response_class=HTMLResponse)
async def get_folder(request: Request, db: db_dependency, service: folder_service_dependency, folder_id: int, thumb: bool = False):
    folder = await service.get(folder_id, db)
    folder_json = folder.model_dump()
    logger.debug(f"folder_json: {folder_json}")
    context = {"request": request,  "folder": folder_json}
    return render_template("view.html", context)

@router.delete("/folders/delete/{folder_id}")
async def delete_folder(folder_id: int):
    # Logic to delete the specified folder and its associated image files
    return {"message": f"Folder {folder_id} deleted along with its image files"}
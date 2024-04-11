import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from core.dependencies import get_db, get_file_service, get_folder_service
from core.logger import get_logger
from core.util import get_mime_type

router = APIRouter()

logger = get_logger(__name__)

@router.get("/image/{file_id}")
#async def get_image(file_id: int, db=Depends(get_db), file_service=Depends(get_file_service), folder_service=Depends(get_folder_service)):
async def get_image(file_id: int, db=Depends(get_db), file_service=Depends(get_file_service), folder_service=Depends(get_folder_service)):

    image_file = await file_service.get(db=db, id=file_id)
    if not image_file:
        raise HTTPException(status_code=404, detail="Image not found")
    folder_path = await folder_service.get_folder_path(image_file.folder_id, db)
    fullpath = os.path.join(folder_path, image_file.org_name)
    
    # 파일의 MIME 타입 결정
    mime_type = get_mime_type(image_file.org_name)
    
    return FileResponse(fullpath, media_type=mime_type)
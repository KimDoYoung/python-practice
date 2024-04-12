import os
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse

from core.dependencies import get_db, get_file_service, get_folder_service
from core.logger import get_logger
from core.util import get_mime_type

router = APIRouter()

logger = get_logger(__name__)

@router.get("/image/{file_id}")
async def get_image(request: Request, file_id: int, db=Depends(get_db), file_service=Depends(get_file_service), folder_service=Depends(get_folder_service)):
    """
    이미지 파일을 반환, thumb가 parameter로 전달되면 썸네일을 반환, 썸네일파일이 없으면 원본 이미지를 반환
    """
    if "thumb" in request.query_params:
        image_file = await file_service.get(db, file_id)
        if not image_file:
            raise HTTPException(status_code=404, detail="Image not found")
        folder_path = await folder_service.get_folder_path(image_file.folder_id, db)        
        fullpath = os.path.join(folder_path, "thumbs",image_file.thumb_path)
        if not os.path.exists(fullpath):
            fullpath = os.path.join(folder_path, image_file.org_name)
    else:
        image_file = await file_service.get(db, file_id)
        if not image_file:
            raise HTTPException(status_code=404, detail="Image not found")
        folder_path = await folder_service.get_folder_path(image_file.folder_id, db)
        fullpath = os.path.join(folder_path, image_file.org_name)
        
        # 파일의 MIME 타입 결정
    mime_type = get_mime_type(fullpath)
    logger.debug("fullpath : %s", fullpath)
    return FileResponse(fullpath, media_type=mime_type)
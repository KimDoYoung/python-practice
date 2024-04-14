import os
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import FileResponse, RedirectResponse

from core.dependencies import get_db, get_file_service, get_folder_service
from core.logger import get_logger
from core.util import backup_and_rotate_image, get_mime_type
from starlette import status

router = APIRouter()

logger = get_logger(__name__)

@router.get("/image/{file_id}")
async def get_image(request: Request, file_id: int, db=Depends(get_db), file_service=Depends(get_file_service), folder_service=Depends(get_folder_service)):
    """
    이미지 파일을 반환, thumb가 parameter로 전달되면 썸네일을 반환 이경우 썸네일파일이 없으면 원본 이미지를 반환
    """
    if "thumb" in request.query_params:
        image_file = await file_service.get(db, file_id)
        if not image_file:
            raise HTTPException(status_code=404, detail="Image not found")
        folder_path = await folder_service.get_folder_path(image_file.folder_id, db)
        if image_file.thumb_path is not None and image_file.thumb_path != "":
            fullpath = os.path.join(folder_path, "thumbs",image_file.thumb_path)
            if not os.path.exists(fullpath):
                fullpath = os.path.join(folder_path, image_file.org_name)
        else:
            fullpath = os.path.join(folder_path, image_file.org_name)        
            logger.debug("fullpath : %s 는 thumb가 존재하지 않음", fullpath)
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

@router.get("/image/rotate/{folder_id}")
async def image_rotate(folder_id: int, images: list[int] = Query(None), 
                       db=Depends(get_db), folder_service=Depends(get_folder_service), file_service=Depends(get_file_service)):
    """
    선택된 이미지를 90도 회전시킨다.
    """
    if not images:
        raise HTTPException(status_code=400, detail="No images provided")
    
    base_folder = await folder_service.get_folder_path(folder_id, db)
    image_list = await file_service.get_files(db, images)
    for image in image_list:
        fullpath = os.path.join(base_folder, image.org_name)
        backup_and_rotate_image(fullpath)
        # thumb가 있으면 그것도 rotate시킨다.
        thumb_path = os.path.join(base_folder, "thumbs", image.thumb_path)
        if os.path.exists(thumb_path):
            backup_and_rotate_image(thumb_path)

    return RedirectResponse(f"/folder/{folder_id}", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/image/delete/{folder_id}")
async def image_delete(folder_id: int, images: list[int] = Query(None), 
                       db=Depends(get_db), folder_service=Depends(get_folder_service), file_service=Depends(get_file_service)):
    """ 선택된 이미지를 삭제한다. """
    if not images:
        raise HTTPException(status_code=400, detail="No images provided")
    
    base_folder = await folder_service.get_folder_path(folder_id, db)
    image_list = await file_service.get_files(db, images)
    for image in image_list:
        fullpath = os.path.join(base_folder, image.org_name)
        # 물리적 파일 삭제
        os.remove(fullpath)
        thumb_path = os.path.join(base_folder, "thumbs", image.thumb_path)
        # thumb파일이 있으면 삭제
        if os.path.exists(thumb_path):
            os.remove(thumb_path)
        # DB에서 삭제
        await file_service.delete(db, image.id)    

    return RedirectResponse(f"/folder/{folder_id}", status_code=status.HTTP_303_SEE_OTHER)
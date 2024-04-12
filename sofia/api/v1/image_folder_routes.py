from fastapi import APIRouter, Depends, Form, Request
import os
from PIL import Image
import exifread
from datetime import datetime
from fastapi.responses import HTMLResponse, RedirectResponse
from core.exceptions import FolderNotFoundError
from core.dependencies import  get_db, get_folder_service
from core.logger import get_logger
from core.template_engine import render_template
from core.util import convert_to_datetime, is_image_file, safe_float_conversion
from models.image_file_model import ImageFile
from models.image_folder_model import ImageFolder, ImageFolderCreate
from starlette.status import HTTP_303_SEE_OTHER
from fastapi import Depends

router = APIRouter()

logger = get_logger(__name__)

#C:\Users\deHong\tmp\도서\주식 자동 거래 시스템 구축
@router.post("/folders/add")
# async def folders_add(db: Depends = Depends(get_db), folder_name: str = Form(...)):
async def folders_add(db = Depends(get_db), folder_name: str = Form(...)):
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
    folder = ImageFolderCreate(folder_name=short_folder_name, folder_path=folder_name, note=note)

    async with db.begin():
        new_folder = ImageFolder(**folder.model_dump())
        db.add(new_folder)
        await db.flush()
        await db.refresh(new_folder)
        new_folder_id = new_folder.id
        for idx, file_name in enumerate(files):
            full_path = os.path.join(folder_name, file_name)
            image_file = create_thumb_and_get_attribute(full_path)
            image_file.folder_id = new_folder_id
            image_file.seq = idx+10
            #image_file = ImageFile(org_name=file_name, seq=idx+10, folder_id=new_folder_id)
            db.add(image_file)
    # `async with db.begin():` 블록을 벗어나면 자동으로 커밋됩니다.          
    return RedirectResponse(f"/folders/{new_folder.id}", status_code=HTTP_303_SEE_OTHER)

# folder_id에 해당하는 폴더의 이미지 목록을 조회    
@router.get("/folders/{folder_id}", response_class=HTMLResponse)
async def get_folder(request: Request, folder_id: int,thumb: bool = False, db = Depends(get_db), service= Depends(get_folder_service) ):
    '''
    폴더 아이디에 해당하는 폴더 정보를 조회하는 API
    '''
    folder = await service.get(folder_id, db)
    folder_json = folder.model_dump()
    logger.debug(f"folder_json: {folder_json}")
    context = {"request": request,  "folder": folder_json}
    return render_template("view.html", context)

@router.delete("/folders/{folder_id}")
async def delete_folder(folder_id: int, db=Depends(get_db), service = Depends(get_folder_service)):
    folder = await service.delete(folder_id, db)
    logger.debug(f"Folder {folder.folder_name} deleted along with its image files")
    return RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)


def create_thumb_and_get_attribute(full_path):
    # 썸네일이 저장될 폴더 경로를 설정
    base_dir = os.path.dirname(full_path)
    thumbs_dir = os.path.join(base_dir, 'thumbs')
    
    # thumbs 폴더가 없다면 생성
    os.makedirs(thumbs_dir, exist_ok=True)

    # 원본 이미지를 불러옴
    with Image.open(full_path) as img:
        max_size = 300
        if img.height > max_size or img.width > max_size:
            # 이미지 크기 비율에 맞게 조정
            if img.height > img.width:
                height_percent = max_size / float(img.height)
                width_size = int((float(img.width) * float(height_percent)))
                img = img.resize((width_size, max_size), Image.Resampling.LANCZOS)
            else:
                width_percent = max_size / float(img.width)
                height_size = int((float(img.height) * float(width_percent)))
                img = img.resize((max_size, height_size), Image.Resampling.LANCZOS)

            # 썸네일 이미지 파일명 설정 및 저장
            thumb_name = os.path.basename(full_path).rsplit('.', 1)[0] + '_thumb.png'
            thumb_path = os.path.join(thumbs_dir, thumb_name)
            img.save(thumb_path, 'PNG')            
        else:
            thumb_path = None

        # 이미지 메타데이터 읽기
        with open(full_path, 'rb') as f:
            tags = exifread.process_file(f)

        # ImageFile 객체 생성
        image_file = ImageFile(
            org_name=os.path.basename(full_path),
            image_format=img.format,
            image_width=img.width,
            image_height=img.height,
            image_mode=img.mode,
            thumb_path=thumb_path
        )

        # Exif 데이터에서 추가적인 정보 추출
        def get_tag_value(tags, tag, default=None):
            return str(tags.get(tag, default))

        image_file.camera_manufacturer = get_tag_value(tags, 'Image Make')
        image_file.camera_model = get_tag_value(tags, 'Image Model')
        #image_file.capture_date_time = get_tag_value(tags, 'EXIF DateTimeOriginal')
        # capture_date_time 값이 문자열 'None' 대신 실제 날짜 문자열이거나 None일 때의 처리
        image_file.capture_date_time = convert_to_datetime(get_tag_value(tags, 'EXIF DateTimeOriginal'))
        image_file.shutter_speed = safe_float_conversion(get_tag_value(tags, 'EXIF ShutterSpeedValue'))
        image_file.aperture_value = safe_float_conversion(get_tag_value(tags, 'EXIF ApertureValue'))
        image_file.iso_speed = safe_float_conversion(get_tag_value(tags, 'EXIF ISOSpeedRatings'))
        image_file.focal_length = safe_float_conversion(get_tag_value(tags, 'EXIF FocalLength'))
        image_file.gps_latitude = safe_float_conversion(get_tag_value(tags, 'GPS GPSLatitude'))
        image_file.gps_longitude = safe_float_conversion(get_tag_value(tags, 'GPS GPSLongitude'))
        image_file.image_orientation = get_tag_value(tags, 'Image Orientation')

        return image_file
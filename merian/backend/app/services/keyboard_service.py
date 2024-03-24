import uuid
import aiofiles
from fastapi import UploadFile
from fastapi import UploadFile
from datetime import datetime
import shutil
from pathlib import Path

from backend.app.core.configs import FILE_DIR

#FILE_DIR = "path/to/your/base/directory"  # 기본 파일 저장 경로 설정

async def save_upload_file(upload_file: UploadFile) -> tuple:
    date_path = datetime.now().strftime("%Y/%m")
    save_dir = Path(FILE_DIR) / date_path
    save_dir.mkdir(parents=True, exist_ok=True)

    ext = upload_file.filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{ext}"
    file_path = save_dir / unique_filename

    file_size = 0  # 파일 크기 초기화
    mime_type = upload_file.content_type  # 파일의 MIME 타입 추출

    async with upload_file.file as file:
        content = await file.read()  # 파일 내용 읽기
        file_size = len(content)  # 파일 크기 계산
        async with aiofiles.open(file_path, 'wb') as out_file:
            await out_file.write(content)  # 파일 쓰기

    # 저장된 파일의 폴더 경로, 파일명, 확장자, 파일 크기, MIME 타입 반환
    return (str(save_dir), unique_filename, ext, file_size, mime_type)


import asyncio
import uuid
from fastapi import UploadFile
from fastapi import UploadFile
from datetime import datetime
import shutil
from pathlib import Path

from backend.app.core.configs import FILE_DIR

async def save_upload_file(upload_file: UploadFile) -> tuple:
    date_path = datetime.now().strftime("%Y/%m")
    save_dir = Path(FILE_DIR) / date_path
    save_dir.mkdir(parents=True, exist_ok=True)  # 동기적인 부분

    ext = upload_file.filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    file_path = save_dir / unique_filename

    mime_type = upload_file.content_type  # 파일의 MIME 타입 추출

    # 파일 쓰기 작업을 비동기적으로 수행
    loop = asyncio.get_running_loop()
    file_size = await loop.run_in_executor(None, save_file, upload_file.file, file_path)

    # 저장된 파일의 폴더 경로, 파일명, 확장자, 파일 크기, MIME 타입 반환
    return (str(save_dir), unique_filename, ext, file_size, mime_type)

def save_file(file, file_path):
    with open(file_path, 'wb') as out_file:
        shutil.copyfileobj(file, out_file)
    return file_path.stat().st_size

import os

def delete_physical_file(file_path):
    """
    물리적 파일을 조용히 삭제하는 함수.
    파일 경로를 인자로 받아 파일이 존재하면 삭제한다.
    파일 삭제 성공 여부만 반환한다.

    :param file_path: 삭제할 파일의 전체 경로
    :return: bool 파일 삭제 성공 여부
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
    except Exception:
        # 예외가 발생하더라도 여기서 처리하고, 실패했다는 것을 나타내기 위해 False 반환
        pass
    return False

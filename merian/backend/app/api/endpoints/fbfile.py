import aiofiles
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from backend.app.core.logger import get_logger
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.keyboard import FBFile
from backend.app.services.db_service import get_db

router = APIRouter()
logger = get_logger(__name__)

@router.get("/file/{id}")
async def view_file(id: int, db: AsyncSession = Depends(get_db)):
    # 비동기 방식으로 데이터베이스에서 파일 메타데이터 조회
    async with db as session:
        result = await session.execute(select(FBFile).filter(FBFile.file_id == id))
        file_data = result.scalars().first()
    if not file_data:
        raise HTTPException(status_code=404, detail="File not found")

    file_path = f"{file_data.phy_folder}/{file_data.phy_name}"

    # 비동기 방식으로 파일 내용을 스트리밍하는 함수
    async def file_generator(file_path):
        async with aiofiles.open(file_path, mode='rb') as f:
            async for line in f:
                yield line

    try:
        # 파일이 실제로 존재하는지 확인
        async with aiofiles.open(file_path, mode='rb'):
            pass
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found on server")

    # StreamingResponse를 사용하여 비동기 파일 스트림 응답 반환
    return StreamingResponse(file_generator(file_path), media_type=file_data.mime_type)
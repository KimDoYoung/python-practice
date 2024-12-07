# nodefile_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session

router = APIRouter()

#TODO: 이미지 회전 기능 구현
@router.get("/rotate/image/{file_id}/{degree}", summary="이미지 회전")
async def get_nodefile(file_id: int, degree: int, db: AsyncSession = Depends(get_session)):
    """
    이미지 파일을 회전합니다.
    - **file_id**: 파일 ID
    - **degree**: 회전 각도
    """
    pass

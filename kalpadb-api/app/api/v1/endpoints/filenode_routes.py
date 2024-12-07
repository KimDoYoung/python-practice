# nodefile_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.domain.filenode.filenode_service import ApNodeFileService

router = APIRouter()

@router.get("/rotate/image/{file_id}/{degree}", summary="이미지 회전")
async def get_nodefile(file_id: int, degree: int, db: AsyncSession = Depends(get_session)):
    """
    이미지 파일을 회전합니다.
    - **file_id**: 파일 ID
    - **degree**: 회전 각도
    """
    if degree not in [90, 180, 270]:
        raise ValueError("회전 각도는 90, 180, 270 중 하나여야 합니다.")
    service = ApNodeFileService(db)
    if service.rotate_image(file_id, degree):
        return {"message": "이미지 회전이 완료되었습니다."}
    else:
        return {"message": "이미지 회전에 실패했습니다."}



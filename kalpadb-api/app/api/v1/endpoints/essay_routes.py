from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.domain.essay.essay_schema import EssayResponse, EssayUpsertRequest
from app.domain.essay.essay_service import EssayService


router = APIRouter()

@router.post("/essay/upsert", response_model=EssayResponse)
async def upsert_essay(request: EssayUpsertRequest, db: AsyncSession = Depends(get_session)):
    ''' 에세이 생성 또는 수정 '''
    service = EssayService(db)
    return await service.upsert_essay(request)

@router.get("/essay/{essay_id}", response_model=EssayResponse)
async def get_essay(essay_id: int, db: AsyncSession = Depends(get_session)):
    ''' 특정 ID로 에세이 조회 '''
    service = EssayService(db)
    return await service.get_essay(essay_id)

#TODO: 에세이 삭제 API 추가
#TODO: 에세이 조회 10개씩 페이징 처리 API 추가
@router.get("/essays", response_model=list[EssayResponse])
async def get_essays(db: AsyncSession = Depends(get_session)):
    ''' 모든 에세이 조회 '''
    service = EssayService(db)
    return await service.get_essays()
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.domain.essay.essay_schema import EssayListRequest, EssayListResponse, EssayResponse, EssayUpsertRequest
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

@router.delete("/essay/{id}", response_model=EssayResponse)
async def delete_essay(id:int, db: AsyncSession = Depends(get_session)):
    ''' 에세이 1개 삭제 '''
    service = EssayService(db)
    return await service.delete_essay(id)

@router.get("/essays", response_model=EssayListResponse, summary="에세이 Page 조회")
async def get_essays(search_text:str=None, 
                    limit: int=10,
                    start_index: int=0,
                    title_only: bool=False,
                    db: AsyncSession = Depends(get_session)):
    ''' 에세이 1 page 조회 '''
    service = EssayService(db)
    request = EssayListRequest(search_text=search_text, 
                            limit=limit, 
                            start_index=start_index, 
                            title_only=title_only)
    return await service.get_essays(request)
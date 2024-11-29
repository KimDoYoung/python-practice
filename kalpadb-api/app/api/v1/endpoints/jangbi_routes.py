# diary_routes.py
"""
모듈 설명: 
    -  장비(구매물품) 관련 API 라우터
주요 기능:

작성자: 김도영
작성일: 2024-11-28
버전: 1.0
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.domain.jangbi.jangbi_schema import JangbiListParam, JangbiListResponse, JangbiResponse
from app.domain.jangbi.jangbi_service import JangbiService

router = APIRouter()

@router.get("/jangbies", response_model=JangbiListResponse)
async def get_jangbi_list(
    start_ymd: str = '19700101',
    end_ymd: str = '99991231',
    search_text : str | None = None,
    lvl : str | None = None,
    order_direction : str = 'desc',
    start_idx : int = 0,
    limit : int = 10,
    db: AsyncSession = Depends(get_session)
):
    ''' 장비 리스트 조회 '''
    service = JangbiService(db)
    param = JangbiListParam(
        start_ymd=start_ymd,
        end_ymd=end_ymd,
        search_text=search_text,
        lvl=lvl,
        order_direction=order_direction,
        start_idx=start_idx,
        limit=limit
    )
    return await service.jangbi_list(param)

@router.get("/jangbi/{jangbi_id}", response_model=JangbiResponse)


@router.post("/jangbi", response_model=JangbiResponse)
async def upsert_diary(
    db: AsyncSession = Depends(get_session)
):
    ''' 장비 생성 또는 수정 '''
    pass

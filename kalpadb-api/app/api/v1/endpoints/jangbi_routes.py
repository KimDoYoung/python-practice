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

router = APIRouter()

@router.post("/jangbi", response_model=JangbiResponse)
async def upsert_diary(
    db: AsyncSession = Depends(get_session)
):
    ''' 장비 생성 또는 수정 '''
    pass

from typing import List
from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.domain.calendar.calendar_schema import CalendarRequest, CalendarResponse
from app.domain.calendar.calendar_service import CalendarService


router = APIRouter()

@router.post("/calendar", response_model=CalendarResponse)
async def insert_calendars(
    req: CalendarRequest,
    db: AsyncSession = Depends(get_session)
):
    ''' 일정 목록 생성 '''
    service = CalendarService(db)
    return  await service.create_calendar(req)

@router.get("/calendar/{yyyymm}", response_model=List[CalendarResponse])
async def get_calendars(yyyymm: str, db: AsyncSession = Depends(get_session)):
    ''' 일정 목록 조회 '''
    service = CalendarService(db)
    return await service.get_1month_calendars(yyyymm)



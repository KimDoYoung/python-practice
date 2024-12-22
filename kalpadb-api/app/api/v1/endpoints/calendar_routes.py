from typing import List
from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.domain.calendar.calendar_schema import CalendarRequest, CalendarResponse
from app.domain.calendar.calendar_service import CalendarService


router = APIRouter()

@router.post("/calendar", summary="일정 저장", response_model=CalendarResponse)
async def insert_calendars(
    req: CalendarRequest,
    db: AsyncSession = Depends(get_session)
):
    ''' 일정 목록 생성 '''
    service = CalendarService(db)
    return  await service.create_calendar(req)

@router.get("/calendar/{yyyymm}", summary="1달 일정 목록리스트", response_model=List[CalendarResponse])
async def get_calendars(yyyymm: str, db: AsyncSession = Depends(get_session)):
    ''' 일정 목록 조회 '''
    service = CalendarService(db)
    response =  await service.get_1month_calendars(yyyymm)

    # 몇개의 날짜에 대해서 음력 날짜를 구해야 함
    extutil_service = extutil_service.ExtUtilService(db)

    sol_array = yyyymm+"01"|yyyymm+"07"|yyyymm+"15"|yyyymm+"25"
    sol_array = sol_array + "|" + extutil_service.last_yyyymmdd(yyyymm)

    sol_lun_array = extutil_service.sol2lun_array(response)




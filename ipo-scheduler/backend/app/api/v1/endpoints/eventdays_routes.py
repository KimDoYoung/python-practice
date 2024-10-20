from typing import List
from fastapi import APIRouter, Depends
from backend.app.core.dependency import get_eventdays_service
from backend.app.domains.system.eventdays_model import EventDays
from backend.app.domains.system.eventdays_service import EventDaysService


# APIRouter 인스턴스 생성
router = APIRouter()

@router.get("/{yyyymm}", response_model=List[EventDays])
async def get_all(yyyymm:str, event_service :EventDaysService=Depends(get_eventdays_service)):
    days = await event_service.get_all(yyyymm)
    return days

@router.get("/calendar/{startYmd}/{endYmd}", response_model=List[EventDays])
async def get_between(startYmd: str, endYmd : str, event_service :EventDaysService=Depends(get_eventdays_service)):
    '''달력에 사용할 휴일정보 조회'''
    days = await event_service.get_days_between(startYmd, endYmd)
    return days
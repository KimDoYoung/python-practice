from typing import List
from fastapi import APIRouter, Depends
from backend.app.core.dependency import get_eventdays_service
from backend.app.domains.system.eventdays_model import EventDays
from backend.app.domains.system.eventdays_service import EventDaysService


# APIRouter 인스턴스 생성
router = APIRouter()

@router.get("/eventdays/{yyyymm}", response_model=List[EventDays])
async def get_all(yyyymm:str, event_service :EventDaysService=Depends(get_eventdays_service)):
    days = await event_service.get_all(yyyymm)
    return days
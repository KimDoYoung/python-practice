# APIRouter 인스턴스 생성
from typing import List

from fastapi import APIRouter, Depends

from backend.app.domains.system.ipo_model import Ipo, IpoDays
from backend.app.domains.system.ipo_service import IpoService
from backend.app.core.dependency import get_ipo_service
from backend.app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

@router.get("/ipo/days/{yyyymm}", response_model=List[IpoDays])
async def get_all(yyyymm:str, ipo_service :IpoService=Depends(get_ipo_service)):
    ''' 공모주 일정 조회'''
    ipo_list = await ipo_service.get_days(yyyymm)
    days = []
    for ipo in ipo_list:
        if ipo.days.청약일 and ipo.days.청약일.startswith(yyyymm):
            ipo_day = IpoDays(company=ipo.name, name='청약일', ymd=ipo.days.청약일)
            days.append(ipo_day)
        if ipo.days.납입일 and ipo.days.납입일.startswith(yyyymm):
            ipo_day = IpoDays(company=ipo.name, name='납입일', ymd=ipo.days.납입일)
            days.append(ipo_day)    
        if ipo.days.환불일 and ipo.days.환불일.startswith(yyyymm):
            ipo_day = IpoDays(company=ipo.name, name='환불일', ymd=ipo.days.환불일)
            days.append(ipo_day)    
        if ipo.days.상장일 and ipo.days.상장일.startswith(yyyymm):
            ipo_day = IpoDays(company=ipo.name, name='상장일', ymd=ipo.days.상장일)
            days.append(ipo_day)
    
    logger.debug(days)

    return days
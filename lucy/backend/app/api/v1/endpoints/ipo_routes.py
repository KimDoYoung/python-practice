# APIRouter 인스턴스 생성
from typing import List

from fastapi import APIRouter, Depends

from backend.app.domains.ipo.ipo_model import Ipo, IpoDays
from backend.app.domains.ipo.ipo_service import IpoService
from backend.app.core.dependency import get_ipo_service
from backend.app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

@router.get("/", response_model=List[Ipo])
async def get_ipo_list(ipo_service :IpoService=Depends(get_ipo_service)) -> List[Ipo]:
    ''' 공모주 목록 조회'''
    list = await ipo_service.get_all(onlyFuture=True)
    return list

@router.get("/calendar/{startYmd}/{endYmd}", response_model=List[IpoDays])
async def get_calendar(startYmd:str, endYmd:str, ipo_service :IpoService=Depends(get_ipo_service)):
    ''' 공모주 일정 조회'''
    ipo_list = await ipo_service.get_days_between(startYmd, endYmd)
    days = []
    for ipo in ipo_list:
        logger.debug(f"{ipo.name} {ipo.days}")
        if ipo.days.청약일:
            ipo_day = IpoDays(company=ipo.name, name='청약일', ymd=ipo.days.청약일, title=ipo.title, scrap_url=ipo.scrap_url)
            days.append(ipo_day)
        if ipo.days.납입일 and ipo.days.환불일:
            if ipo.days.납입일 == ipo.days.환불일:
                ipo_day = IpoDays(company=ipo.name, name='납입/환불일', ymd=ipo.days.납입일, title=ipo.title, scrap_url=ipo.scrap_url)
                days.append(ipo_day)
            else:
                ipo_day1 = IpoDays(company=ipo.name, name='납입일', ymd=ipo.days.납입일, title=ipo.title, scrap_url=ipo.scrap_url)
                ipo_day2 = IpoDays(company=ipo.name, name='환불일', ymd=ipo.days.환불일, title=ipo.title, scrap_url=ipo.scrap_url)
                days.append(ipo_day1)
                days.append(ipo_day2)
        elif ipo.days.납입일:
            ipo_day = IpoDays(company=ipo.name, name='납입일', ymd=ipo.days.납입일, title=ipo.title, scrap_url=ipo.scrap_url)
            days.append(ipo_day)
        elif ipo.days.환불일:
            ipo_day = IpoDays(company=ipo.name, name='환불일', ymd=ipo.days.환불일, title=ipo.title, scrap_url=ipo.scrap_url)
            days.append(ipo_day)
        if ipo.days.상장일:
            ipo_day = IpoDays(company=ipo.name, name='상장일', ymd=ipo.days.상장일, title=ipo.title, scrap_url=ipo.scrap_url)
            days.append(ipo_day)
    return days

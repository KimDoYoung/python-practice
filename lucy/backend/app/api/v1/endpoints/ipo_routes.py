# APIRouter 인스턴스 생성
from typing import List

from fastapi import APIRouter, Depends


from backend.app.domains.ipo.ipo_history_model import IpoHistory
from backend.app.domains.ipo.ipo_history_service import IpoHistoryService
from backend.app.domains.ipo.ipo_model import Ipo, IpoDays
from backend.app.domains.ipo.ipo_service import IpoService
from backend.app.core.dependency import get_config_service, get_ipo_service, get_ipohistory_service
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

#---------- Ipo History  
@router.get("/history", response_model=List[IpoHistory])
async def get_ipo_datas(service :IpoHistoryService=Depends(get_ipohistory_service)):
    ''' 공모주 데이터 모두 조회'''
    history_list = await service.get_all()
    return history_list

@router.get("/history/{ipo_id}", response_model=IpoHistory)
async def get_ipo_datas(ipo_id:str, service :IpoHistoryService=Depends(get_ipohistory_service)):
    ''' 공모주 데이터  1 개 조회'''
    history = await service.get_1(ipo_id)
    return history

@router.post("/history", response_model=dict)
async def create_ipo_history(history: IpoHistory, service :IpoHistoryService=Depends(get_ipohistory_service)):
    ''' 공모주 데이터 생성'''
    history = await service.create(history.model_dump())
    return {"result": 'OK', "_id": str(history.id)}

@router.delete("/history/{ipo_id}", response_model=dict)
async def delete_ipo_history(ipo_id: str, service :IpoHistoryService=Depends(get_ipohistory_service)):
    ''' 공모주 데이터 삭제 '''
    await service.delete_1(ipo_id)

    return {"result": 'OK'}

@router.put("/history/{ipo_id}", response_model=IpoHistory)
async def update_ipo_history(ipo_id: str, history: IpoHistory,service :IpoHistoryService=Depends(get_ipohistory_service)):
    ''' 공모주 history 데이터 수정'''
    await service.update_1(ipo_id, history)
    updated_history = await service.get_1(ipo_id)
    return updated_history



@router.get("/make-formula", response_model=dict)
async def update_ipo_history(service :IpoHistoryService=Depends(get_ipohistory_service)):
    '''데이터로 곱하기변수를 계산하는 공식을 만든다'''
    formula = await service.make_formula()
    config_service = get_config_service()
    dbconfig = await config_service.get_1('ipo_expected_cost_express')
    if dbconfig:
        dbconfig.value = formula
        await dbconfig.save()
    else:
        dbconfig = await config_service.create({'key': 'ipo_expected_cost_express', 'value': formula})
    logger.debug(f'Formula: {formula}')
    return {'formula': formula}
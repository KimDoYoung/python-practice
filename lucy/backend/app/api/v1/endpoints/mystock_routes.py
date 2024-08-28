# mystock_routes.py
"""
모듈 설명: 
    - mystock 관련 API 라우터
주요 기능:
    - get_list : 나의 주식 목록 조회
    - delete_mystock : 나의 주식 삭제
    - add_mystock : 나의 주식 추가
    - danta : 단타 머신에서 쓰는 service

작성자: 김도영
작성일: 2024-08-21
버전: 1.0
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from backend.app.core.logger import get_logger
from backend.app.domains.stc.ls.model.t0424_model import T0424INBLOCK, T0424_Request
from backend.app.domains.stc.ls.model.t8407_model import T8407_Request, T8407_Response, T8407InBLOCK
from backend.app.domains.system.mystock_model import MyStock, MyStockDto
from backend.app.domains.system.mystock_service import MyStockService
from backend.app.core.dependency import  get_mystock_service
from backend.app.managers.stock_api_manager import StockApiManager
from backend.app.utils.naver_util import get_stock_info
from typing import List

logger = get_logger(__name__)

router = APIRouter()

@router.get("/", response_model=List[MyStock])
async def get_list(
    stk_type: Optional[str] = Query(None, description="주식 유형 필터 (예: 단타, 관심, 보유)"),
    mystock_service: MyStockService = Depends(get_mystock_service)
) -> List[MyStock]:
    '''나의 주식 목록 조회'''
    if stk_type:
        list = await mystock_service.get_all_by_type(stk_type)
    else:
        list = await mystock_service.get_all()
    return list

@router.delete("/delete/{id}")
async def delete_mystock(id: str, mystock_service :MyStockService=Depends(get_mystock_service)):
    ''' 나의 주식 id로 삭제 '''
    try:
        await mystock_service.delete_by_id(id)
        return {"message": "MyStock deleted successfully"}
    except Exception as e:
        logger.error(f"Failed to delete mystock: {e}")
        raise HTTPException(status_code=400, detail="Failed to delete mystock")

@router.post("/add")
async def add_mystock(mystock_dto:MyStockDto, mystock_service :MyStockService=Depends(get_mystock_service)):
    ''' 나의 주식 1개 추가 '''
    try:
        await mystock_service.upsert(mystock_dto)
        return {"message": "MyStock added successfully"}
    except Exception as e:
        logger.error(f"Failed to add mystock: {e}")
        raise HTTPException(status_code=400, detail="Failed to add mystock")

@router.get("/danta", response_model=dict)
async def danta(mystock_service :MyStockService=Depends(get_mystock_service)):
    ''' 단타 머신에서 쓰는 service '''
    mystock_dto = MyStockDto(stk_code="005931", stk_name="AAA")
    mystock_dto.buy_ordno = "1234"
    mystock_dto.buy_qty = 10
    mystock_dto.buy_price = 1000
    mystock_dto.buy_time = "2021-07-01 10:00:00"
    mystock_dto.stk_types = ["단타"]
    await mystock_service.upsert(mystock_dto)
    danta_list = await  mystock_service.get_all_by_type('단타')
    for danta in danta_list:
        logger.debug(danta)
    mystock_dto.sell_ordno = "5678"
    mystock_dto.sell_qty = 10
    mystock_dto.sell_price = 2000
    mystock_dto.sell_time = "2021-07-01 10:30:00"
    await mystock_service.upsert(mystock_dto)
    await mystock_service.delete_all_by_type('단타')
    return {"message": "Danta success"}

@router.get("/naver-info/{stk_code}", response_model=dict)
async def naver_info(stk_code: str):
    ''' 네이버 주식 정보 조회 '''
    stock_info = get_stock_info(stk_code)
    return stock_info

@router.put('/add/stktype/{stk_code}/{stk_type}', response_model=dict)
async def add_stktype(stk_code: str, stk_type: str, mystock_service :MyStockService=Depends(get_mystock_service)):
    ''' 
        stk_code로 찾아서 거기에 stk_type을 추가한다. 이미 있으면 추가하지 않는다.
    '''
    mystock = await mystock_service.get_1(stk_code)
    if mystock:
        if stk_type not in mystock.stk_types:
            mystock.stk_types.append(stk_type)
            await mystock.save()
            
    return {"message": "Add success"}

@router.put('/extract/stktype/{stk_code}/{stk_type}', response_model=dict)
async def add_stktype(stk_code: str, stk_type: str, mystock_service :MyStockService=Depends(get_mystock_service)):
    ''' 
        stk_code로 찾아서 거기에 stk_type이 있으면 제거한다.
    '''
    mystock = await mystock_service.get_1(stk_code)
    if mystock:
        if stk_type in mystock.stk_types:
            mystock.stk_types.remove(stk_type)
            if not mystock.stk_types:
                await mystock.delete()
            else:
                await mystock.save()            
    return {"message": "Add success"}


@router.get("/extract/stktype", response_model=dict)
async def extract_stktype(stk_type: Optional[str] = Query(None, description="주식 유형 필터 (예: 단타, 관심, 보유)"),
                        mystock_service :MyStockService=Depends(get_mystock_service)):
    ''' 
    stk_type을 갖고 있는 모든 MyStock 찾아서 거기에서 stk_types에서 제거 
    stk_types가 모두 비어 있으면 그것 자체를 삭제
    '''
    if stk_type.lower() == 'all':
        await mystock_service.delete_all()
        return {"message": "Extract all success"}
                
    mystocks = await mystock_service.get_all_by_type(stk_type)
    for mystock in mystocks:
        mystock.stk_types.remove(stk_type)
        if not mystock.stk_types:
            await mystock.delete()
        else:
            await mystock.save()
    return {"message": "Extract success"}

@router.get("/mykeep", response_model=dict)
async def mykeep(mystock_service :MyStockService=Depends(get_mystock_service)):
    ''' 
    내가 보유한 종목, 현재 보유를 모두 지우고 다시 추가한다.
    '''
    stk_type = '보유'
    mystocks = await mystock_service.get_all_by_type(stk_type)
    for mystock in mystocks:
        mystock.stk_types.remove(stk_type)
        if not mystock.stk_types:
            await mystock.delete()
        else:
            await mystock.save()
    # KIS에서 가져온 보유 종목
    kis_api = await StockApiManager().stock_api('KIS')
    kis_inquire_balance =  await kis_api.inquire_balance()
    output1 = kis_inquire_balance.output1
    for item in output1:
        stk_code = item.pdno
        stk_name = item.prdt_name
        if '스팩' in stk_name:
            continue
        stk_types = ['보유']
        mystock_dto = MyStockDto(stk_code=stk_code, stk_name=stk_name, stk_types=stk_types, stk_company='KIS')
        await mystock_service.upsert(mystock_dto)    
    # LS에서 가져온 보유 종목
    ls_api = await StockApiManager().stock_api('LS')
    response = await ls_api.jango2(T0424_Request(t0424InBlock=T0424INBLOCK()))
    list = response.t0424OutBlock1
    for item in list:
        stk_code = item.expcode
        stk_name = item.hname
        if '스팩' in stk_name:
            continue
        stk_types = ['보유']
        mystock_dto = MyStockDto(stk_code=stk_code, stk_name=stk_name, stk_types=stk_types, stk_company='LS')
        await mystock_service.upsert(mystock_dto)
    
    return {"message": "Extract success"}

@router.get("/current_costs/{stk_codes}", response_model=T8407_Response)
async def current_costs(stk_codes:str):
    ''' 현재 비용 조회(멀티) '''
    ls_api = await StockApiManager().stock_api('LS')
    count = int(len(stk_codes)/6)
    
    # t8407in = T8407InBLOCK(nrec=len(stk_codes), shcode=''.join(stk_codes))
    t8407in = T8407InBLOCK(nrec=count, shcode=stk_codes)
    response = await ls_api.multi_current_cost(T8407_Request(t8407InBlock=t8407in))
    return response


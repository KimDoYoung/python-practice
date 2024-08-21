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
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from backend.app.core.logger import get_logger
from backend.app.domains.system.mystock_model import MyStock, MyStockDto
from backend.app.domains.system.mystock_service import MyStockService
from backend.app.core.dependency import  get_mystock_service

logger = get_logger(__name__)

router = APIRouter()

@router.get("/", response_model=List[MyStock])
async def get_list(mystock_service :MyStockService=Depends(get_mystock_service)) -> List[MyStock]:
    ''' 나의 주식 목록 조회'''
    list = await mystock_service.get_all()
    # list.sort(key=lambda x: x.last_update_time)
    return list

@router.delete("/delete/{id}")
async def delete_mystock(id: str, mystock_service :MyStockService=Depends(get_mystock_service)):
    ''' 나의 주식 삭제 '''
    try:
        await mystock_service.delete_by_id(id)
        return {"message": "MyStock deleted successfully"}
    except Exception as e:
        logger.error(f"Failed to delete mystock: {e}")
        raise HTTPException(status_code=400, detail="Failed to delete mystock")

@router.post("/add")
async def add_mystock(mystock_dto:MyStockDto, mystock_service :MyStockService=Depends(get_mystock_service)):
    ''' 나의 주식 추가 '''
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

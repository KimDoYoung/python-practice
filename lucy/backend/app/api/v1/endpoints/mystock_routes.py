# APIRouter 인스턴스 생성
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

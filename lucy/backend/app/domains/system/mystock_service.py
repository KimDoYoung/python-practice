# mystock_service.py
"""
모듈 설명: 
    - MyStock Collection에 대한 비즈니스 로직을 처리하는 서비스
주요 기능:
    - MyStock Collection에 대한 CRUD

작성자: 김도영
작성일: 07
버전: 1.0
"""
from bson import ObjectId
from fastapi import HTTPException
from backend.app.core.logger import get_logger
from motor.motor_asyncio import AsyncIOMotorClient

from backend.app.domains.system.mystock_model import MyStock, MyStockDto
from backend.app.core.dependency import get_ipo_service
from backend.app.utils import naver_util

logger = get_logger(__name__)


class MyStockService:

    async def create(self, data: MyStockDto) -> MyStock:
        mystock = MyStock(**data.model_dump())
        await mystock.create()
        return mystock
    
    async def get_all(self) -> list[MyStock]:
        ''' MyStock Collection에서 모든 document를 가져온다.'''
        try:
            mystocks = await MyStock.find().to_list()
            return mystocks
        except Exception as e:
            logger.error(f"Failed to retrieve all MyStocks: {e}")
            raise e

    async def delete_by_id(self, id: str) -> bool:
        if not ObjectId.is_valid(id):   
            raise HTTPException(status_code=400, detail="Invalid ID format")
        mystock = await MyStock.get(id)        
        if mystock:
            await mystock.delete()
            return True
        else:
            return False

    async def delete(self, stk_code: str) -> bool:
        mystock = await MyStock.find_one(MyStock.stk_code == stk_code)
        if mystock:
            await mystock.delete()
            return True
        else:
            return False
    async def get_1(self, stk_code:str) -> MyStock:
        mystock = await MyStock.find_one(MyStock.stk_code == stk_code)
        return mystock
        
    async def upsert(self, mystock_dto: MyStockDto):
        stk_code = mystock_dto.stk_code
        stk_types = mystock_dto.stk_types

        mystock = await self.get_1(stk_code)
        if mystock:
            for stk_type in stk_types:
                if stk_type not in mystock.stk_types:
                    mystock.stk_types.append(stk_type)
            await mystock.save()
        else:
            stock_info = naver_util.get_stock_info(stk_code)
            if not stock_info['stk_name']:
                ipo_service = get_ipo_service()
                ipo = await ipo_service.get_ipo(stk_code)
                if not ipo.stk_name:
                    raise HTTPException(status_code=400, detail="No stock name found")
                mystock_dto.stk_name = ipo.stk_name
            else:
                mystock_dto.stk_name = stock_info['stk_name']
            mystock = await self.create(mystock_dto)
                
        return mystock
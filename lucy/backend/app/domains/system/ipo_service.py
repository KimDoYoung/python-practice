from datetime import datetime
from typing import Any, Dict, List, Optional
from beanie import PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import ValidationError
from backend.app.domains.system.config_model import DbConfig
import logging

from backend.app.domains.system.eventdays_model import EventDays
from backend.app.domains.system.ipo_model import Ipo

from backend.app.core.logger import get_logger

logger = get_logger(__name__)

class IpoService:
    # _instance = None
    def __init__(self, db_client: AsyncIOMotorClient):
        self.db_client = db_client

    async def create(self, keyvalue: dict):
        ipo = Ipo(**keyvalue)
        await ipo.create()
        return ipo
    

    async def get_days_between(self, startYmd: str, endYmd: str)-> List[Ipo]:
        ipo_list = await Ipo.find({
            "$or": [
                {"days.청약일": {"$gte": startYmd, "$lte": endYmd}},
                {"days.납입일": {"$gte": startYmd, "$lte": endYmd}},
                {"days.환불일": {"$gte": startYmd, "$lte": endYmd}},
                {"days.상장일": {"$gte": startYmd, "$lte": endYmd}}
            ]
        }).to_list()

        return ipo_list

    async def get_days(self, yyyymm:str) -> List[Ipo]:
        ''' ipo class에서 days의 각각의 청약일, 납입일, 환불일, 상장일 을 각각 yyyymm과 비교해서 한개라도 해당하면 ipo 데이터를 가져온다.'''
        pattern = f'^{yyyymm}'
        try:
            ipos_raw  = await Ipo.find({
                "$or": [
                    {"days.청약일": {"$regex": pattern}},
                    {"days.납입일": {"$regex": pattern}},
                    {"days.환불일": {"$regex": pattern}},
                    {"days.상장일": {"$regex": pattern}}
                ]
            }).to_list()
            # return ipos
            return ipos_raw
        except Exception as e:
            logger.error(f"Failed to retrieve all Ipos: {e}")
            raise e

    async def get_all(self, onlyFuture:bool=False, sorting:bool= True) -> List[Ipo]:
        ''' onlyFuture가 True이면 현재 날짜 이후의 데이터만 가져온다. sorting이 True이면 processed_time을 기준으로 내림차순으로 정렬한다.'''
        try:
            current_date = datetime.now().strftime('%Y%m%d')
            query = {}
            if onlyFuture:
                query = {
                    "$or": [
                        {"days.청약일": {"$gte": current_date}},
                        {"days.납입일": {"$gte": current_date}},
                        {"days.환불일": {"$gte": current_date}},
                        {"days.상장일": {"$gte": current_date}}
                    ]
                }
            
            ipos = await Ipo.find(query).to_list()
            
            if sorting:
                ipos = sorted(ipos, key=lambda x: x.processed_time, reverse=True)
            else:
                ipos = sorted(ipos, key=lambda x: x.processed_time)

            return ipos
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
    
    async def update_by_id(self, id: PydanticObjectId, data: Dict[str, Any]) -> Optional[Ipo]:
        ipo = await Ipo.get(id)
        if ipo:
            await ipo.set(data)
            await ipo.save()
            return ipo
        else:
            logger.error(f"Ipo with id {id} not found")
            return None

    async def update_by_stk_name(self, stk_name: str, data: Dict[str, Any]) -> Optional[Ipo]:
        ipo = await Ipo.find_one(Ipo.stk_name == stk_name)
        if ipo:
            return await self.update_by_id(id=ipo.id, data=data)
        else:
            logger.error(f"Ipo with stk_name {stk_name} not found")
            return None

    async def delete(self, id: PydanticObjectId) -> Ipo:
        ipo = await Ipo.get(id)
        if ipo:
            ipo = await ipo.delete()
            return ipo


    async def get_ipo(self, stk_code: str) -> Ipo:
        ipo = await Ipo.find_one(Ipo.stk_code == stk_code)
        return ipo
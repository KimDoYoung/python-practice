from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.domain.hdd.hdd_schema import GroupItemResponse
from app.domain.hdd.hdd_service import HDDService


router = APIRouter()
@router.get("/hdd/volumn-list", response_model=List[GroupItemResponse])
async def hdd_volumn_list(db: AsyncSession = Depends(get_session)):
    ''' HDD volumn 리스트 조회 '''
    service = HDDService(db)
    return await service.volumn_list()

#TODO : 트리 구조를 생각하면서 구현해야함

# @router.get("/hdd/list/{volumn_name}", response_model=List[HDDResponse])
# async def hdd_list(volumn_name: str, directory_only: bool,  db: AsyncSession = Depends(get_session)):
#     ''' HDD 리스트 조회 '''
#     service = HDDService(db)
#     return await service.hdd_list(volumn_name, directory_only)

# @router.get("/hdd/root/list/{volumn_name}", response_model=List[HDDResponse])
# async def hdd_list(volumn_name: str,  db: AsyncSession = Depends(get_session)):
#     ''' HDD 리스트 조회 '''
#     service = HDDService(db)
#     return await service.hdd_list(volumn_name, directory_only)

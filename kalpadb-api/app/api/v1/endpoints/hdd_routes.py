from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.domain.hdd.hdd_schema import GroupItemResponse, HDDChildRequest, HDDResponse, HDDSearchRequest, HDDSearchResponse
from app.domain.hdd.hdd_service import HDDService


router = APIRouter()
@router.get("/hdd/volumn-list", response_model=List[GroupItemResponse])
async def hdd_volumn_list(db: AsyncSession = Depends(get_session)):
    ''' HDD volumn 리스트 조회 '''
    service = HDDService(db)
    return await service.volumn_list()

@router.get("/hdd/child/{volumn_name}/{pid}/{gubun}", response_model=List[HDDResponse])
async def hdd_child_list(volumn_name: str, pid: int, gubun: str,  db: AsyncSession = Depends(get_session)):
    ''' volumn_name과  pid로 child 리스트 조회 '''
    childreq = HDDChildRequest(volumn_name=volumn_name, pid=pid, gubun=gubun)
    service = HDDService(db)
    return await service.hdd_child_list(childreq)

@router.get("/hdd/search", response_model=HDDSearchResponse)
async def search_hdd(
    search_text: str = None,
    volumn_name: str = None,
    gubun: str = 'A',
    start_index: int = 0,
    limit: int = 10,  
    db: AsyncSession = Depends(get_session)):
    ''' HDD 검색 '''
    search_req = HDDSearchRequest(search_text=search_text, 
                volumn_name=volumn_name, 
                gubun=gubun, 
                start_index=start_index, 
                limit=limit)
    service = HDDService(db)
    return await service.search_hdd(search_req)

# judal_routes.py
"""
모듈 설명: 
    - judal관련 API 라우터
주요 기능:
    -   기능을 넣으시오

작성자: 김도영
작성일: 2024-08-21
버전: 1.0
"""
from typing import List

from fastapi import APIRouter, Depends

from backend.app.core.logger import get_logger
from backend.app.domains.judal.judal_model import JudalCsvData, JudalStock, JudalTheme, QueryCondition
from backend.app.domains.judal.judal_service import JudalService
from backend.app.core.dependency import get_judal_service

logger = get_logger(__name__)

router = APIRouter()

@router.get("/themes", response_model=List[JudalTheme])
async def themes(judal_service :JudalService=Depends(get_judal_service)) -> List[JudalTheme]:
    ''' 테마 목록을 리턴'''
    list = await judal_service.get_themes()
    list = [theme for theme in list if '테마' in theme.name and theme.name != "전체 테마"]
    
    return list

@router.get("/detail-themes", response_model=List[JudalTheme])
async def detail_themes(judal_service :JudalService=Depends(get_judal_service)) -> List[JudalTheme]:
    ''' 상세 테마 목록을 리턴'''
    list = await judal_service.get_detail_themes()   
    return list

@router.get("/csv/{csv_file_name}", response_model=List[JudalCsvData])
async def csv_file(csv_file_name:str, judal_service :JudalService=Depends(get_judal_service)):
    ''' csv_file을 읽어서 리턴'''
    list = await judal_service.get_csv_file(csv_file_name)
    return list

@router.post("/search", response_model=List[JudalStock])
async def search(query: QueryCondition, judal_service :JudalService=Depends(get_judal_service)):
    ''' 검색조건에 맞는 주식 목록을 리턴'''
    logger.debug(f'검색조건: {query}')
    list = await judal_service.search(query)
    return list
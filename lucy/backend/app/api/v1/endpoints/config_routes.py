# APIRouter 인스턴스 생성
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from backend.app.domains.system.config_model import DbConfig, DbConfigRequest
from backend.app.domains.system.config_service import DbConfigService
from backend.app.core.dependency import get_config_service
from backend.app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

@router.get("/", response_model=List[DbConfig])
async def get_config_list(config_service :DbConfigService=Depends(get_config_service)) -> List[DbConfig]:
    ''' Config 모두 조회'''
    list = await config_service.get_all()
    return list

@router.get("/{key}", response_model=DbConfig)
async def get_1(key:str, config_service :DbConfigService=Depends(get_config_service)) -> DbConfig:
    ''' Config 1개 조회'''
    dbconfig = await config_service.get_1(key)
    return dbconfig

@router.post("/",  response_model=DbConfig)
async def create_1(dbconfig : DbConfigRequest, config_service :DbConfigService=Depends(get_config_service)) -> DbConfig:
    ''' Config 추가'''
    existing_config = await config_service.get_1(DbConfig.key == dbconfig.key)
    if existing_config:
        raise HTTPException(status_code=400, detail="Config with this key already exists")
    dbconfig = await config_service.create(dbconfig.model_dump())
    return dbconfig

@router.put("/{key}",  response_model=DbConfig)
async def update_1(key:str, dbconfig : DbConfigRequest, config_service :DbConfigService=Depends(get_config_service)) -> DbConfig:
    ''' Config document 수정'''
    dbconfig = await config_service.update_1(key, dbconfig.model_dump())
    return dbconfig

@router.delete("/{key}",  response_model=DbConfig)
async def delete_1(key:str, config_service :DbConfigService=Depends(get_config_service)) -> DbConfig:
    ''' Config 삭제'''
    dbconfig = await config_service.delete_1(key)
    if not dbconfig:
        raise HTTPException(status_code=404, detail="Config not found")
    return dbconfig

# company_routes.py
"""
모듈 설명: 
    -  회사 정보를 등록, 조회, 삭제하는 API 라우터
    -  app_key, app_secret_key를 생성하여 회사 정보와 함께 저장
    -  회사 정보는 회사 ID, 서비스명, 시작일, 종료일로 구성
주요 기능:
    - /api/v1/company/ : 회사 목록 조회
    - /api/v1/company/register : 회사 정보 등록
    - /api/v1/company/delete/{company_id}/{service_id} : 회사 정보 삭제

작성자: 김도영
작성일: 2024-10-10
버전: 1.0
"""
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.logger import get_logger
from backend.app.core.database import get_session
from backend.app.core.security import generate_app_key, secret_key_encrypt
from backend.app.domain.ifi.ifi01.ifi01_company_api_schema import Ifi01CompanyApiCreate, Ifi01CompanyApiResponse
from backend.app.domain.ifi.ifi01.ifi01_company_api_service import Ifi01CompanyApiService
from backend.app.domain.sys.sys01.code_service import CodeService
from backend.app.domain.sys.sys01.sys01_company_schema import Sys09CodeResponse
from backend.app.domain.sys.sys01.sys01_company_service import Sys01CompanyService

logger = get_logger(__name__)

router = APIRouter()

@router.get("/",  response_model=List[Ifi01CompanyApiResponse])
async def list(db: AsyncSession = Depends(get_session)):
    ''' ifi01 회사 목록 조회-view '''
    service = Ifi01CompanyApiService(db)
    company_list = await service.get_company_all()
    return company_list

@router.get("/info/{company_api_id}",  response_model=Ifi01CompanyApiResponse)
async def info(company_api_id: int,  db: AsyncSession = Depends(get_session)):
    ''' 1개의 회사정보찾기-view '''
    service = Ifi01CompanyApiService(db)
    company = await service.get_company_api(company_api_id)
    app_secret_key = secret_key_encrypt(company.ifi01_app_key, f"{company.ifi01_company_id}|{company.ifi01_service_cd}|{company.ifi01_start_date}")
    resp = Ifi01CompanyApiResponse.model_validate(company)
    resp.ifi01_app_secret_key = app_secret_key
    
    #회사명조회
    company_service = Sys01CompanyService(db)
    sys01_company  = await company_service.get(company.ifi01_company_id)
    resp.sys01_company_nm =  sys01_company.sys01_company_nm if sys01_company else ""
    #Service Name조회
    code_service = CodeService(db)
    service_nm = await code_service.get_name('ApiServiceCode',company.ifi01_service_cd)
    resp.ifi01_service_nm = service_nm
    
    return resp


@router.delete("/delete/{company_api_id}",  response_model=Ifi01CompanyApiResponse)
async def delete(company_api_id:int,  db: AsyncSession = Depends(get_session)):
    ''' 회사 정보 삭제 '''
    service = Ifi01CompanyApiService(db)
    logger.debug(f"회사 정보 삭제: {company_api_id}")
    deleted_company = await service.delete_company_api(company_api_id)
    resp =  Ifi01CompanyApiResponse.model_validate(deleted_company)
    return resp
    
@router.get("/code/{category}",  response_model=List[Sys09CodeResponse])
async def services(category:str, db: AsyncSession = Depends(get_session)):
    ''' 코드 서비스 목록 조회-view '''
    service = CodeService(db)
    code_list = await service.get_code_by_category(category)
    return [Sys09CodeResponse.model_validate(code) for code in code_list]


@router.post("/register",  response_model=Ifi01CompanyApiResponse)
async def register(company: Ifi01CompanyApiCreate, db: AsyncSession = Depends(get_session)):
    ''' 회사정보에 기반하여 app_key, secret_key를 만들고 Db에 Insert한다. '''
    # app_key와 app_secret_key 생성 (고유한 값으로)
    service01 = Ifi01CompanyApiService(db)
    app_key = generate_app_key()
    data = f"{company.ifi01_company_id}|{company.ifi01_service_cd}|{company.ifi01_start_date}"
    app_secret_key = secret_key_encrypt(app_key, data)

    dict = company.model_dump()
    dict.update({'ifi01_app_key': app_key})
    new_company = await service01.create_company_api(dict)

    # 회사명 조회
    company_service = Sys01CompanyService(db)
    sys01_company  = await company_service.get(new_company.ifi01_company_id)
    company_name = sys01_company.sys01_company_nm if sys01_company else ""
    #Service Name조회
    code_service = CodeService(db)
    service_nm = await code_service.get_name('ApiServiceCode',company.ifi01_service_cd)
    
    resp = Ifi01CompanyApiResponse (
        ifi01_company_api_id=new_company.ifi01_company_api_id,
        ifi01_company_id=new_company.ifi01_company_id,
        sys01_company_nm = company_name,
        ifi01_service_cd=new_company.ifi01_service_cd,
        ifi01_service_nm=service_nm,
        ifi01_start_date=new_company.ifi01_start_date,
        ifi01_close_date=new_company.ifi01_close_date,
        ifi01_app_key=app_key,
        ifi01_app_secret_key=app_secret_key,
        ifi01_created_date=new_company.ifi01_created_date
    )

    logger.info(f"새로운 회사 등록: {resp}")
    return resp

@router.post("/re-register/{company_api_id}",  response_model=Ifi01CompanyApiResponse)
async def register(company_api_id:int, company: Ifi01CompanyApiCreate, db: AsyncSession = Depends(get_session)):
    '''재등록-회사정보에 기반하여 app_key, secret_key를 만들고 Db에 Update '''
    # app_key와 app_secret_key 생성 (고유한 값으로)
    service = Ifi01CompanyApiService(db)
    app_key = generate_app_key()
    data = f"{company.ifi01_company_id}|{company.ifi01_service_cd}|{company.ifi01_start_date}"
    app_secret_key = secret_key_encrypt(app_key, data)

    dict = company.model_dump()
    dict.update({'ifi01_company_api_id': company_api_id})
    dict.update({'ifi01_app_key': app_key})
    dict.update({'ifi01_app_secret_key': app_secret_key})
    dict.update({'ifi01_update_date': datetime.now()})
    logger.info(f"업데이트 회사 정보: {dict}")
    updated_company = await service.update_company_api(company_api_id, dict)


    # 응답으로 Pydantic CompanyResponse 모델 반환
    resp = Ifi01CompanyApiResponse(
        ifi01_company_api_id=updated_company.ifi01_company_api_id,
        ifi01_company_id=updated_company.ifi01_company_id,
        ifi01_service_cd=updated_company.ifi01_service_cd,
        ifi01_start_date=updated_company.ifi01_start_date,
        ifi01_close_date=updated_company.ifi01_close_date,
        ifi01_app_key=app_key,
        ifi01_app_secret_key=app_secret_key,
        ifi01_created_date=updated_company.ifi01_created_date,
        ifi01_update_date =  updated_company.ifi01_update_date
    )
    #회사명조회
    company_service = Sys01CompanyService(db)
    sys01_company  = await company_service.get(updated_company.ifi01_company_id)
    company_nm = sys01_company.sys01_company_nm if sys01_company else ""
    resp.sys01_company_nm = company_nm
    
    #Service Name조회
    code_service = CodeService(db)
    service_nm = await code_service.get_name('ApiServiceCode',company.ifi01_service_cd)
    resp.ifi01_service_nm = service_nm
    
    logger.info(f"업데이트 회사 : {resp}")
    
    return resp    
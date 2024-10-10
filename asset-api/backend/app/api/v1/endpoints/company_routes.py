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
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.logger import get_logger
from backend.app.domain.company.company_schema import CompanyRequest, CompanyResponse
from backend.app.core.database import get_session
from backend.app.core.security import generate_app_key, secret_key_encrypt
from backend.app.domain.company.company_service import create_company, delete_company, get_all_companies
logger = get_logger(__name__)

router = APIRouter()

@router.get("/",  response_model=List[CompanyResponse])
async def list(db: AsyncSession = Depends(get_session)):
    ''' 회사 목록 조회, 발급일 역순으로 정렬 '''
    company_list = await get_all_companies(db)  # 비동기 함수 호출 시 await 사용
    
    # SQLAlchemy 모델을 Pydantic 모델로 변환
    return [CompanyResponse.model_validate(company) for company in company_list]

@router.delete("/delete/{company_id}/{service_id}",  response_model=CompanyResponse)
async def delete(company_id:int, service_id:str, db: AsyncSession = Depends(get_session)):
    ''' 회사 정보 삭제 '''
    logger.debug(f"회사 정보 삭제: {company_id}, {service_id}")
    deleted_company = await delete_company(db, company_id, service_id)
    return CompanyResponse.model_validate(deleted_company)
    

@router.post("/register",  response_model=CompanyResponse)
async def register(company: CompanyRequest, db: AsyncSession = Depends(get_session)):
    ''' 회사정보에 기반하여 app_key, secret_key를 만들고 Db에 저장한다. '''
    # app_key와 app_secret_key 생성 (고유한 값으로)
    app_key = generate_app_key()
    data = f"{company.company_id}|{company.service_id}|{company.start_ymd}"
    app_secret_key = secret_key_encrypt(app_key, data)

    dict = company.model_dump()
    dict.update({'app_key': app_key})
    new_company = await create_company(db, dict)

    # 응답으로 Pydantic CompanyResponse 모델 반환
    resp = CompanyResponse(
        company_id=new_company.company_id,
        service_id=new_company.service_id,
        start_ymd=new_company.start_ymd,
        end_ymd=new_company.end_ymd,
        app_key=app_key,
        app_secret_key=app_secret_key,  # 실제로는 앱 시크릿을 노출하지 않는 게 좋음
        created_at=new_company.created_at
    )
    logger.info(f"새로운 회사 등록: {resp}")
    return resp
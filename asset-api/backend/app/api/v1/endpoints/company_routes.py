
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

@router.delete("/delete/{company_id}/{service_nm}",  response_model=CompanyResponse)
async def delete(company_id:int, service_nm:str, db: AsyncSession = Depends(get_session)):
    ''' 회사 정보 삭제 '''
    logger.debug(f"회사 정보 삭제: {company_id}, {service_nm}")
    deleted_company = await delete_company(db, company_id, service_nm)
    return CompanyResponse.model_validate(deleted_company)
    

@router.post("/register",  response_model=CompanyResponse)
async def register(company: CompanyRequest, db: AsyncSession = Depends(get_session)):
    ''' 회사정보에 기반하여 app_key, secret_key를 만들고 Db에 저장한다. '''
    # app_key와 app_secret_key 생성 (고유한 값으로)
    app_key = generate_app_key()
    data = f"{company.company_id}|{company.service_nm}|{company.start_ymd}"
    app_secret_key = secret_key_encrypt(app_key, data)

    dict = company.model_dump()
    dict.update({'app_key': app_key})
    new_company = await create_company(db, dict)

    # 응답으로 Pydantic CompanyResponse 모델 반환
    resp = CompanyResponse(
        company_id=new_company.company_id,
        service_nm=new_company.service_nm,
        start_ymd=new_company.start_ymd,
        end_ymd=new_company.end_ymd,
        app_key=app_key,
        app_secret_key=app_secret_key  # 실제로는 앱 시크릿을 노출하지 않는 게 좋음
    )
    logger.info(f"새로운 회사 등록: {resp}")
    return resp
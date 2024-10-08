
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.logger import get_logger
from backend.app.domain.company.company_model import CompanyModel
from backend.app.domain.company.company_schema import CompanyRequest, CompanyResponse
from backend.app.core.database import get_session
from backend.app.core.security import generate_app_key, secret_key_encrypt
logger = get_logger(__name__)

router = APIRouter()

@router.post("/register",  response_model=CompanyResponse)
async def register(company: CompanyRequest, db: AsyncSession = Depends(get_session)):
    ''' 회사정보에 기반하여 app_key, secret_key를 만들고 Db에 저장한다. '''
    # app_key와 app_secret_key 생성 (고유한 값으로)
    app_key = generate_app_key()
    data = f"{company.company_id}|{company.service_nm}|{company.start_ymd}"
    app_secret_key = secret_key_encrypt(app_key, data)

    # SQLAlchemy 객체로 데이터베이스에 저장
    new_company = CompanyModel(
        company_id=company.company_id,
        service_nm=company.service_nm,
        start_ymd=company.start_ymd,
        end_ymd=company.end_ymd,
        app_key=app_key
    )

    # DB에 추가
    db.add(new_company)
    db.commit()
    db.refresh(new_company)

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
from datetime import datetime
from typing import List, Optional
from sqlalchemy import func, text
from sqlalchemy.future import select
from backend.app.domain.ifi.ifi01.ifi01_company_api_model import Ifi01CompanyApi
from backend.app.core.logger import get_logger
from backend.app.domain.ifi.ifi01.ifi01_company_api_schema import Ifi01CompanyApiResponse
from backend.app.domain.sys.sys01.sys01_company_model import Sys01Company
from backend.app.core.database import get_session

logger = get_logger()

class Ifi01CompanyApiService:

    @staticmethod
    async def generate_company_api_id() -> Optional[int]:
        """회사 API ID 생성"""
        async with get_session() as session:
            result = await session.execute(text("SELECT f_create_seq()"))
            return result.scalar()

    @staticmethod
    async def create_company_api(data: dict) -> Ifi01CompanyApi:
        """회사 API 정보를 생성"""
        company_api_id = await Ifi01CompanyApiService.generate_company_api_id()

        # 날짜 형식 변환
        def parse_date(date_str):
            return datetime.strptime(date_str, '%Y-%m-%d').date() if isinstance(date_str, str) else date_str

        ifi01_start_date = parse_date(data['ifi01_start_date'])
        ifi01_close_date = parse_date(data['ifi01_close_date'])
        current_time = datetime.now()

        # Ifi01CompanyApi 객체 생성
        new_company_api = Ifi01CompanyApi(
            ifi01_company_api_id=company_api_id,
            ifi01_company_id=data['ifi01_company_id'],
            ifi01_service_cd=data['ifi01_service_cd'],
            ifi01_start_date=ifi01_start_date,
            ifi01_close_date=ifi01_close_date,
            ifi01_app_key=data['ifi01_app_key'],
            ifi01_created_date=current_time,
        )

        async with get_session() as session:
            session.add(new_company_api)
            await session.commit()
            await session.refresh(new_company_api)
            return new_company_api

    @staticmethod
    async def get_company_by_app_key(app_key: str) -> Optional[Ifi01CompanyApi]:
        """주어진 app_key에 해당하는 회사 API 정보를 반환"""
        async with get_session() as session:
            query = select(Ifi01CompanyApi).where(Ifi01CompanyApi.ifi01_app_key == app_key)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @staticmethod
    async def get_company_api(company_api_id: int) -> Optional[Ifi01CompanyApi]:
        """주어진 ID에 해당하는 회사 API 정보를 반환"""
        async with get_session() as session:
            query = select(Ifi01CompanyApi).where(Ifi01CompanyApi.ifi01_company_api_id == company_api_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @staticmethod
    async def get_company_all() -> List[Ifi01CompanyApiResponse]:
        """모든 회사 API 정보를 반환"""
        async with get_session() as session:
            query = (
                select(
                    Ifi01CompanyApi,
                    func.coalesce(Sys01Company.sys01_company_nm, '').label("sys01_company_name")
                )
                .outerjoin(Sys01Company, Ifi01CompanyApi.ifi01_company_id == Sys01Company.sys01_company_id)
                .order_by(Ifi01CompanyApi.ifi01_created_date.desc())
            )
            result = await session.execute(query)
            company_apis = result.all()

            return [
                Ifi01CompanyApiResponse(
                    ifi01_company_api_id=row.Ifi01CompanyApi.ifi01_company_api_id,
                    ifi01_company_id=row.Ifi01CompanyApi.ifi01_company_id,
                    ifi01_service_cd=row.Ifi01CompanyApi.ifi01_service_cd,
                    ifi01_start_date=row.Ifi01CompanyApi.ifi01_start_date,
                    ifi01_close_date=row.Ifi01CompanyApi.ifi01_close_date,
                    ifi01_app_key=row.Ifi01CompanyApi.ifi01_app_key,
                    ifi01_created_date=row.Ifi01CompanyApi.ifi01_created_date,
                    sys01_company_nm=row.sys01_company_name
                ) for row in company_apis
            ]

    @staticmethod
    async def delete_company_api(company_api_id: int) -> Optional[Ifi01CompanyApi]:
        """회사 API 삭제"""
        async with get_session() as session:
            query = select(Ifi01CompanyApi).where(Ifi01CompanyApi.ifi01_company_api_id == company_api_id)
            result = await session.execute(query)
            deleted_company = result.scalar_one_or_none()

            if deleted_company is None:
                logger.error(f"Company API with id {company_api_id} not found.")
                raise ValueError(f"Company API with id {company_api_id} does not exist.")

            try:
                await session.delete(deleted_company)
                await session.commit()
                logger.info(f"Company API with id {company_api_id} successfully deleted.")
            except Exception as e:
                logger.error(f"Failed to delete Company API with id {company_api_id}: {e}")
                await session.rollback()
                raise ValueError(f"Failed to delete Company API with id {company_api_id}: {str(e)}")

            return deleted_company

    @staticmethod
    async def update_company_api(company_api_id: int, data_dict: dict) -> Optional[Ifi01CompanyApi]:
        """회사 API 정보 업데이트"""
        async with get_session() as session:
            query = select(Ifi01CompanyApi).where(Ifi01CompanyApi.ifi01_company_api_id == company_api_id)
            result = await session.execute(query)
            updated_company = result.scalar_one_or_none()

            if updated_company is None:
                raise ValueError(f"Company API with id {company_api_id} not found.")

            for key, value in data_dict.items():
                if hasattr(updated_company, key):
                    setattr(updated_company, key, value)

            await session.commit()
            return updated_company

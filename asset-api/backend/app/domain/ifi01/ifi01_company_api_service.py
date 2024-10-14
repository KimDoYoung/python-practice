from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.app.domain.ifi01.ifi01_company_api_model import Ifi01CompanyApi
from backend.app.domain.ifi01.ifi01_company_api_schema import Ifi01CompanyApiCreate

class Ifi01CompanyApiService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # 회사 API 생성
    async def create_company_api(self, company_api_data: Ifi01CompanyApiCreate):
        new_company_api = Ifi01CompanyApi(**company_api_data.dict())
        self.db.add(new_company_api)
        await self.db.commit()
        await self.db.refresh(new_company_api)
        return new_company_api

    # 회사 API 정보 가져오기
    async def get_company_api(self, company_api_id: int):
        stmt = select(Ifi01CompanyApi).where(Ifi01CompanyApi.ifi01_company_api_id == company_api_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    # 회사 API 리스트 가져오기
    async def get_company_apis(self):
        stmt = select(Ifi01CompanyApi)
        result = await self.db.execute(stmt)
        return result.scalars().all()

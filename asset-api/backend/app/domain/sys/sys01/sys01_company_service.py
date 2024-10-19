from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.domain.sys.sys01.sys01_company_model import Sys01Company

class Sys01CompanyService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, company_id: int):
        # 비동기적으로 쿼리를 실행
        result = await self.db.execute(
            select(Sys01Company).filter(Sys01Company.sys01_company_id == company_id)
        )
        return result.scalars().first()  # 결과를 스칼라 값으로 변환 후 첫 번째 결과 반환

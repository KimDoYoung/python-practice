from sqlalchemy.future import select
from backend.app.core.database import get_session
from backend.app.domain.sys.sys01.sys01_company_model import Sys01Company

class Sys01CompanyService:

    @staticmethod
    async def get(company_id: int) -> Sys01Company:
        """주어진 company_id에 해당하는 회사 정보를 비동기적으로 가져옵니다."""
        async with get_session() as session:
            query = select(Sys01Company).where(Sys01Company.sys01_company_id == company_id)
            result = await session.execute(query)
            company = result.scalar_one_or_none()
            return company

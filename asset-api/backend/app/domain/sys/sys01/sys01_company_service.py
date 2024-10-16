from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.domain.sys.sys01.sys01_company_model import Sys01Company

class Sys01CompanyService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def get(self, company_id: int):
        return self.db.query(Sys01Company).filter(Sys01Company.sys01_company_id == company_id).first()




from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.app.domain.ifi.ifi10.ifi10_law_model import Ifi10Law
from backend.app.domain.ifi.ifi10.ifi10_law_schema import Ifi10LawCreate

class Ifi10LawService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # 법규 생성
    async def create_law(self, law_data: Ifi10LawCreate):
        new_law = Ifi10Law(**law_data.dict())
        self.db.add(new_law)
        await self.db.commit()
        await self.db.refresh(new_law)
        return new_law

    # 법규 정보 가져오기
    async def get_law(self, law_id: int):
        stmt = select(Ifi10Law).where(Ifi10Law.ifi10_law_id == law_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    # 법규 리스트 가져오기
    async def get_laws(self):
        stmt = select(Ifi10Law)
        result = await self.db.execute(stmt)
        return result.scalars().all()

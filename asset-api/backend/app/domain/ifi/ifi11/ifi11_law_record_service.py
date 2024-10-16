from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.app.domain.ifi11.ifi11_law_record_model import Ifi11LawRecord
from backend.app.domain.ifi11.ifi11_law_record_schema import Ifi11LawRecordCreate

class Ifi11LawRecordService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # 법규 기록 생성
    async def create_law_record(self, law_record_data: Ifi11LawRecordCreate):
        new_law_record = Ifi11LawRecord(**law_record_data.dict())
        self.db.add(new_law_record)
        await self.db.commit()
        await self.db.refresh(new_law_record)
        return new_law_record

    # 법규 기록 정보 가져오기
    async def get_law_record(self, law_record_id: int):
        stmt = select(Ifi11LawRecord).where(Ifi11LawRecord.ifi11_law_record_id == law_record_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    # 법규 기록 리스트 가져오기
    async def get_law_records(self):
        stmt = select(Ifi11LawRecord)
        result = await self.db.execute(stmt)
        return result.scalars().all()

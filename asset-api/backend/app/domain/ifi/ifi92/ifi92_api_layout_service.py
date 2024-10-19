from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.app.domain.ifi.ifi92.ifi92_api_layout_model import Ifi92ApiLayout
from backend.app.domain.ifi.ifi92.ifi92_api_layout_schema import Ifi92ApiLayoutCreate

class Ifi92ApiLayoutService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # API 레이아웃 생성
    async def create_api_layout(self, layout_data: Ifi92ApiLayoutCreate):
        new_layout = Ifi92ApiLayout(**layout_data.dict())
        self.db.add(new_layout)
        await self.db.commit()
        await self.db.refresh(new_layout)
        return new_layout

    # API 레이아웃 정보 가져오기
    async def get_api_layout(self, layout_id: int):
        stmt = select(Ifi92ApiLayout).where(Ifi92ApiLayout.ifi92_api_layout_id == layout_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    # API 레이아웃 리스트 가져오기
    async def get_api_layouts(self):
        stmt = select(Ifi92ApiLayout)
        result = await self.db.execute(stmt)
        return result.scalars().all()

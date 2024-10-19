from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.app.domain.ifi.ifi96.ifi96_file_layout_model import Ifi96FileLayout
from backend.app.domain.ifi.ifi96.ifi96_file_layout_schema import Ifi96FileLayoutCreate

class Ifi96FileLayoutService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # 파일 레이아웃 생성
    async def create_file_layout(self, file_layout_data: Ifi96FileLayoutCreate):
        new_file_layout = Ifi96FileLayout(**file_layout_data.dict())
        self.db.add(new_file_layout)
        await self.db.commit()
        await self.db.refresh(new_file_layout)
        return new_file_layout

    # 파일 레이아웃 정보 가져오기
    async def get_file_layout(self, file_layout_id: int):
        stmt = select(Ifi96FileLayout).where(Ifi96FileLayout.ifi96_file_layout_id == file_layout_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    # 파일 레이아웃 리스트 가져오기
    async def get_file_layouts(self):
        stmt = select(Ifi96FileLayout)
        result = await self.db.execute(stmt)
        return result.scalars().all()

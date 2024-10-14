from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.app.domain.ifi91.ifi91_config_api_model import Ifi91ConfigApi
from backend.app.domain.ifi91.ifi91_config_api_schema import Ifi91ConfigApiCreate

class Ifi91ConfigApiService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # API 설정 생성
    async def create_api(self, api_data: Ifi91ConfigApiCreate):
        new_api = Ifi91ConfigApi(**api_data.dict())
        self.db.add(new_api)
        await self.db.commit()
        await self.db.refresh(new_api)
        return new_api

    # API 정보 가져오기
    async def get_api(self, api_id: int):
        stmt = select(Ifi91ConfigApi).where(Ifi91ConfigApi.ifi91_config_api_id == api_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    # API 리스트 가져오기
    async def get_apis(self):
        stmt = select(Ifi91ConfigApi)
        result = await self.db.execute(stmt)
        return result.scalars().all()

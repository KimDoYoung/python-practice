from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.app.domain.ifi.ifi90.ifi90_config_model import Ifi90Config
from backend.app.domain.ifi.ifi90.ifi90_config_schema import Ifi90ConfigCreate

class Ifi90ConfigService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # I/F 설정 생성
    async def create_config(self, config_data: Ifi90ConfigCreate):
        new_config = Ifi90Config(**config_data.dict())
        self.db.add(new_config)
        await self.db.commit()
        await self.db.refresh(new_config)
        return new_config

    # I/F 설정 정보 가져오기
    async def get_config(self, config_id: int):
        stmt = select(Ifi90Config).where(Ifi90Config.ifi90_config_id == config_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    # I/F 설정 리스트 가져오기
    async def get_configs(self):
        stmt = select(Ifi90Config)
        result = await self.db.execute(stmt)
        return result.scalars().all()
